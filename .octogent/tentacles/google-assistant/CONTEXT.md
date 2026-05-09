# Google Assistant

## Scope
Gerenciamento de Gmail, Google Calendar e Google Sheets via MCP.

## Key Files
- `mcp_servers/google-assistant/server.py` — servidor MCP (se aplicável)
- `scripts/new_tentacle.py` — como este tentáculo foi criado

## MCP Server
- `mcp_servers/google-assistant/server.py` — servidor MCP FastMCP
- Registrado em `.claude/settings.local.json` como `google-assistant`

## Ferramentas MCP disponíveis
- `google-assistant_action(param)` — ação principal (personalizar)

## Key Decisions
- TODO: documentar decisões de arquitetura

## Conventions
- TODO: documentar convenções deste agente

## Related Tentacles
- `orchestrator` — coordenador principal
