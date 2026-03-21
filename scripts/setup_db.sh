#!/bin/bash
# =============================================================================
# Script de setup do banco de dados PostgreSQL
# =============================================================================

set -e

DB_NAME="${DB_NAME:-carteirinhas_db}"
DB_USER="${DB_USER:-postgres}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

echo "=== Criando banco de dados: $DB_NAME ==="
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo "Banco já existe."

echo "=== Executando schema.sql ==="
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f ../database/schema.sql

echo "=== Executando seeds.sql ==="
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f ../database/seeds.sql

echo "=== Setup concluído! ==="
echo "Banco: $DB_NAME"
echo "Host: $DB_HOST:$DB_PORT"
