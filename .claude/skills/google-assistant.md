# Skill: Google Assistant

## Papel
Gerenciamento de Gmail, Google Calendar e Google Sheets via MCP.

## Quando acionar
- Quando o usuário pedir algo relacionado a google assistant
- Delegado pelo orchestrator

## Ferramentas disponíveis
- `google-assistant_action(param)` — ação principal (personalizar em `mcp_servers/google-assistant/server.py`)

## Comportamento
1. Leia `.octogent/tentacles/google-assistant/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("google-assistant", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
