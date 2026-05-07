# Orchestrator — Todo

## Backlog
- [ ] Criar terminal no Octogent com skill proactive-agent.md como initial prompt
- [ ] Implementar leitura periódica de `logs/activity.log` para status dashboard
- [ ] Criar rotina de "resumo do dia" (emails + agenda + posts) entregue às 8h via Telegram
- [ ] Adicionar alerta automático quando linkedin-poster falhar 2x seguidas
- [ ] Implementar health check de todos os agentes via `/status` no Telegram
- [ ] Criar swarm de workers para processar múltiplas tarefas em paralelo

## Concluído
- [x] Skill proactive-agent.md definida com mapa de delegação completo
- [x] Canal clilink-events configurado para receber eventos de todos os agentes
- [x] Logger compartilhado (logs/logger.py) usado por todos os tentáculos
- [x] Octogent inicializado no projeto (octogent init)
