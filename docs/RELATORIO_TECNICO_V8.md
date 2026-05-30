# Fusion Cargas Inteligente V8 — Notificações em tempo real

## Objetivo
Implantar comunicação operacional em tempo real para reduzir atrasos entre operação, financeiro, segurança e acompanhamento de fretes.

## Entregas
- Django Channels configurado no ASGI.
- WebSocket autenticado em `/ws/notificacoes/`.
- Central web em `/notificacoes/`.
- API REST em `/api/v1/notificacoes/`.
- Marcação de notificação como lida individual e em lote.
- Modelo expandido com usuário, canal, prioridade, link e payload JSON.
- Serviço `NotificacaoService` para uso por outros módulos.
- Preparação para Redis/Channels em produção.

## Uso técnico
Para disparar uma notificação por código:

```python
from notificacoes.services import NotificacaoService
NotificacaoService.criar(usuario=user, titulo='Frete atualizado', mensagem='Status alterado para em trânsito.', canal='frete', prioridade='alta')
```

## Próximo passo recomendado
V9: rastreamento real com mapas, geocodificação, eventos de localização e mapa operacional.
