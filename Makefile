# =============================================================================
# Agente de Monitoramento Preventivo de Carteirinhas
# Makefile - Docker Compose
# =============================================================================

SHELL := /bin/bash

.PHONY: help up down restart logs logs-backend logs-frontend logs-db \
        processar test-api build clean reset info

# ─────────────────────────────────────────────
# Help
# ─────────────────────────────────────────────

help: ## Exibe esta lista de comandos
	@echo ""
	@echo "  Agente de Monitoramento - Comandos"
	@echo "  ======================================================="
	@echo ""
	@echo "  DOCKER"
	@echo "    make up               Sobe tudo (banco + backend + frontend)"
	@echo "    make down             Para tudo"
	@echo "    make restart          Reinicia tudo"
	@echo "    make build            Rebuild das imagens"
	@echo "    make reset            Para, limpa volumes e sobe do zero"
	@echo "    make clean            Remove containers, imagens e volumes"
	@echo ""
	@echo "  LOGS"
	@echo "    make logs             Logs de todos os servicos"
	@echo "    make logs-backend     Logs do backend"
	@echo "    make logs-frontend    Logs do frontend"
	@echo "    make logs-db          Logs do banco"
	@echo ""
	@echo "  PROCESSAMENTO"
	@echo "    make processar        Processa vencimentos (gera alertas)"
	@echo "    make test-api         Testa endpoints da API"
	@echo ""
	@echo "  INFO"
	@echo "    make info             Exibe URLs e status"
	@echo "    make deploy-info      Instrucoes de deploy"
	@echo ""

# ─────────────────────────────────────────────
# Docker Compose
# ─────────────────────────────────────────────

up: ## Sobe tudo (banco + backend + frontend)
	@echo ""
	@echo "[DOCKER] Subindo servicos..."
	@echo ""
	docker compose up -d --build
	@echo ""
	@echo "  ======================================================="
	@echo "  [OK] Tudo rodando!"
	@echo ""
	@echo "  Dashboard:  http://localhost:3000"
	@echo "  API Docs:   http://localhost:8000/docs"
	@echo ""
	@echo "  Proximo passo:"
	@echo "    make processar    (gera os alertas)"
	@echo ""
	@echo "  Ver logs:"
	@echo "    make logs"
	@echo "  ======================================================="
	@echo ""

down: ## Para tudo
	@echo "[DOCKER] Parando servicos..."
	docker compose down
	@echo "[OK] Parado"

restart: ## Reinicia tudo
	@echo "[DOCKER] Reiniciando..."
	docker compose restart
	@echo "[OK] Reiniciado"

build: ## Rebuild das imagens Docker
	@echo "[DOCKER] Rebuild..."
	docker compose build --no-cache
	@echo "[OK] Imagens reconstruidas"

reset: ## Para, limpa tudo e sobe do zero (inclusive banco)
	@echo "[DOCKER] Reset completo..."
	docker compose down -v
	docker compose up -d --build
	@echo ""
	@echo "[OK] Tudo recriado do zero"
	@echo "     Rode 'make processar' para gerar alertas"
	@echo ""

clean: ## Remove containers, imagens e volumes do projeto
	@echo "[CLEAN] Removendo tudo..."
	docker compose down -v --rmi local --remove-orphans
	@echo "[OK] Limpo"

# ─────────────────────────────────────────────
# Logs
# ─────────────────────────────────────────────

logs: ## Logs de todos os servicos (tempo real)
	docker compose logs -f

logs-backend: ## Logs do backend
	docker compose logs -f backend

logs-frontend: ## Logs do frontend
	docker compose logs -f frontend

logs-db: ## Logs do banco
	docker compose logs -f db

# ─────────────────────────────────────────────
# Processamento e testes
# ─────────────────────────────────────────────

processar: ## Executa o processamento de vencimentos
	@echo "[PROCESSAR] Executando..."
	@curl -s -X POST http://localhost:8000/api/processar | python -m json.tool 2>/dev/null || \
		curl -s -X POST http://localhost:8000/api/processar
	@echo ""

test-api: ## Testa os principais endpoints
	@echo ""
	@echo "== Health =="
	@curl -s http://localhost:8000/health
	@echo ""
	@echo ""
	@echo "== Resumo =="
	@curl -s http://localhost:8000/api/resumo | python -m json.tool 2>/dev/null || \
		curl -s http://localhost:8000/api/resumo
	@echo ""
	@echo "== Empresas =="
	@curl -s http://localhost:8000/api/empresas | python -m json.tool 2>/dev/null || \
		curl -s http://localhost:8000/api/empresas
	@echo ""
	@echo "== Alertas (top 5) =="
	@curl -s "http://localhost:8000/api/alertas?limit=5" | python -m json.tool 2>/dev/null || \
		curl -s "http://localhost:8000/api/alertas?limit=5"
	@echo ""
	@echo "[OK] Testes concluidos"

# ─────────────────────────────────────────────
# Acesso direto ao banco
# ─────────────────────────────────────────────

db-shell: ## Abre o psql dentro do container
	docker compose exec db psql -U postgres -d carteirinhas_db

db-check: ## Verifica dados no banco
	@echo "[DB] Verificando..."
	@docker compose exec db psql -U postgres -d carteirinhas_db \
		-c "SELECT 'Empresas: ' || count(*) FROM empresas_contratadas UNION ALL SELECT 'Funcionarios: ' || count(*) FROM funcionarios UNION ALL SELECT 'Alertas: ' || count(*) FROM alertas;"

# ─────────────────────────────────────────────
# Informacoes
# ─────────────────────────────────────────────

info: ## Exibe URLs e status dos containers
	@echo ""
	@echo "  Agente de Monitoramento de Carteirinhas"
	@echo "  ======================================================="
	@echo "  Dashboard:    http://localhost:3000"
	@echo "  API:          http://localhost:8000"
	@echo "  Swagger:      http://localhost:8000/docs"
	@echo "  PostgreSQL:   localhost:5432 (carteirinhas_db)"
	@echo ""
	@echo "  Status dos containers:"
	@docker compose ps
	@echo ""

deploy-info: ## Instrucoes de deploy
	@echo ""
	@echo "  Deploy"
	@echo "  ======================================================="
	@echo ""
	@echo "  Frontend (Vercel):"
	@echo "    1. Push para GitHub"
	@echo "    2. Importe em vercel.com"
	@echo "    3. Root Directory: frontend"
	@echo "    4. Env: NEXT_PUBLIC_API_URL=[url-backend]"
	@echo ""
	@echo "  Backend (Render/Railway):"
	@echo "    1. Conecte o repo"
	@echo "    2. Root Directory: backend"
	@echo "    3. Start: uvicorn app.main:app --host 0.0.0.0 --port 8000"
	@echo "    4. Env: DATABASE_URL=[connection-string]"
	@echo ""
	@echo "  Banco (Neon/Supabase):"
	@echo "    1. Crie um projeto gratuito"
	@echo "    2. Execute schema.sql e seeds.sql"
	@echo "    3. Copie a connection string"
	@echo ""
