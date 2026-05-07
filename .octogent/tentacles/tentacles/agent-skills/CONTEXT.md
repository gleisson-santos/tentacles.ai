# Agent Skills

Camada comportamental: skills Claude, regras de eficiência e configuração de MCPs.

## Scope
- `.claude/skills/` — comportamento detalhado de cada agente
- `.claude/rules/efficiency.md` — regras obrigatórias de uso de tokens
- `.claude/agents/architect.md` — persona arquiteto com decisões registradas
- `.claude/commands/init.md` — checklist de inicialização de sessão
- `.claude/settings.local.json` — MCPs registrados + permissões PowerShell/Bash

## Key Decisions

### Skills por agente
Cada agente do Clilink tem uma skill dedicada que define seu comportamento detalhado:

| Skill | Agente | Responsabilidade |
|-------|--------|-----------------|
| `proactive-agent.md` | Orchestrator | Mapa de delegação, priorização de urgência |
| `gmail-manager.md` | Google Assistant | Comportamento inbox, envio, categorização |
| `calendar-manager.md` | Google Assistant | Briefing matinal, criação de eventos, fuso SP |
| `content-creator.md` | LinkedIn + Files | Estrutura de posts, contratos PDF, PPTX |
| `project-context.md` | Todos | Resumo rápido para orientar sessões novas |
| `bootstrap-project.md` | Meta | Prompt reutilizável para inicializar novos projetos |

### MCPs registrados em `settings.local.json`
Três MCP Servers ativos via stdio transport:
- `linkedin-poster` → `linkedin_mcp_server.py` com credenciais OAuth2 no `env`
- `google-assistant` → `mcp_servers/google_mcp/server.py`
- `files-assistant` → `mcp_servers/files_mcp/server.py`

**Atenção:** `LINKEDIN_CLIENT_SECRET` está em texto plano no `settings.local.json` — não commitar este arquivo.

### Permissões PowerShell
Allowlist extensa em `settings.local.json` permite: `octogent *`, `python *`, `pip install *`, `git *`, `npm *`, `winget install *` sem prompt de confirmação.

## Conventions
- Skills usam seções `## Papel`, `## Ferramentas disponíveis`, `## Comportamento padrão`
- Regras em `efficiency.md` são OBRIGATÓRIAS em toda sessão — não são sugestões
- `project-context.md` é o primeiro arquivo a ler em sessão nova; evita scan do repo
- Ao adicionar nova ferramenta a um agente, atualizar tanto a skill quanto o `CONTEXT.md` do tentáculo correspondente
- `architect.md` é o lugar canônico para registrar decisões arquiteturais com data

## Related Tentacles
- Todos os tentáculos — cada um tem uma skill correspondente aqui
- `orchestrator` — skill `proactive-agent.md` é o cérebro de delegação

<!-- octogent:suggested-skills:start -->
## Suggested Skills

You can use these skills if you need to.

- `bootstrap-project`
- `project-context`
<!-- octogent:suggested-skills:end -->
