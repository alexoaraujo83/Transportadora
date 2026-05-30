# Deploy de Produção — Fusion Cargas Inteligente V14

## Pré-requisitos
- Docker e Docker Compose instalados.
- Domínio configurado.
- Banco PostgreSQL persistente.
- Variáveis de ambiente seguras.
- Backup automatizado.

## Passos
```bash
cp .env.production.example .env
# editar SECRET_KEY, DB, domínio, credenciais e integrações
chmod +x scripts/*.sh
./scripts/install_prod.sh
```

## Comandos úteis
```bash
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

## Segurança mínima antes de publicar
- DEBUG=False.
- SECRET_KEY forte.
- ALLOWED_HOSTS configurado.
- CSRF_TRUSTED_ORIGINS com domínio HTTPS.
- Banco com senha forte.
- Admin padrão alterado/removido.
- Backup testado.
