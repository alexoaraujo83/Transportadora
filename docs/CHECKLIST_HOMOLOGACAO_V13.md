# Checklist de Homologação V13 - Fusion Cargas Inteligente

## 1. Ambiente
- [ ] `.env` criado com base em `.env.example`.
- [ ] Banco PostgreSQL ativo.
- [ ] Redis ativo para cache/canais.
- [ ] `python manage.py check` executado sem erros.
- [ ] Migrations aplicadas.
- [ ] Superusuário criado.

## 2. Segurança
- [ ] DEBUG desativado em produção.
- [ ] SECRET_KEY forte configurada.
- [ ] ALLOWED_HOSTS configurado.
- [ ] HTTPS habilitado no proxy/Nginx.
- [ ] Rate limit validado.
- [ ] Perfis e políticas padrão criados.

## 3. Operação
- [ ] Cadastro de cliente testado.
- [ ] Cadastro de motorista testado.
- [ ] Cadastro de transportadora testado.
- [ ] Cotação criada e convertida em frete.
- [ ] Frete movimentado entre status operacionais.
- [ ] Checklist, ocorrência e documento vinculados ao frete.
- [ ] Posição de rastreamento registrada.

## 4. Financeiro
- [ ] Conta a pagar criada.
- [ ] Conta a receber criada.
- [ ] Repasse de motorista lançado.
- [ ] Comissão operacional registrada.
- [ ] Conciliação testada.
- [ ] DRE simples conferida.

## 5. Portal externo
- [ ] Token externo criado.
- [ ] Consulta pública de frete validada.
- [ ] Aceite digital validado.
- [ ] Upload de comprovante validado.

## 6. Inteligência operacional
- [ ] Comando `gerar_insights` executado.
- [ ] Painel de inteligência acessível.
- [ ] Score de motorista calculado.
- [ ] Risco operacional exibido.

## 7. Entrega
- [ ] Testes automatizados executados.
- [ ] CI/CD configurado no repositório.
- [ ] Backup validado.
- [ ] Documentação entregue ao operador.
