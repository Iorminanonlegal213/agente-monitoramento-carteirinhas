from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case, distinct
from typing import Optional, List
from datetime import date

from app.database import get_db
from app.models import (
    EmpresaContratada, Contrato, Funcionario, Requisito,
    FuncionarioRequisito, Carteirinha, Alerta, ExecucaoProcessamento
)
from app.schemas import (
    EmpresaOut, ContratoOut, RequisitoOut, FuncionarioOut,
    FuncionarioDetalhadoOut, AlertaOut, ResumoExecutivo,
    ConsolidacaoEmpresa, ConsolidacaoUnidade, ConsolidacaoContrato,
    ProcessamentoOut
)
from app.services.processamento import processar_vencimentos

router = APIRouter()


# === EMPRESAS ===
@router.get("/empresas", response_model=List[EmpresaOut], tags=["Empresas"])
def listar_empresas(db: Session = Depends(get_db)):
    return db.query(EmpresaContratada).filter(EmpresaContratada.ativo == True).all()


# === CONTRATOS ===
@router.get("/contratos", response_model=List[ContratoOut], tags=["Contratos"])
def listar_contratos(
    status: Optional[str] = None,
    empresa_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    q = db.query(Contrato)
    if status:
        q = q.filter(Contrato.status == status)
    if empresa_id:
        q = q.filter(Contrato.empresa_id == empresa_id)
    return q.all()


# === REQUISITOS ===
@router.get("/requisitos", response_model=List[RequisitoOut], tags=["Requisitos"])
def listar_requisitos(db: Session = Depends(get_db)):
    return db.query(Requisito).all()


# === FUNCIONÁRIOS ===
@router.get("/funcionarios", tags=["Funcionários"])
def listar_funcionarios(
    empresa_id: Optional[int] = None,
    contrato_id: Optional[int] = None,
    ativo: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    q = (
        db.query(
            Funcionario,
            EmpresaContratada.razao_social.label("empresa_nome"),
            Contrato.numero_contrato.label("contrato_numero"),
            Contrato.unidade.label("contrato_unidade"),
            Contrato.status.label("contrato_status"),
        )
        .join(EmpresaContratada)
        .join(Contrato)
    )
    if empresa_id:
        q = q.filter(Funcionario.empresa_id == empresa_id)
    if contrato_id:
        q = q.filter(Funcionario.contrato_id == contrato_id)
    if ativo is not None:
        q = q.filter(Funcionario.ativo == ativo)

    results = []
    for f, emp_nome, ctr_num, ctr_uni, ctr_st in q.all():
        results.append({
            "id": f.id, "nome": f.nome, "cpf": f.cpf, "cargo": f.cargo,
            "empresa_id": f.empresa_id, "contrato_id": f.contrato_id,
            "matricula": f.matricula, "ativo": f.ativo,
            "empresa_nome": emp_nome, "contrato_numero": ctr_num,
            "contrato_unidade": ctr_uni, "contrato_status": ctr_st,
        })
    return results


@router.get("/funcionarios/{funcionario_id}/requisitos", tags=["Funcionários"])
def requisitos_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    func = db.query(Funcionario).get(funcionario_id)
    if not func:
        raise HTTPException(404, "Funcionário não encontrado")

    reqs = (
        db.query(FuncionarioRequisito, Requisito)
        .join(Requisito)
        .filter(FuncionarioRequisito.funcionario_id == funcionario_id)
        .all()
    )

    results = []
    hoje = date.today()
    for fr, req in reqs:
        dias = (fr.data_vencimento - hoje).days if fr.data_vencimento else None
        results.append({
            "id": fr.id,
            "requisito_nome": req.nome,
            "requisito_codigo": req.codigo,
            "categoria": req.categoria,
            "data_emissao": fr.data_emissao,
            "data_vencimento": fr.data_vencimento,
            "dias_restantes": dias,
            "numero_documento": fr.numero_documento,
            "inconsistencia": fr.data_vencimento is None,
        })
    return results


# === ALERTAS ===
@router.get("/alertas", tags=["Alertas"])
def listar_alertas(
    criticidade: Optional[str] = None,
    faixa: Optional[str] = None,
    empresa_id: Optional[int] = None,
    contrato_id: Optional[int] = None,
    unidade: Optional[str] = None,
    tipo_item: Optional[str] = None,
    resolvido: Optional[bool] = False,
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    q = (
        db.query(
            Alerta,
            Funcionario.nome.label("func_nome"),
            EmpresaContratada.razao_social.label("emp_nome"),
            Contrato.numero_contrato.label("ctr_num"),
            Contrato.unidade.label("ctr_uni"),
            Contrato.status.label("ctr_st"),
        )
        .select_from(Alerta)
        .join(Funcionario, Alerta.funcionario_id == Funcionario.id)
        .join(EmpresaContratada, Funcionario.empresa_id == EmpresaContratada.id)
        .join(Contrato, Funcionario.contrato_id == Contrato.id)
    )

    if criticidade:
        q = q.filter(Alerta.criticidade == criticidade)
    if faixa:
        q = q.filter(Alerta.faixa_vencimento == faixa)
    if empresa_id:
        q = q.filter(Funcionario.empresa_id == empresa_id)
    if contrato_id:
        q = q.filter(Funcionario.contrato_id == contrato_id)
    if unidade:
        q = q.filter(Contrato.unidade == unidade)
    if tipo_item:
        q = q.filter(Alerta.tipo_item == tipo_item)
    if resolvido is not None:
        q = q.filter(Alerta.resolvido == resolvido)

    # Ordenar por criticidade
    criticidade_order = case(
        (Alerta.criticidade == "critica", 1),
        (Alerta.criticidade == "alta", 2),
        (Alerta.criticidade == "media", 3),
        (Alerta.criticidade == "baixa", 4),
        else_=5
    )
    q = q.order_by(criticidade_order, Alerta.dias_restantes)

    # Contar total separadamente para evitar problema de subquery
    count_q = (
        db.query(func.count(Alerta.id))
        .select_from(Alerta)
        .join(Funcionario, Alerta.funcionario_id == Funcionario.id)
        .join(EmpresaContratada, Funcionario.empresa_id == EmpresaContratada.id)
        .join(Contrato, Funcionario.contrato_id == Contrato.id)
    )
    if criticidade:
        count_q = count_q.filter(Alerta.criticidade == criticidade)
    if faixa:
        count_q = count_q.filter(Alerta.faixa_vencimento == faixa)
    if empresa_id:
        count_q = count_q.filter(Funcionario.empresa_id == empresa_id)
    if contrato_id:
        count_q = count_q.filter(Funcionario.contrato_id == contrato_id)
    if unidade:
        count_q = count_q.filter(Contrato.unidade == unidade)
    if tipo_item:
        count_q = count_q.filter(Alerta.tipo_item == tipo_item)
    if resolvido is not None:
        count_q = count_q.filter(Alerta.resolvido == resolvido)
    total = count_q.scalar()

    rows = q.offset(offset).limit(limit).all()

    alertas = []
    for a, fn, en, cn, cu, cs in rows:
        alertas.append({
            "id": a.id, "funcionario_id": a.funcionario_id,
            "funcionario_nome": fn, "empresa_nome": en,
            "contrato_numero": cn, "unidade": cu, "contrato_status": cs,
            "tipo_item": a.tipo_item, "item_descricao": a.item_descricao,
            "data_vencimento": a.data_vencimento.isoformat() if a.data_vencimento else None,
            "dias_restantes": a.dias_restantes,
            "faixa_vencimento": a.faixa_vencimento,
            "criticidade": a.criticidade,
            "acao_recomendada": a.acao_recomendada,
            "responsavel_sugerido": a.responsavel_sugerido,
            "resolvido": a.resolvido,
            "criado_em": a.criado_em.isoformat() if a.criado_em else None,
        })
    return {"total": total, "alertas": alertas}


@router.get("/alertas/criticos", tags=["Alertas"])
def alertas_criticos(db: Session = Depends(get_db)):
    return listar_alertas(criticidade="critica", db=db)


# === RESUMO EXECUTIVO ===
@router.get("/resumo", response_model=ResumoExecutivo, tags=["Resumo"])
def resumo_executivo(db: Session = Depends(get_db)):
    alertas = db.query(Alerta).filter(Alerta.resolvido == False).all()

    criticos = sum(1 for a in alertas if a.criticidade == "critica")
    altos = sum(1 for a in alertas if a.criticidade == "alta")
    medios = sum(1 for a in alertas if a.criticidade == "media")
    baixos = sum(1 for a in alertas if a.criticidade == "baixa")
    oks = sum(1 for a in alertas if a.criticidade == "ok")
    inconsistencias = sum(1 for a in alertas if "INCONSISTÊNCIA" in (a.item_descricao or ""))

    func_ids = set(a.funcionario_id for a in alertas)
    emp_ids = set()
    for fid in func_ids:
        f = db.query(Funcionario).get(fid)
        if f:
            emp_ids.add(f.empresa_id)

    # Por faixa
    faixas = {}
    for a in alertas:
        faixas[a.faixa_vencimento] = faixas.get(a.faixa_vencimento, 0) + 1

    # Por empresa
    emp_map = {}
    for a in alertas:
        f = db.query(Funcionario).get(a.funcionario_id)
        if f:
            e = db.query(EmpresaContratada).get(f.empresa_id)
            if e:
                key = e.razao_social
                if key not in emp_map:
                    emp_map[key] = {"empresa": key, "total": 0, "criticos": 0}
                emp_map[key]["total"] += 1
                if a.criticidade == "critica":
                    emp_map[key]["criticos"] += 1

    # Por unidade
    uni_map = {}
    for a in alertas:
        f = db.query(Funcionario).get(a.funcionario_id)
        if f:
            c = db.query(Contrato).get(f.contrato_id)
            if c:
                key = c.unidade
                if key not in uni_map:
                    uni_map[key] = {"unidade": key, "total": 0, "criticos": 0}
                uni_map[key]["total"] += 1
                if a.criticidade == "critica":
                    uni_map[key]["criticos"] += 1

    ultima = db.query(ExecucaoProcessamento).order_by(
        ExecucaoProcessamento.id.desc()
    ).first()

    return ResumoExecutivo(
        total_alertas=len(alertas),
        total_criticos=criticos,
        total_altos=altos,
        total_medios=medios,
        total_baixos=baixos,
        total_ok=oks,
        total_inconsistencias=inconsistencias,
        total_funcionarios_afetados=len(func_ids),
        total_empresas_afetadas=len(emp_ids),
        data_processamento=ultima.data_execucao if ultima else None,
        alertas_por_faixa=faixas,
        alertas_por_empresa=sorted(emp_map.values(), key=lambda x: x["total"], reverse=True),
        alertas_por_unidade=sorted(uni_map.values(), key=lambda x: x["total"], reverse=True),
    )


# === CONSOLIDAÇÕES ===
@router.get("/consolidacao/empresas", tags=["Consolidação"])
def consolidar_empresas(db: Session = Depends(get_db)):
    results = (
        db.query(
            EmpresaContratada.id,
            EmpresaContratada.razao_social,
            func.count(Alerta.id).label("total"),
            func.sum(case((Alerta.criticidade == "critica", 1), else_=0)).label("criticos"),
            func.sum(case((Alerta.criticidade == "alta", 1), else_=0)).label("altos"),
            func.sum(case((Alerta.criticidade == "media", 1), else_=0)).label("medios"),
            func.sum(case((Alerta.criticidade == "baixa", 1), else_=0)).label("baixos"),
        )
        .join(Funcionario, Funcionario.empresa_id == EmpresaContratada.id)
        .join(Alerta, Alerta.funcionario_id == Funcionario.id)
        .filter(Alerta.resolvido == False)
        .group_by(EmpresaContratada.id, EmpresaContratada.razao_social)
        .order_by(func.count(Alerta.id).desc())
        .all()
    )
    return [
        {"empresa_id": r[0], "empresa_nome": r[1], "total_alertas": r[2],
         "criticos": r[3] or 0, "altos": r[4] or 0, "medios": r[5] or 0, "baixos": r[6] or 0}
        for r in results
    ]


@router.get("/consolidacao/unidades", tags=["Consolidação"])
def consolidar_unidades(db: Session = Depends(get_db)):
    results = (
        db.query(
            Contrato.unidade,
            func.count(Alerta.id).label("total"),
            func.sum(case((Alerta.criticidade == "critica", 1), else_=0)).label("criticos"),
            func.sum(case((Alerta.criticidade == "alta", 1), else_=0)).label("altos"),
            func.sum(case((Alerta.criticidade == "media", 1), else_=0)).label("medios"),
            func.sum(case((Alerta.criticidade == "baixa", 1), else_=0)).label("baixos"),
        )
        .join(Funcionario, Funcionario.contrato_id == Contrato.id)
        .join(Alerta, Alerta.funcionario_id == Funcionario.id)
        .filter(Alerta.resolvido == False)
        .group_by(Contrato.unidade)
        .order_by(func.count(Alerta.id).desc())
        .all()
    )
    return [
        {"unidade": r[0], "total_alertas": r[1],
         "criticos": r[2] or 0, "altos": r[3] or 0, "medios": r[4] or 0, "baixos": r[5] or 0}
        for r in results
    ]


@router.get("/consolidacao/contratos", tags=["Consolidação"])
def consolidar_contratos(db: Session = Depends(get_db)):
    results = (
        db.query(
            Contrato.id,
            Contrato.numero_contrato,
            EmpresaContratada.razao_social,
            Contrato.unidade,
            func.count(Alerta.id).label("total"),
            func.sum(case((Alerta.criticidade == "critica", 1), else_=0)).label("criticos"),
            func.sum(case((Alerta.criticidade == "alta", 1), else_=0)).label("altos"),
            func.sum(case((Alerta.criticidade == "media", 1), else_=0)).label("medios"),
            func.sum(case((Alerta.criticidade == "baixa", 1), else_=0)).label("baixos"),
        )
        .join(Funcionario, Funcionario.contrato_id == Contrato.id)
        .join(EmpresaContratada, Contrato.empresa_id == EmpresaContratada.id)
        .join(Alerta, Alerta.funcionario_id == Funcionario.id)
        .filter(Alerta.resolvido == False)
        .group_by(Contrato.id, Contrato.numero_contrato, EmpresaContratada.razao_social, Contrato.unidade)
        .order_by(func.count(Alerta.id).desc())
        .all()
    )
    return [
        {"contrato_id": r[0], "contrato_numero": r[1], "empresa_nome": r[2],
         "unidade": r[3], "total_alertas": r[4],
         "criticos": r[5] or 0, "altos": r[6] or 0, "medios": r[7] or 0, "baixos": r[8] or 0}
        for r in results
    ]


# === PROCESSAMENTO ===
@router.post("/processar", tags=["Processamento"])
def reprocessar(db: Session = Depends(get_db)):
    execucao = processar_vencimentos(db)
    return {
        "mensagem": "Processamento concluído com sucesso",
        "execucao_id": execucao.id,
        "total_registros": execucao.total_registros,
        "total_criticos": execucao.total_criticos,
        "total_altos": execucao.total_altos,
        "total_medios": execucao.total_medios,
        "total_baixos": execucao.total_baixos,
        "total_ok": execucao.total_ok,
        "total_inconsistencias": execucao.total_inconsistencias,
    }


@router.get("/processamentos", tags=["Processamento"])
def listar_processamentos(db: Session = Depends(get_db)):
    return db.query(ExecucaoProcessamento).order_by(
        ExecucaoProcessamento.id.desc()
    ).limit(20).all()


# === FILTROS (dados para dropdowns) ===
@router.get("/filtros/unidades", tags=["Filtros"])
def listar_unidades(db: Session = Depends(get_db)):
    results = db.query(distinct(Contrato.unidade)).filter(Contrato.status == "vigente").all()
    return [r[0] for r in results]


@router.get("/filtros/tipos-requisito", tags=["Filtros"])
def listar_tipos_requisito(db: Session = Depends(get_db)):
    results = db.query(distinct(Requisito.categoria)).all()
    return [r[0] for r in results if r[0]]
