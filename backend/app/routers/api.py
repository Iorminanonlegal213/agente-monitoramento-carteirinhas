from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case, distinct, text
from typing import Optional, List
from datetime import date

from app.database import get_db
from app.models import (
    EmpresaContratada, Contrato, Funcionario, Requisito,
    FuncionarioRequisito, Carteirinha, Alerta, ExecucaoProcessamento
)
from app.schemas import (
    EmpresaOut, ContratoOut, RequisitoOut,
    ResumoExecutivo, ProcessamentoOut
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
    """Lista funcionários com dados da empresa e contrato via SQL puro para evitar ambiguidade."""
    sql = text("""
        SELECT
            f.id, f.nome, f.cpf, f.cargo, f.empresa_id, f.contrato_id,
            f.matricula, f.ativo,
            e.razao_social as empresa_nome,
            c.numero_contrato as contrato_numero,
            c.unidade as contrato_unidade,
            c.status as contrato_status
        FROM funcionarios f
        JOIN empresas_contratadas e ON f.empresa_id = e.id
        JOIN contratos c ON f.contrato_id = c.id
        WHERE (:empresa_id IS NULL OR f.empresa_id = :empresa_id)
          AND (:contrato_id IS NULL OR f.contrato_id = :contrato_id)
          AND (:ativo IS NULL OR f.ativo = :ativo)
        ORDER BY f.nome
    """)

    rows = db.execute(sql, {
        "empresa_id": empresa_id,
        "contrato_id": contrato_id,
        "ativo": ativo,
    }).mappings().all()

    return [dict(r) for r in rows]


@router.get("/funcionarios/{funcionario_id}/requisitos", tags=["Funcionários"])
def requisitos_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    func_obj = db.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
    if not func_obj:
        raise HTTPException(404, "Funcionário não encontrado")

    sql = text("""
        SELECT
            fr.id, r.nome as requisito_nome, r.codigo as requisito_codigo,
            r.categoria, fr.data_emissao, fr.data_vencimento,
            fr.numero_documento
        FROM funcionario_requisitos fr
        JOIN requisitos r ON fr.requisito_id = r.id
        WHERE fr.funcionario_id = :func_id
        ORDER BY fr.data_vencimento NULLS FIRST
    """)

    rows = db.execute(sql, {"func_id": funcionario_id}).mappings().all()
    hoje = date.today()

    results = []
    for r in rows:
        dias = (r["data_vencimento"] - hoje).days if r["data_vencimento"] else None
        results.append({
            **dict(r),
            "dias_restantes": dias,
            "inconsistencia": r["data_vencimento"] is None,
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
    """Lista alertas com dados do funcionário, empresa e contrato via SQL puro."""

    # Construir WHERE dinâmico
    conditions = []
    params = {"limit_val": limit, "offset_val": offset}

    if resolvido is not None:
        conditions.append("a.resolvido = :resolvido")
        params["resolvido"] = resolvido
    if criticidade:
        conditions.append("a.criticidade = :criticidade")
        params["criticidade"] = criticidade
    if faixa:
        conditions.append("a.faixa_vencimento = :faixa")
        params["faixa"] = faixa
    if empresa_id:
        conditions.append("f.empresa_id = :empresa_id")
        params["empresa_id"] = empresa_id
    if contrato_id:
        conditions.append("f.contrato_id = :contrato_id")
        params["contrato_id"] = contrato_id
    if unidade:
        conditions.append("c.unidade = :unidade")
        params["unidade"] = unidade
    if tipo_item:
        conditions.append("a.tipo_item = :tipo_item")
        params["tipo_item"] = tipo_item

    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Count
    count_sql = text(f"""
        SELECT COUNT(*)
        FROM alertas a
        JOIN funcionarios f ON a.funcionario_id = f.id
        JOIN empresas_contratadas e ON f.empresa_id = e.id
        JOIN contratos c ON f.contrato_id = c.id
        WHERE {where_clause}
    """)
    total = db.execute(count_sql, params).scalar()

    # Data
    data_sql = text(f"""
        SELECT
            a.id, a.funcionario_id, f.nome as funcionario_nome,
            e.razao_social as empresa_nome,
            c.numero_contrato as contrato_numero,
            c.unidade, c.status as contrato_status,
            a.tipo_item, a.item_descricao, a.data_vencimento,
            a.dias_restantes, a.faixa_vencimento, a.criticidade,
            a.acao_recomendada, a.responsavel_sugerido,
            a.resolvido, a.criado_em
        FROM alertas a
        JOIN funcionarios f ON a.funcionario_id = f.id
        JOIN empresas_contratadas e ON f.empresa_id = e.id
        JOIN contratos c ON f.contrato_id = c.id
        WHERE {where_clause}
        ORDER BY
            CASE a.criticidade
                WHEN 'critica' THEN 1
                WHEN 'alta' THEN 2
                WHEN 'media' THEN 3
                WHEN 'baixa' THEN 4
                ELSE 5
            END,
            a.dias_restantes NULLS LAST
        LIMIT :limit_val OFFSET :offset_val
    """)

    rows = db.execute(data_sql, params).mappings().all()

    alertas = []
    for r in rows:
        alertas.append({
            "id": r["id"],
            "funcionario_id": r["funcionario_id"],
            "funcionario_nome": r["funcionario_nome"],
            "empresa_nome": r["empresa_nome"],
            "contrato_numero": r["contrato_numero"],
            "unidade": r["unidade"],
            "contrato_status": r["contrato_status"],
            "tipo_item": r["tipo_item"],
            "item_descricao": r["item_descricao"],
            "data_vencimento": r["data_vencimento"].isoformat() if r["data_vencimento"] else None,
            "dias_restantes": r["dias_restantes"],
            "faixa_vencimento": r["faixa_vencimento"],
            "criticidade": r["criticidade"],
            "acao_recomendada": r["acao_recomendada"],
            "responsavel_sugerido": r["responsavel_sugerido"],
            "resolvido": r["resolvido"],
            "criado_em": r["criado_em"].isoformat() if r["criado_em"] else None,
        })

    return {"total": total, "alertas": alertas}


@router.get("/alertas/criticos", tags=["Alertas"])
def alertas_criticos(db: Session = Depends(get_db)):
    return listar_alertas(criticidade="critica", db=db)


# === RESUMO EXECUTIVO ===
@router.get("/resumo", response_model=ResumoExecutivo, tags=["Resumo"])
def resumo_executivo(db: Session = Depends(get_db)):
    # Contagens por criticidade
    stats = db.execute(text("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN criticidade = 'critica' THEN 1 ELSE 0 END) as criticos,
            SUM(CASE WHEN criticidade = 'alta' THEN 1 ELSE 0 END) as altos,
            SUM(CASE WHEN criticidade = 'media' THEN 1 ELSE 0 END) as medios,
            SUM(CASE WHEN criticidade = 'baixa' THEN 1 ELSE 0 END) as baixos,
            SUM(CASE WHEN criticidade = 'ok' THEN 1 ELSE 0 END) as oks,
            SUM(CASE WHEN item_descricao LIKE '%INCONSISTÊNCIA%' THEN 1 ELSE 0 END) as inconsistencias,
            COUNT(DISTINCT funcionario_id) as funcionarios_afetados
        FROM alertas
        WHERE resolvido = false
    """)).mappings().first()

    # Empresas afetadas
    emp_count = db.execute(text("""
        SELECT COUNT(DISTINCT f.empresa_id)
        FROM alertas a
        JOIN funcionarios f ON a.funcionario_id = f.id
        WHERE a.resolvido = false
    """)).scalar()

    # Por faixa
    faixas_rows = db.execute(text("""
        SELECT faixa_vencimento, COUNT(*) as cnt
        FROM alertas WHERE resolvido = false
        GROUP BY faixa_vencimento
    """)).mappings().all()
    faixas = {r["faixa_vencimento"]: r["cnt"] for r in faixas_rows}

    # Por empresa
    emp_rows = db.execute(text("""
        SELECT e.razao_social as empresa, COUNT(*) as total,
            SUM(CASE WHEN a.criticidade = 'critica' THEN 1 ELSE 0 END) as criticos
        FROM alertas a
        JOIN funcionarios f ON a.funcionario_id = f.id
        JOIN empresas_contratadas e ON f.empresa_id = e.id
        WHERE a.resolvido = false
        GROUP BY e.razao_social
        ORDER BY total DESC
    """)).mappings().all()

    # Por unidade
    uni_rows = db.execute(text("""
        SELECT c.unidade, COUNT(*) as total,
            SUM(CASE WHEN a.criticidade = 'critica' THEN 1 ELSE 0 END) as criticos
        FROM alertas a
        JOIN funcionarios f ON a.funcionario_id = f.id
        JOIN contratos c ON f.contrato_id = c.id
        WHERE a.resolvido = false
        GROUP BY c.unidade
        ORDER BY total DESC
    """)).mappings().all()

    ultima = db.query(ExecucaoProcessamento).order_by(
        ExecucaoProcessamento.id.desc()
    ).first()

    return ResumoExecutivo(
        total_alertas=stats["total"] or 0,
        total_criticos=stats["criticos"] or 0,
        total_altos=stats["altos"] or 0,
        total_medios=stats["medios"] or 0,
        total_baixos=stats["baixos"] or 0,
        total_ok=stats["oks"] or 0,
        total_inconsistencias=stats["inconsistencias"] or 0,
        total_funcionarios_afetados=stats["funcionarios_afetados"] or 0,
        total_empresas_afetadas=emp_count or 0,
        data_processamento=ultima.data_execucao if ultima else None,
        alertas_por_faixa=faixas,
        alertas_por_empresa=[dict(r) for r in emp_rows],
        alertas_por_unidade=[dict(r) for r in uni_rows],
    )


# === CONSOLIDAÇÕES ===
@router.get("/consolidacao/empresas", tags=["Consolidação"])
def consolidar_empresas(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT e.id as empresa_id, e.razao_social as empresa_nome,
            COUNT(*) as total_alertas,
            SUM(CASE WHEN a.criticidade = 'critica' THEN 1 ELSE 0 END) as criticos,
            SUM(CASE WHEN a.criticidade = 'alta' THEN 1 ELSE 0 END) as altos,
            SUM(CASE WHEN a.criticidade = 'media' THEN 1 ELSE 0 END) as medios,
            SUM(CASE WHEN a.criticidade = 'baixa' THEN 1 ELSE 0 END) as baixos
        FROM alertas a
        JOIN funcionarios f ON a.funcionario_id = f.id
        JOIN empresas_contratadas e ON f.empresa_id = e.id
        WHERE a.resolvido = false
        GROUP BY e.id, e.razao_social
        ORDER BY total_alertas DESC
    """)).mappings().all()
    return [dict(r) for r in rows]


@router.get("/consolidacao/unidades", tags=["Consolidação"])
def consolidar_unidades(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT c.unidade, COUNT(*) as total_alertas,
            SUM(CASE WHEN a.criticidade = 'critica' THEN 1 ELSE 0 END) as criticos,
            SUM(CASE WHEN a.criticidade = 'alta' THEN 1 ELSE 0 END) as altos,
            SUM(CASE WHEN a.criticidade = 'media' THEN 1 ELSE 0 END) as medios,
            SUM(CASE WHEN a.criticidade = 'baixa' THEN 1 ELSE 0 END) as baixos
        FROM alertas a
        JOIN funcionarios f ON a.funcionario_id = f.id
        JOIN contratos c ON f.contrato_id = c.id
        WHERE a.resolvido = false
        GROUP BY c.unidade
        ORDER BY total_alertas DESC
    """)).mappings().all()
    return [dict(r) for r in rows]


@router.get("/consolidacao/contratos", tags=["Consolidação"])
def consolidar_contratos(db: Session = Depends(get_db)):
    rows = db.execute(text("""
        SELECT c.id as contrato_id, c.numero_contrato, e.razao_social as empresa_nome,
            c.unidade, COUNT(*) as total_alertas,
            SUM(CASE WHEN a.criticidade = 'critica' THEN 1 ELSE 0 END) as criticos,
            SUM(CASE WHEN a.criticidade = 'alta' THEN 1 ELSE 0 END) as altos,
            SUM(CASE WHEN a.criticidade = 'media' THEN 1 ELSE 0 END) as medios,
            SUM(CASE WHEN a.criticidade = 'baixa' THEN 1 ELSE 0 END) as baixos
        FROM alertas a
        JOIN funcionarios f ON a.funcionario_id = f.id
        JOIN contratos c ON f.contrato_id = c.id
        JOIN empresas_contratadas e ON c.empresa_id = e.id
        WHERE a.resolvido = false
        GROUP BY c.id, c.numero_contrato, e.razao_social, c.unidade
        ORDER BY total_alertas DESC
    """)).mappings().all()
    return [dict(r) for r in rows]


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


# === FILTROS ===
@router.get("/filtros/unidades", tags=["Filtros"])
def listar_unidades(db: Session = Depends(get_db)):
    results = db.query(distinct(Contrato.unidade)).filter(Contrato.status == "vigente").all()
    return [r[0] for r in results]


@router.get("/filtros/tipos-requisito", tags=["Filtros"])
def listar_tipos_requisito(db: Session = Depends(get_db)):
    results = db.query(distinct(Requisito.categoria)).all()
    return [r[0] for r in results if r[0]]
