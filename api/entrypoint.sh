#!/bin/bash
set -e

echo "Aguardando banco de dados..."
until pg_isready -h postgres -p 5432 -U postgres > /dev/null 2>&1; do
  echo "Banco de dados não está pronto. Aguardando..."
  sleep 2
done

echo "Banco de dados pronto!"
echo "Executando migrações do Alembic..."
alembic upgrade head

echo "Iniciando aplicação..."
exec uvicorn main:app --host 0.0.0.0 --port 8000

