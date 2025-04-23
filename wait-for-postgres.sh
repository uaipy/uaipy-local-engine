#!/bin/bash
echo "Aguardando PostgreSQL..."
while ! nc -z uaipydb 5432; do
  sleep 1
done

echo "PostgreSQL está pronto, iniciando aplicação..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
