# Skill: Agent Skills

## Papel
Repositório de comportamentos e instruções detalhadas de cada agente.

## Quando acionar
- Quando o usuário pedir algo relacionado a agent skills
- Delegado pelo orchestrator

## Comportamento
1. Leia `.octogent/tentacles/agent-skills/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("agent-skills", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
