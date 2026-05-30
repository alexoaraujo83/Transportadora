#!/usr/bin/env sh
set -eu
BACKUP_DIR=${BACKUP_DIR:-./backups}
mkdir -p "$BACKUP_DIR"
STAMP=$(date +%Y%m%d_%H%M%S)
FILE="$BACKUP_DIR/fusion_${STAMP}.sql.gz"
docker compose -f docker-compose.prod.yml exec -T db pg_dump -U "${POSTGRES_USER:-fusion}" "${POSTGRES_DB:-fusion}" | gzip > "$FILE"
echo "Backup gerado: $FILE"
