# Fusion Cargas Inteligente V7 — Segurança Avançada

## Objetivo
A V7 endurece o sistema para uso mais próximo de produção, com controle de acesso dinâmico, trilha de eventos de segurança, rate limit e parâmetros de segurança HTTP.

## Implantações realizadas

### 1. App `seguranca`
Inclui modelos próprios para:
- `EventoSeguranca`: registra rate limit, acesso negado, webhooks inválidos, ações críticas e eventos sistêmicos.
- `PoliticaAcesso`: permite definir permissões por perfil e módulo.

### 2. Rate limit
Foi criado `RateLimitMiddleware` para limitar:
- tentativas de login e emissão de JWT;
- chamadas de API.

Variáveis configuráveis no `.env`:
- `RATE_LIMIT_WINDOW_SECONDS`
- `RATE_LIMIT_LOGIN_PER_MINUTE`
- `RATE_LIMIT_API_PER_MINUTE`

### 3. Auditoria de acessos negados
Respostas 401/403 passam a gerar evento de segurança automaticamente.

### 4. Painel de segurança
Nova rota:
- `/seguranca/`

Exibe eventos recentes, quantidade de eventos críticos/altos e políticas de acesso cadastradas.

### 5. Políticas padrão
Novo comando:

```bash
python manage.py criar_politicas_padrao
```

Cria permissões iniciais para ADMIN, OPERADOR, CLIENTE, MOTORISTA e TRANSPORTADORA.

### 6. Hardening de produção
Configurações adicionadas:
- `SECURE_CONTENT_TYPE_NOSNIFF`
- `SECURE_REFERRER_POLICY`
- `SESSION_COOKIE_SAMESITE`
- `CSRF_COOKIE_SAMESITE`
- SSL redirect em produção
- cookies seguros em produção
- HSTS em produção

## Status V7
- Segurança avançada: 80%
- Rate limit: 75%
- Auditoria de segurança: 75%
- Políticas dinâmicas: 70%
- Produção segura: 70%

## Próxima versão sugerida
V8 — Notificações em tempo real com WebSocket/Django Channels, eventos operacionais ao vivo e painel de alertas.
