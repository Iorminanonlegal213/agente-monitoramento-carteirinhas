from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List


# === Empresa ===
class EmpresaBase(BaseModel):
    razao_social: str
    cnpj: str
    contato_nome: Optional[str] = None
    contato_email: Optional[str] = None
    contato_telefone: Optional[str] = None

class EmpresaOut(EmpresaBase):
    id: int
    ativo: bool
    class Config:
        from_attributes = True


# === Contrato ===
class ContratoBase(BaseModel):
    numero_contrato: str
    empresa_id: int
    objeto: Optional[str] = None
    unidade: str
    gestor_contrato: Optional[str] = None
    fiscal_contrato: Optional[str] = None
    data_inicio: date
    data_fim: date
    status: str = "vigente"

class ContratoOut(ContratoBase):
    id: int
    class Config:
        from_attributes = True


# === Requisito ===
class RequisitoOut(BaseModel):
    id: int
    nome: str
    codigo: str
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    validade_meses: Optional[int] = None
    obrigatorio: bool
    class Config:
        from_attributes = True


# === Funcionario ===
class FuncionarioOut(BaseModel):
    id: int
    nome: str
    cpf: str
    cargo: Optional[str] = None
    empresa_id: int
    contrato_id: int
    matricula: Optional[str] = None
    ativo: bool
    class Config:
        from_attributes = True

class FuncionarioDetalhadoOut(FuncionarioOut):
    empresa_nome: Optional[str] = None
    contrato_numero: Optional[str] = None
    contrato_unidade: Optional[str] = None
    contrato_status: Optional[str] = None


# === Alerta ===
class AlertaOut(BaseModel):
    id: int
    funcionario_id: int
    funcionario_nome: Optional[str] = None
    empresa_nome: Optional[str] = None
    contrato_numero: Optional[str] = None
    unidade: Optional[str] = None
    contrato_status: Optional[str] = None
    tipo_item: str
    item_descricao: str
    data_vencimento: Optional[date] = None
    dias_restantes: Optional[int] = None
    faixa_vencimento: str
    criticidade: str
    acao_recomendada: Optional[str] = None
    responsavel_sugerido: Optional[str] = None
    resolvido: bool = False
    criado_em: Optional[datetime] = None
    class Config:
        from_attributes = True


# === Resumo Executivo ===
class ResumoExecutivo(BaseModel):
    total_alertas: int
    total_criticos: int
    total_altos: int
    total_medios: int
    total_baixos: int
    total_ok: int
    total_inconsistencias: int
    total_funcionarios_afetados: int
    total_empresas_afetadas: int
    data_processamento: Optional[datetime] = None
    alertas_por_faixa: dict
    alertas_por_empresa: List[dict]
    alertas_por_unidade: List[dict]


# === Consolidação ===
class ConsolidacaoEmpresa(BaseModel):
    empresa_id: int
    empresa_nome: str
    total_alertas: int
    criticos: int
    altos: int
    medios: int
    baixos: int

class ConsolidacaoUnidade(BaseModel):
    unidade: str
    total_alertas: int
    criticos: int
    altos: int
    medios: int
    baixos: int

class ConsolidacaoContrato(BaseModel):
    contrato_id: int
    contrato_numero: str
    empresa_nome: str
    unidade: str
    total_alertas: int
    criticos: int
    altos: int
    medios: int
    baixos: int


# === Processamento ===
class ProcessamentoOut(BaseModel):
    id: int
    data_execucao: datetime
    total_registros: int
    total_criticos: int
    total_altos: int
    total_medios: int
    total_baixos: int
    total_ok: int
    total_inconsistencias: int
    status: str
    class Config:
        from_attributes = True
