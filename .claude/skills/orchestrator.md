# Skill: Orchestrator

## Papel
Coordenador central do ecossistema Tentacles. Monitora eventos e delega tarefas.

## Quando acionar
- Quando o usuário pedir algo relacionado a orchestrator
- Delegado pelo orchestrator

## Comportamento
1. Leia `.octogent/tentacles/orchestrator/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("orchestrator", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
