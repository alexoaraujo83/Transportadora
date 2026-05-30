# Fusion Cargas Inteligente V6 FULL

## Objetivo da V6
A V6 amplia a versão anterior com foco comercial e pré-venda operacional, adicionando cadastro de clientes, tabela de preço por rota, propostas comerciais e simulador de precificação.

## Implantações adicionadas

### 1. CRM básico de clientes
- Novo app `clientes`.
- Cadastro de cliente PF/PJ.
- Documento CPF/CNPJ.
- Contato principal, telefone, e-mail e origem padrão.
- CRUD web protegido por login e perfil.
- API REST `/api/v1/clientes/`.

### 2. Precificação e tabela de rotas
- Novo app `precificacao`.
- Cadastro de tabela de preço por origem/destino.
- Campos de veículo, carroceria, valor mínimo motorista, pedágio, custo extra e margem percentual.
- Cálculo automático de valor sugerido ao cliente quando não houver valor fechado.
- API REST `/api/v1/tabelas-preco/`.

### 3. Simulador de preço
- Tela web `/precificacao/simulador/`.
- API `/api/v1/simular-preco/`.
- Busca tabela ativa pela rota informada.
- Retorna valor motorista, valor cliente, margem e indicação se encontrou tabela.

### 4. Propostas comerciais
- Cadastro de propostas por cliente, rota, carga, peso, cubagem e validade.
- Status: rascunho, enviada, aprovada, recusada e cancelada.
- API REST `/api/v1/propostas-comerciais/`.

### 5. Dashboard ampliado
- Indicador de clientes cadastrados.
- Indicador de tabelas de preço ativas.
- Indicador de propostas comerciais abertas.

## Validação executada
- Compilação de sintaxe Python: OK.
- Integridade do ZIP: OK.

## Observação técnica
A validação completa com `manage.py check` exige instalação das dependências do `requirements.txt`. O pacote está preparado para execução com Docker/PostgreSQL.
