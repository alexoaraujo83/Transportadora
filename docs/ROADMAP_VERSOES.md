# Roadmap das versões Fusion Cargas Inteligente

## V1 — Base funcional
- Estrutura Django.
- Apps principais.
- Dashboard inicial.
- Fretes, motoristas, transportadoras, cotações, financeiro, rastreamento, notificações, webhooks e auditoria.
- Docker e README inicial.

## V2 — Operação web e API
- JWT.
- CRUD web.
- Permissões por perfil.
- API REST com filtros.
- Dashboard ampliado.
- Relatórios CSV.
- Serviços preparados para WhatsApp, risco e mapas.

## V3 — Fluxo operacional
- Kanban operacional.
- Checklist por frete.
- Histórico de status.
- Consulta de risco preparada.
- Ações de coleta, descarga e mudança de status.
- Testes iniciais de fluxo.

## V4 — Operação avançada
- Documentos por frete.
- Ocorrências operacionais.
- Tarefas operacionais.
- Financeiro com categoria, centro de custo e data de pagamento.
- Relatórios adicionais.

## V5 — Produção técnica
- Healthcheck.
- API de KPIs.
- Seed demo.
- Docker Compose de produção.
- Nginx preparado.
- Gunicorn.
- Script de backup PostgreSQL.

## V6 — Comercial e precificação
- Cadastro de clientes.
- Tabela de preços por rota.
- Propostas comerciais.
- Simulador de precificação web/API.
- Dashboard com indicadores comerciais.

## Próximas versões recomendadas

### V7 — Segurança e governança
- RBAC/ABAC mais granular por ação e objeto.
- Rate limit real no login e API.
- Trilha de auditoria com antes/depois das alterações.
- Bloqueio por tentativas inválidas.
- Política de senha, sessão e expiração.

### V8 — Notificações em tempo real
- Django Channels/WebSocket.
- Alertas em tempo real no dashboard.
- Fila Celery + Redis para tarefas assíncronas.
- Envio automático de mensagens via WhatsApp/e-mail.

### V9 — Rastreamento e mapas reais
- Integração com API de mapas.
- Distância estimada, rota, ETA e eventos geográficos.
- Portal/app do motorista para enviar localização e comprovantes.

### V10 — Financeiro profissional
- Contas a pagar/receber.
- DRE operacional.
- Comissão por operador/prospectador.
- Fechamento por cliente, motorista e transportadora.
- Exportações Excel/PDF.

### V11 — Portal externo
- Portal do cliente.
- Portal do motorista.
- Portal da transportadora.
- Upload de documentos e comprovantes.
- Acompanhamento público com token seguro.

### V12 — Inteligência operacional
- Ranking de motoristas.
- Sugestão de preço por histórico.
- Análise de margem por rota.
- Previsão de risco operacional.
- Otimização de prospecção.

### V13 — Qualidade final e homologação
- Testes automatizados completos.
- CI/CD.
- Observabilidade.
- Logs estruturados.
- Homologação de produção.
- Manual do usuário e treinamento.


## V9 concluída
Rastreamento e mapas reais implantados. Faltam V10 a V13 para maturidade de produção completa.
