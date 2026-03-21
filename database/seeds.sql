-- =============================================================================
-- Seeds - Dados fictícios para desenvolvimento e demonstração
-- =============================================================================

-- Empresas Contratadas
INSERT INTO empresas_contratadas (razao_social, cnpj, contato_nome, contato_email, contato_telefone) VALUES
('XYZ Serviços Industriais Ltda', '12.345.678/0001-90', 'Carlos Mendes', 'carlos@xyzservicos.com.br', '(21) 99876-5432'),
('ABC Manutenção e Engenharia S.A.', '23.456.789/0001-01', 'Ana Beatriz', 'ana.beatriz@abcmanut.com.br', '(21) 98765-4321'),
('Delta Facilities Ltda', '34.567.890/0001-12', 'Roberto Lima', 'roberto@deltafacilities.com.br', '(21) 97654-3210'),
('Omega Segurança Patrimonial Ltda', '45.678.901/0001-23', 'Fernanda Costa', 'fernanda@omegaseg.com.br', '(21) 96543-2109'),
('Sol Nascente Limpeza e Conservação', '56.789.012/0001-34', 'José Augusto', 'jose@solnascente.com.br', '(21) 95432-1098');

-- Contratos
INSERT INTO contratos (numero_contrato, empresa_id, objeto, unidade, gestor_contrato, fiscal_contrato, data_inicio, data_fim, status) VALUES
('CTR-2024-001', 1, 'Manutenção Industrial', 'Estação Comprida', 'Paulo Henrique', 'Marcos Vieira', '2024-01-01', '2026-12-31', 'vigente'),
('CTR-2024-002', 2, 'Manutenção Predial', 'Terminal Oceânico', 'Lucia Fernandes', 'Ricardo Alves', '2024-03-01', '2026-06-30', 'vigente'),
('CTR-2024-003', 3, 'Facilities e Apoio', 'Estação Serra', 'Diego Martins', 'Amanda Souza', '2024-06-01', '2026-09-30', 'vigente'),
('CTR-2023-010', 4, 'Vigilância Patrimonial', 'Terminal Baía', 'Renato Oliveira', 'Carla Nunes', '2023-01-01', '2025-12-31', 'vigente'),
('CTR-2023-015', 5, 'Limpeza e Conservação', 'Estação Comprida', 'Paula Santos', 'Jorge Ramos', '2023-06-01', '2025-06-30', 'vigente'),
('CTR-2022-005', 1, 'Manutenção Elétrica', 'Terminal Oceânico', 'Paulo Henrique', 'Marcos Vieira', '2022-01-01', '2024-12-31', 'encerrado');

-- Funcionários
INSERT INTO funcionarios (nome, cpf, cargo, empresa_id, contrato_id, matricula) VALUES
-- XYZ Serviços (contrato vigente CTR-2024-001)
('João da Silva', '111.222.333-44', 'Eletricista Industrial', 1, 1, 'XYZ-001'),
('Pedro Almeida', '222.333.444-55', 'Mecânico Industrial', 1, 1, 'XYZ-002'),
('Lucas Ferreira', '333.444.555-66', 'Técnico de Segurança', 1, 1, 'XYZ-003'),
('Rafael Santos', '444.555.666-77', 'Soldador', 1, 1, 'XYZ-004'),
-- ABC Manutenção (contrato vigente CTR-2024-002)
('Maria Oliveira', '555.666.777-88', 'Engenheira Civil', 2, 2, 'ABC-001'),
('Ana Paula Costa', '666.777.888-99', 'Técnica em Edificações', 2, 2, 'ABC-002'),
('Carlos Eduardo', '777.888.999-00', 'Encanador', 2, 2, 'ABC-003'),
-- Delta Facilities (contrato vigente CTR-2024-003)
('Fernanda Lima', '888.999.000-11', 'Coord. Facilities', 3, 3, 'DLT-001'),
('Roberto Dias', '999.000.111-22', 'Auxiliar de Manutenção', 3, 3, 'DLT-002'),
-- Omega Segurança (contrato vigente CTR-2023-010)
('Marcos Pereira', '100.200.300-40', 'Vigilante', 4, 4, 'OMG-001'),
('Juliana Ramos', '200.300.400-50', 'Vigilante', 4, 4, 'OMG-002'),
('Thiago Nascimento', '300.400.500-60', 'Supervisor de Segurança', 4, 4, 'OMG-003'),
-- Sol Nascente (contrato vigente CTR-2023-015)
('Sandra Martins', '400.500.600-70', 'Auxiliar de Limpeza', 5, 5, 'SN-001'),
('Claudio Barbosa', '500.600.700-80', 'Auxiliar de Limpeza', 5, 5, 'SN-002'),
-- XYZ contrato encerrado
('Antonio Gomes', '600.700.800-90', 'Eletricista', 1, 6, 'XYZ-005');

-- Requisitos
INSERT INTO requisitos (nome, codigo, descricao, categoria, validade_meses, obrigatorio) VALUES
('NR-10 - Segurança em Instalações Elétricas', 'NR10', 'Curso obrigatório para trabalhos com eletricidade', 'NR', 24, TRUE),
('NR-35 - Trabalho em Altura', 'NR35', 'Curso obrigatório para trabalhos acima de 2m', 'NR', 24, TRUE),
('NR-33 - Espaço Confinado', 'NR33', 'Curso obrigatório para trabalho em espaços confinados', 'NR', 12, TRUE),
('ASO - Atestado de Saúde Ocupacional', 'ASO', 'Exame médico admissional/periódico', 'ASO', 12, TRUE),
('CNH - Carteira Nacional de Habilitação', 'CNH', 'Habilitação para condução de veículos', 'CNH', 60, FALSE),
('Curso de Integração SMS', 'INTSMS', 'Integração de segurança, meio ambiente e saúde', 'CURSO', 12, TRUE),
('NR-20 - Inflamáveis e Combustíveis', 'NR20', 'Segurança com inflamáveis e combustíveis', 'NR', 12, TRUE),
('Curso de Primeiros Socorros', 'PRISOC', 'Capacitação em primeiros socorros', 'CURSO', 24, FALSE),
('NR-06 - EPI', 'NR06', 'Treinamento sobre uso de EPI', 'NR', 12, TRUE),
('Curso de Combate a Incêndio', 'INCEND', 'Brigada de incêndio', 'CURSO', 12, FALSE);

-- Funcionário x Requisitos (com datas variadas para gerar alertas)
-- João da Silva (XYZ) - NR-10 vence em 5 dias, ASO vence em 25 dias
INSERT INTO funcionario_requisitos (funcionario_id, requisito_id, data_emissao, data_vencimento, numero_documento) VALUES
(1, 1, '2024-03-26', CURRENT_DATE + INTERVAL '5 days', 'NR10-2024-001'),
(1, 4, '2025-03-26', CURRENT_DATE + INTERVAL '25 days', 'ASO-2025-001'),
(1, 6, '2025-01-15', CURRENT_DATE + INTERVAL '120 days', 'INT-2025-001'),
-- Pedro Almeida (XYZ) - ASO vencido há 3 dias, NR-35 vence em 12 dias
(2, 4, '2024-03-18', CURRENT_DATE - INTERVAL '3 days', 'ASO-2024-002'),
(2, 2, '2024-04-08', CURRENT_DATE + INTERVAL '12 days', 'NR35-2024-002'),
(2, 1, '2025-01-01', CURRENT_DATE + INTERVAL '200 days', 'NR10-2025-002'),
-- Lucas Ferreira (XYZ) - NR-33 vence hoje
(3, 3, '2025-03-21', CURRENT_DATE, 'NR33-2025-003'),
(3, 4, '2025-02-01', CURRENT_DATE + INTERVAL '45 days', 'ASO-2025-003'),
(3, 6, '2025-03-01', CURRENT_DATE + INTERVAL '90 days', 'INT-2025-003'),
-- Rafael Santos (XYZ) - tudo ok
(4, 1, '2025-03-01', CURRENT_DATE + INTERVAL '180 days', 'NR10-2025-004'),
(4, 4, '2025-03-01', CURRENT_DATE + INTERVAL '150 days', 'ASO-2025-004'),
-- Maria Oliveira (ABC) - ASO vence em 3 dias, NR-35 vence em 55 dias
(5, 4, '2024-03-24', CURRENT_DATE + INTERVAL '3 days', 'ASO-2024-005'),
(5, 2, '2024-05-16', CURRENT_DATE + INTERVAL '55 days', 'NR35-2024-005'),
(5, 6, '2025-03-01', CURRENT_DATE + INTERVAL '100 days', 'INT-2025-005'),
-- Ana Paula Costa (ABC) - CNH vencida há 10 dias
(6, 5, '2020-03-11', CURRENT_DATE - INTERVAL '10 days', 'CNH-2020-006'),
(6, 4, '2025-02-01', CURRENT_DATE + INTERVAL '60 days', 'ASO-2025-006'),
-- Carlos Eduardo (ABC) - NR-20 vence em 28 dias
(7, 7, '2025-04-19', CURRENT_DATE + INTERVAL '28 days', 'NR20-2025-007'),
(7, 4, '2025-01-15', CURRENT_DATE + INTERVAL '70 days', 'ASO-2025-007'),
-- Fernanda Lima (Delta) - Integração vence em 8 dias
(8, 6, '2025-03-29', CURRENT_DATE + INTERVAL '8 days', 'INT-2025-008'),
(8, 4, '2025-03-01', CURRENT_DATE + INTERVAL '90 days', 'ASO-2025-008'),
-- Roberto Dias (Delta) - sem data de vencimento (inconsistência)
(9, 4, '2025-01-01', NULL, 'ASO-2025-009'),
(9, 6, '2024-06-01', CURRENT_DATE + INTERVAL '15 days', 'INT-2024-009'),
-- Marcos Pereira (Omega) - NR-10 vencido há 20 dias, ASO vence em 2 dias
(10, 1, '2023-03-01', CURRENT_DATE - INTERVAL '20 days', 'NR10-2023-010'),
(10, 4, '2024-03-23', CURRENT_DATE + INTERVAL '2 days', 'ASO-2024-010'),
(10, 9, '2025-01-01', CURRENT_DATE + INTERVAL '100 days', 'NR06-2025-010'),
-- Juliana Ramos (Omega) - tudo ok
(11, 4, '2025-03-01', CURRENT_DATE + INTERVAL '200 days', 'ASO-2025-011'),
(11, 9, '2025-03-01', CURRENT_DATE + INTERVAL '180 days', 'NR06-2025-011'),
-- Thiago Nascimento (Omega) - Curso Incêndio vence em 14 dias
(12, 10, '2025-04-04', CURRENT_DATE + INTERVAL '14 days', 'INCEND-2025-012'),
(12, 4, '2025-02-15', CURRENT_DATE + INTERVAL '80 days', 'ASO-2025-012'),
-- Sandra Martins (Sol Nascente) - ASO vence em 45 dias
(13, 4, '2025-05-06', CURRENT_DATE + INTERVAL '45 days', 'ASO-2025-013'),
(13, 6, '2025-03-15', CURRENT_DATE + INTERVAL '110 days', 'INT-2025-013'),
-- Claudio Barbosa (Sol Nascente) - NR-06 vencido há 5 dias
(14, 9, '2024-03-16', CURRENT_DATE - INTERVAL '5 days', 'NR06-2024-014'),
(14, 4, '2025-01-01', CURRENT_DATE + INTERVAL '65 days', 'ASO-2025-014'),
-- Antonio Gomes (XYZ contrato encerrado) - ASO vencido
(15, 4, '2023-06-01', CURRENT_DATE - INTERVAL '100 days', 'ASO-2023-015');

-- Carteirinhas
INSERT INTO carteirinhas (funcionario_id, numero_carteirinha, data_emissao, data_vencimento, status) VALUES
(1, 'CART-2024-001', '2024-03-01', CURRENT_DATE + INTERVAL '5 days', 'ativa'),
(2, 'CART-2024-002', '2024-03-01', CURRENT_DATE - INTERVAL '3 days', 'vencida'),
(3, 'CART-2024-003', '2024-06-01', CURRENT_DATE, 'ativa'),
(4, 'CART-2024-004', '2025-01-01', CURRENT_DATE + INTERVAL '180 days', 'ativa'),
(5, 'CART-2024-005', '2024-03-01', CURRENT_DATE + INTERVAL '3 days', 'ativa'),
(6, 'CART-2024-006', '2024-01-01', CURRENT_DATE + INTERVAL '30 days', 'ativa'),
(7, 'CART-2024-007', '2025-01-01', CURRENT_DATE + INTERVAL '90 days', 'ativa'),
(8, 'CART-2024-008', '2024-06-01', CURRENT_DATE + INTERVAL '8 days', 'ativa'),
(9, 'CART-2024-009', '2024-06-01', CURRENT_DATE + INTERVAL '60 days', 'ativa'),
(10, 'CART-2023-010', '2023-06-01', CURRENT_DATE - INTERVAL '20 days', 'vencida'),
(11, 'CART-2024-011', '2025-01-01', CURRENT_DATE + INTERVAL '200 days', 'ativa'),
(12, 'CART-2024-012', '2024-09-01', CURRENT_DATE + INTERVAL '80 days', 'ativa'),
(13, 'CART-2024-013', '2025-01-01', CURRENT_DATE + INTERVAL '110 days', 'ativa'),
(14, 'CART-2024-014', '2024-01-01', CURRENT_DATE - INTERVAL '5 days', 'vencida'),
(15, 'CART-2022-015', '2022-06-01', CURRENT_DATE - INTERVAL '100 days', 'vencida');
