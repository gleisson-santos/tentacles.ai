---
name: files-assistant
description: Habilidade de files-assistant integrada ao ecossistema Tentacles.
---

# Skill: Files Assistant

## Papel
Criação de documentos profissionais (PDF e PowerPoint) via MCP.

## Quando acionar
- Quando o usuário pedir algo relacionado a files assistant
- Delegado pelo orchestrator

## Ferramentas disponíveis
- `files-assistant_action(param)` — ação principal (personalizar em `mcp_servers/files-assistant/server.py`)

## Comportamento
1. Leia `.octogent/tentacles/files-assistant/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("files-assistant", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
