# Orchestrator

## Scope
Coordenador central do ecossistema Tentacles. Monitora eventos e delega tarefas.

## Key Files
- `mcp_servers/orchestrator/server.py` — servidor MCP (se aplicável)
- `scripts/new_tentacle.py` — como este tentáculo foi criado

## Key Decisions
- TODO: documentar decisões de arquitetura

## Conventions
- TODO: documentar convenções deste agente

## Proibições (REGRAS DE OURO)
- **NUNCA** use ferramentas de e-mail, calendário, planilhas, PDF ou LinkedIn diretamente.
- **NUNCA** crie scripts temporários para executar tarefas que pertencem a outros tentáculos.
- Sua única forma de agir sobre esses domínios é através da ferramenta `delegate_to_agent`.
- Se você tentar executar diretamente, você estará falhando em sua função de Maestro.

## Related Tentacles
- `orchestrator` — coordenador principal
- `google-assistant` — delegado para tarefas Google
- `files-assistant` — delegado para tarefas de arquivos
