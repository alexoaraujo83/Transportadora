# API Operacional V3

Base: `/api/v1/`

## Endpoints principais
- `/api/v1/fretes/`
- `/api/v1/motoristas/`
- `/api/v1/transportadoras/`
- `/api/v1/cotacoes/`
- `/api/v1/financeiro/`
- `/api/v1/rastreamentos/`
- `/api/v1/checklists/`
- `/api/v1/historico-status/`
- `/api/v1/consultas-risco/`

## Ações especiais de frete
### Mudar status
`POST /api/v1/fretes/{id}/mudar-status/`
```json
{"status":"AGENDADO", "observacao":"Motorista confirmado"}
```

### Registrar coleta
`POST /api/v1/fretes/{id}/registrar-coleta/`
```json
{"observacao":"Coleta realizada às 08h30"}
```

### Registrar descarga
`POST /api/v1/fretes/{id}/registrar-descarga/`
```json
{"observacao":"Descarga finalizada sem avarias"}
```

### Consultar checklist
`GET /api/v1/fretes/{id}/checklist/`
