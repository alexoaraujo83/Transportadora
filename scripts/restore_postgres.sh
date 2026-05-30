#!/usr/bin/env bash
set -euo pipefail
BACKUP_FILE=${1:-}
if [ -z "$BACKUP_FILE" ]; then
  echo "Uso: ./scripts/restore_postgres.sh caminho/backup.sql"
  exit 1
fi
docker compose -f docker-compose.prod.yml exec -T db psql -U fusion_user -d fusion_cargas < "$BACKUP_FILE"
echo "Restauração concluída."
