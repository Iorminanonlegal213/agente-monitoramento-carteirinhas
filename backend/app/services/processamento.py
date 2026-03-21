"""
Motor de processamento de vencimentos e geração de alertas.
Contém toda a lógica de classificação de criticidade.
"""
from datetime import date, datetime
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models import (
    Funcionario, FuncionarioRequisito, Carteirinha, Contrato,
    Alerta, ExecucaoProcessamento, EmpresaContratada, Requisito
)


def classificar_vencimento(data_vencimento: date | None, hoje: date) -> Tuple[str, str, int | None]:
    """
    Retorna (faixa_vencimento, criticidade, dias_restantes).
    """
    if data_vencimento is None:
        return ("sem_risco", "ok", None)

    dias = (data_vencimento - hoje).days

    if dias < 0:
        return ("vencido", "critica", dias)
    elif dias == 0:
        return ("vence_hoje", "critica", 0)
    elif dias <= 7:
        return ("ate_7_dias", "alta", dias)
    elif dias <= 15:
        return ("ate_15_dias", "media", dias)
    elif dias <= 30:
        return ("ate_30_dias", "media", dias)
    elif dias <= 60:
        return ("ate_60_dias", "baixa", dias)
    else:
        return ("sem_risco", "ok", dias)


def gerar_acao_recomendada(faixa: str, tipo_item: str) -> str:
    acoes = {
        "vencido": f"Tratativa IMEDIATA: {tipo_item} vencido. Regularizar antes da próxima atividade operacional.",
        "vence_hoje": f"URGENTE: {tipo_item} vence hoje. Acionar contratada para renovação imediata.",
        "ate_7_dias": f"Acionar empresa contratada para atualização do {tipo_item} e renovação da carteirinha.",
        "ate_15_dias": f"Planejar renovação do {tipo_item} junto à empresa contratada.",
        "ate_30_dias": f"Agendar renovação do {tipo_item}. Prazo confortável para regularização.",
        "ate_60_dias": f"Monitorar vencimento do {tipo_item}. Sem urgência imediata.",
        "sem_risco": f"{tipo_item} dentro da validade. Nenhuma ação necessária no momento.",
    }
    return acoes.get(faixa, "Verificar situação.")


def gerar_responsavel(faixa: str, contrato: Contrato) -> str:
    fiscal = contrato.fiscal_contrato or "Fiscal do contrato"
    gestor = contrato.gestor_contrato or "Gestor do contrato"

    if faixa in ("vencido", "vence_hoje"):
        return f"{fiscal} / RH da contratada / SMS"
    elif faixa in ("ate_7_dias", "ate_15_dias"):
        return f"{fiscal} / SMS / {gestor}"
    else:
        return f"{fiscal} / Gestor da unidade"


def processar_vencimentos(db: Session) -> ExecucaoProcessamento:
    """
    Processa todos os funcionários com contrato vigente,
    verifica vencimentos de requisitos e carteirinhas,
    e gera alertas classificados.
    """
    hoje = date.today()

    # Criar registro de execução
    execucao = ExecucaoProcessamento(
        data_execucao=datetime.now(),
        status="processando"
    )
    db.add(execucao)
    db.flush()

    # Limpar alertas anteriores não resolvidos
    db.query(Alerta).filter(Alerta.resolvido == False).delete()

    # Buscar funcionários com contrato vigente
    funcionarios = (
        db.query(Funcionario)
        .join(Contrato)
        .filter(Contrato.status == "vigente")
        .filter(Funcionario.ativo == True)
        .all()
    )

    contadores = {
        "total": 0, "criticos": 0, "altos": 0,
        "medios": 0, "baixos": 0, "ok": 0, "inconsistencias": 0
    }

    for func in funcionarios:
        contrato = func.contrato

        # Processar requisitos do funcionário
        func_reqs = (
            db.query(FuncionarioRequisito)
            .join(Requisito)
            .filter(FuncionarioRequisito.funcionario_id == func.id)
            .all()
        )

        for fr in func_reqs:
            requisito = fr.requisito

            # Verificar inconsistência
            if fr.data_vencimento is None:
                alerta = Alerta(
                    funcionario_id=func.id,
                    tipo_item=requisito.categoria or "OUTRO",
                    item_descricao=f"{requisito.nome} - INCONSISTÊNCIA CADASTRAL",
                    data_vencimento=None,
                    dias_restantes=None,
                    faixa_vencimento="sem_risco",
                    criticidade="media",
                    acao_recomendada="Inconsistência cadastral detectada: data de vencimento ausente. Corrigir cadastro.",
                    responsavel_sugerido="Administrador do sistema / RH da contratada",
                    execucao_id=execucao.id
                )
                db.add(alerta)
                contadores["total"] += 1
                contadores["inconsistencias"] += 1
                continue

            faixa, criticidade, dias = classificar_vencimento(fr.data_vencimento, hoje)

            if faixa != "sem_risco":
                alerta = Alerta(
                    funcionario_id=func.id,
                    tipo_item=requisito.categoria or "OUTRO",
                    item_descricao=requisito.nome,
                    data_vencimento=fr.data_vencimento,
                    dias_restantes=dias,
                    faixa_vencimento=faixa,
                    criticidade=criticidade,
                    acao_recomendada=gerar_acao_recomendada(faixa, requisito.nome),
                    responsavel_sugerido=gerar_responsavel(faixa, contrato),
                    execucao_id=execucao.id
                )
                db.add(alerta)
                contadores["total"] += 1

                if criticidade == "critica":
                    contadores["criticos"] += 1
                elif criticidade == "alta":
                    contadores["altos"] += 1
                elif criticidade == "media":
                    contadores["medios"] += 1
                elif criticidade == "baixa":
                    contadores["baixos"] += 1
            else:
                contadores["ok"] += 1

        # Processar carteirinhas
        carteirinhas = (
            db.query(Carteirinha)
            .filter(Carteirinha.funcionario_id == func.id)
            .all()
        )

        for cart in carteirinhas:
            faixa, criticidade, dias = classificar_vencimento(cart.data_vencimento, hoje)

            if faixa != "sem_risco":
                alerta = Alerta(
                    funcionario_id=func.id,
                    tipo_item="CARTEIRINHA",
                    item_descricao=f"Carteirinha {cart.numero_carteirinha}",
                    data_vencimento=cart.data_vencimento,
                    dias_restantes=dias,
                    faixa_vencimento=faixa,
                    criticidade=criticidade,
                    acao_recomendada=gerar_acao_recomendada(faixa, "Carteirinha"),
                    responsavel_sugerido=gerar_responsavel(faixa, contrato),
                    execucao_id=execucao.id
                )
                db.add(alerta)
                contadores["total"] += 1

                if criticidade == "critica":
                    contadores["criticos"] += 1
                elif criticidade == "alta":
                    contadores["altos"] += 1
                elif criticidade == "media":
                    contadores["medios"] += 1
                elif criticidade == "baixa":
                    contadores["baixos"] += 1
            else:
                contadores["ok"] += 1

    # Atualizar execução
    execucao.total_registros = contadores["total"]
    execucao.total_criticos = contadores["criticos"]
    execucao.total_altos = contadores["altos"]
    execucao.total_medios = contadores["medios"]
    execucao.total_baixos = contadores["baixos"]
    execucao.total_ok = contadores["ok"]
    execucao.total_inconsistencias = contadores["inconsistencias"]
    execucao.status = "concluido"

    db.commit()
    db.refresh(execucao)
    return execucao
