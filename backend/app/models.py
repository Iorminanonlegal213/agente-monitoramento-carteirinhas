from sqlalchemy import (
    Column, Integer, String, Boolean, Date, DateTime, Text, ForeignKey,
    CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class EmpresaContratada(Base):
    __tablename__ = "empresas_contratadas"

    id = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String(255), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=False)
    contato_nome = Column(String(150))
    contato_email = Column(String(200))
    contato_telefone = Column(String(20))
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    contratos = relationship("Contrato", back_populates="empresa")
    funcionarios = relationship("Funcionario", back_populates="empresa")


class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(Integer, primary_key=True, index=True)
    numero_contrato = Column(String(50), unique=True, nullable=False)
    empresa_id = Column(Integer, ForeignKey("empresas_contratadas.id"), nullable=False)
    objeto = Column(Text)
    unidade = Column(String(150), nullable=False)
    gestor_contrato = Column(String(150))
    fiscal_contrato = Column(String(150))
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    status = Column(String(20), default="vigente")
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    empresa = relationship("EmpresaContratada", back_populates="contratos")
    funcionarios = relationship("Funcionario", back_populates="contrato")


class Funcionario(Base):
    __tablename__ = "funcionarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    cargo = Column(String(100))
    empresa_id = Column(Integer, ForeignKey("empresas_contratadas.id"), nullable=False)
    contrato_id = Column(Integer, ForeignKey("contratos.id"), nullable=False)
    matricula = Column(String(50))
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    empresa = relationship("EmpresaContratada", back_populates="funcionarios")
    contrato = relationship("Contrato", back_populates="funcionarios")
    requisitos = relationship("FuncionarioRequisito", back_populates="funcionario")
    carteirinhas = relationship("Carteirinha", back_populates="funcionario")
    alertas = relationship("Alerta", back_populates="funcionario")


class Requisito(Base):
    __tablename__ = "requisitos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    descricao = Column(Text)
    categoria = Column(String(50))
    validade_meses = Column(Integer)
    obrigatorio = Column(Boolean, default=True)
    criado_em = Column(DateTime, server_default=func.now())

    funcionario_requisitos = relationship("FuncionarioRequisito", back_populates="requisito")


class FuncionarioRequisito(Base):
    __tablename__ = "funcionario_requisitos"

    id = Column(Integer, primary_key=True, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    requisito_id = Column(Integer, ForeignKey("requisitos.id"), nullable=False)
    data_emissao = Column(Date)
    data_vencimento = Column(Date)
    numero_documento = Column(String(100))
    observacao = Column(Text)
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    funcionario = relationship("Funcionario", back_populates="requisitos")
    requisito = relationship("Requisito", back_populates="funcionario_requisitos")


class Carteirinha(Base):
    __tablename__ = "carteirinhas"

    id = Column(Integer, primary_key=True, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    numero_carteirinha = Column(String(50), unique=True, nullable=False)
    data_emissao = Column(Date, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    status = Column(String(20), default="ativa")
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    funcionario = relationship("Funcionario", back_populates="carteirinhas")


class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    tipo_item = Column(String(50), nullable=False)
    item_descricao = Column(String(200), nullable=False)
    data_vencimento = Column(Date)
    dias_restantes = Column(Integer)
    faixa_vencimento = Column(String(30), nullable=False)
    criticidade = Column(String(10), nullable=False)
    acao_recomendada = Column(Text)
    responsavel_sugerido = Column(String(200))
    resolvido = Column(Boolean, default=False)
    execucao_id = Column(Integer, ForeignKey("execucoes_processamento.id"))
    criado_em = Column(DateTime, server_default=func.now())
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now())

    funcionario = relationship("Funcionario", back_populates="alertas")
    execucao = relationship("ExecucaoProcessamento", back_populates="alertas")


class ExecucaoProcessamento(Base):
    __tablename__ = "execucoes_processamento"

    id = Column(Integer, primary_key=True, index=True)
    data_execucao = Column(DateTime, server_default=func.now())
    total_registros = Column(Integer, default=0)
    total_criticos = Column(Integer, default=0)
    total_altos = Column(Integer, default=0)
    total_medios = Column(Integer, default=0)
    total_baixos = Column(Integer, default=0)
    total_ok = Column(Integer, default=0)
    total_inconsistencias = Column(Integer, default=0)
    status = Column(String(20), default="concluido")
    observacao = Column(Text)
    criado_em = Column(DateTime, server_default=func.now())

    alertas = relationship("Alerta", back_populates="execucao")
