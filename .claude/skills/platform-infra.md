# Skill: Platform Infra

## Papel
Infraestrutura e launcher do sistema

## Quando acionar
- Quando o usuário pedir algo relacionado a platform infra
- Delegado pelo orchestrator

## Comportamento
1. Leia `.octogent/tentacles/platform-infra/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("platform-infra", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
