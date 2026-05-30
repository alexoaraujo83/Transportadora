# Runbook de Incidentes — V14

## Sistema fora do ar
1. Verificar containers: `docker compose -f docker-compose.prod.yml ps`.
2. Verificar logs: `docker compose -f docker-compose.prod.yml logs --tail=200 web`.
3. Reiniciar serviços: `docker compose -f docker-compose.prod.yml restart`.
4. Conferir banco e Redis.

## Erro de banco
1. Verificar conexão e credenciais no `.env`.
2. Rodar migrations pendentes.
3. Conferir espaço em disco.
4. Restaurar backup se necessário.

## Lentidão
1. Verificar CPU/RAM.
2. Conferir queries e logs.
3. Limpar cache se necessário.
4. Escalar web workers.

## Falha de integração externa
1. Conferir tokens e URLs no `.env`.
2. Verificar fila/webhooks pendentes.
3. Reprocessar webhooks não processados.
