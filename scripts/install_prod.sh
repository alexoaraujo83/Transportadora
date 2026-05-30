#!/usr/bin/env bash
set -euo pipefail
if [ ! -f .env ]; then
  echo "Arquivo .env não encontrado. Copie .env.production.example para .env e ajuste as variáveis."
  exit 1
fi
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
echo "Deploy concluído. Verifique /health/ e logs do container web."
