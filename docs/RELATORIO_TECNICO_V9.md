# Fusion Cargas Inteligente V9 - Rastreamento e Mapas Reais

## Objetivo
Implantar camada realista de rastreamento, mapas e rotas, mantendo integrações externas preparadas para Google Maps, Mapbox, rastreadores veiculares ou aplicativo do motorista.

## Entregas
- Modelo `PontoRota` para pontos planejados da viagem.
- Modelo `PosicaoAtualFrete` para leitura rápida da última posição.
- `EventoRastreamento` ampliado com tipo, origem, velocidade e odômetro.
- Serviço `RastreamentoService` para registrar posição e concluir pontos.
- Serviço `MapasService` para links Google Maps.
- Tela de mapa operacional.
- Tela de rota por frete.
- API REST ampliada para posição atual, pontos de rota e mapa do frete.

## Status
- Rastreamento histórico: 85%
- Posição atual: 80%
- Rotas planejadas: 75%
- Mapas reais via link: 65%
- Integração com provedor pago de mapas: preparada, pendente de chave/API

## Próxima versão recomendada
V10 - Financeiro profissional: fluxo de contas a pagar/receber, comissões, DRE operacional, baixa parcial, anexos e conciliação.
