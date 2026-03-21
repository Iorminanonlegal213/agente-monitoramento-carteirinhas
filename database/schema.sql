-- =============================================================================
-- Agente de Monitoramento Preventivo de Carteirinhas
-- Schema PostgreSQL
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Empresas Contratadas
CREATE TABLE empresas_contratadas (
    id SERIAL PRIMARY KEY,
    razao_social VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    contato_nome VARCHAR(150),
    contato_email VARCHAR(200),
    contato_telefone VARCHAR(20),
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

-- Contratos
CREATE TABLE contratos (
    id SERIAL PRIMARY KEY,
    numero_contrato VARCHAR(50) UNIQUE NOT NULL,
    empresa_id INTEGER NOT NULL REFERENCES empresas_contratadas(id),
    objeto TEXT,
    unidade VARCHAR(150) NOT NULL,
    gestor_contrato VARCHAR(150),
    fiscal_contrato VARCHAR(150),
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'vigente' CHECK (status IN ('vigente', 'encerrado', 'suspenso')),
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_contratos_empresa ON contratos(empresa_id);
CREATE INDEX idx_contratos_status ON contratos(status);
CREATE INDEX idx_contratos_unidade ON contratos(unidade);

-- Funcionários
CREATE TABLE funcionarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    cargo VARCHAR(100),
    empresa_id INTEGER NOT NULL REFERENCES empresas_contratadas(id),
    contrato_id INTEGER NOT NULL REFERENCES contratos(id),
    matricula VARCHAR(50),
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_funcionarios_empresa ON funcionarios(empresa_id);
CREATE INDEX idx_funcionarios_contrato ON funcionarios(contrato_id);

-- Requisitos (tipos de documentos/certificações)
CREATE TABLE requisitos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50) CHECK (categoria IN ('NR', 'ASO', 'CNH', 'CURSO', 'CARTEIRINHA', 'OUTRO')),
    validade_meses INTEGER,
    obrigatorio BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT NOW()
);

-- Funcionário x Requisitos (vencimentos individuais)
CREATE TABLE funcionario_requisitos (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER NOT NULL REFERENCES funcionarios(id),
    requisito_id INTEGER NOT NULL REFERENCES requisitos(id),
    data_emissao DATE,
    data_vencimento DATE,
    numero_documento VARCHAR(100),
    observacao TEXT,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW(),
    UNIQUE(funcionario_id, requisito_id)
);

CREATE INDEX idx_func_req_funcionario ON funcionario_requisitos(funcionario_id);
CREATE INDEX idx_func_req_vencimento ON funcionario_requisitos(data_vencimento);

-- Carteirinhas
CREATE TABLE carteirinhas (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER NOT NULL REFERENCES funcionarios(id),
    numero_carteirinha VARCHAR(50) UNIQUE NOT NULL,
    data_emissao DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'ativa' CHECK (status IN ('ativa', 'vencida', 'suspensa', 'cancelada')),
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_carteirinhas_funcionario ON carteirinhas(funcionario_id);
CREATE INDEX idx_carteirinhas_vencimento ON carteirinhas(data_vencimento);

-- Alertas
CREATE TABLE alertas (
    id SERIAL PRIMARY KEY,
    funcionario_id INTEGER NOT NULL REFERENCES funcionarios(id),
    tipo_item VARCHAR(50) NOT NULL,
    item_descricao VARCHAR(200) NOT NULL,
    data_vencimento DATE,
    dias_restantes INTEGER,
    faixa_vencimento VARCHAR(30) NOT NULL CHECK (faixa_vencimento IN (
        'vencido', 'vence_hoje', 'ate_7_dias', 'ate_15_dias', 'ate_30_dias', 'ate_60_dias', 'sem_risco'
    )),
    criticidade VARCHAR(10) NOT NULL CHECK (criticidade IN ('critica', 'alta', 'media', 'baixa', 'ok')),
    acao_recomendada TEXT,
    responsavel_sugerido VARCHAR(200),
    resolvido BOOLEAN DEFAULT FALSE,
    execucao_id INTEGER,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_alertas_funcionario ON alertas(funcionario_id);
CREATE INDEX idx_alertas_criticidade ON alertas(criticidade);
CREATE INDEX idx_alertas_faixa ON alertas(faixa_vencimento);
CREATE INDEX idx_alertas_resolvido ON alertas(resolvido);

-- Execuções de Processamento
CREATE TABLE execucoes_processamento (
    id SERIAL PRIMARY KEY,
    data_execucao TIMESTAMP DEFAULT NOW(),
    total_registros INTEGER DEFAULT 0,
    total_criticos INTEGER DEFAULT 0,
    total_altos INTEGER DEFAULT 0,
    total_medios INTEGER DEFAULT 0,
    total_baixos INTEGER DEFAULT 0,
    total_ok INTEGER DEFAULT 0,
    total_inconsistencias INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'concluido',
    observacao TEXT,
    criado_em TIMESTAMP DEFAULT NOW()
);

-- Adicionar FK de execucao nos alertas
ALTER TABLE alertas ADD CONSTRAINT fk_alertas_execucao
    FOREIGN KEY (execucao_id) REFERENCES execucoes_processamento(id);
