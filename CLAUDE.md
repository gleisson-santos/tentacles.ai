# Clilink — Plataforma de Agentes de Produtividade

## Objetivo
Sistema multi-agente que automatiza: postagem LinkedIn, gestão de Gmail/Calendar/Sheets, criação de PDFs/PPTX e chatbot Telegram — tudo orquestrado via Claude Code + Octogent dashboard.

## Tech Stack
- **IA de texto:** Groq API — `llama-3.3-70b-versatile`
- **IA de imagem:** Stability AI — `v2beta/stable-image/generate/core`
- **LinkedIn:** OAuth2 + LinkedIn API v2
- **Google:** Gmail API + Calendar API + Sheets API + Drive API (OAuth2)
- **Telegram:** python-telegram-bot v20+
- **PDF:** reportlab + pypdf
- **PowerPoint:** python-pptx
- **Dashboard:** Octogent (`octogent` no terminal) — fonte local na pasta `octogent/`
- **MCP Protocol:** FastMCP (todos os servidores)
- **Runtime:** Python 3.14 + Node.js 22 (Octogent)

## Mapa de Agentes (Tentáculos Octogent)

| Agente | Arquivo Principal | Responsabilidade |
|--------|-------------------|------------------|
| agent-skills | — | `.claude/skills/` — comportamento detalhado de cada agente |
| files-assistant | `mcp_servers/files_mcp/server.py` | Criação de PDFs e apresentações PowerPoint |
| google-assistant | `mcp_servers/google_mcp/server.py` | Gmail, Google Calendar e Google Sheets |
| linkedin-poster | `auto_poster.py` | Auto-post LinkedIn a cada 2h (Groq + Stability AI) |
| orchestrator | `.claude/skills/proactive-agent.md` | Coordenador central, monitora canal `clilink-events` |
| platform-infra | — | `start_clilink.ps1` — launcher que sobe todos os serviços |
| telegram-bot | `bots/telegram_bot.py` | Interface Telegram → detecta intenção → executa via Dashboard |

## Estrutura de Arquivos
```
Clilink/
├── CLAUDE.md                          ← LEIA PRIMEIRO em toda sessão
├── auto_poster.py                     ← Loop LinkedIn (2h)
├── linkedin_mcp_server.py             ← MCP LinkedIn
├── test_groq.py                       ← Teste sem publicar
├── test_producao.py                   ← Teste com publicação real
│
├── mcp_servers/
│   ├── google_mcp/
│   │   ├── server.py                  ← MCP Gmail + Calendar + Sheets
│   │   ├── auth.py                    ← OAuth2 Google
│   │   ├── gmail_tools.py             ← Funções Gmail
│   │   ├── calendar_tools.py          ← Funções Calendar
│   │   ├── sheets_tools.py            ← Funções Sheets
│   │   └── credentials/               ← token.json + client_secret.json (não commitar)
│   └── files_mcp/
│       ├── server.py                  ← MCP PDF + PPTX
│       ├── pdf_tools.py               ← Criação de PDFs
│       └── pptx_tools.py              ← Criação de PowerPoint
│
├── bots/
│   └── telegram_bot.py                ← Bot Telegram com detecção de intenção via Groq
│                                         Integra com Octogent via API HTTP (porta 8787)
│
├── scripts/
│   ├── new_tentacle.py                ← Cria novo tentáculo completo (agent+skill+MCP+deck)
│   └── sync_tentacles.py              ← Sincroniza Mapa de Agentes no CLAUDE.md
│
├── logs/
│   ├── logger.py                      ← Logger compartilhado (activity.log + canal octogent)
│   └── activity.log                   ← Log de todas as ações dos agentes
│
├── outputs/
│   ├── pdfs/                          ← PDFs gerados
│   ├── presentations/                 ← PPTX gerados
│   └── .status/                       ← Arquivos de status para bridge Telegram↔Dashboard
│                                         {task_id}.done contém caminho do arquivo gerado
│
├── .claude/
│   ├── settings.local.json            ← MCPs registrados + permissões
│   ├── skills/
│   │   ├── project-context.md
│   │   ├── bootstrap-project.md
│   │   ├── gmail-manager.md
│   │   ├── calendar-manager.md
│   │   ├── content-creator.md
│   │   └── proactive-agent.md         ← Orquestrador principal
│   ├── rules/efficiency.md
│   ├── agents/architect.md
│   └── commands/init.md
│
└── .octogent/tentacles/               ← 7 tentáculos: linkedin-poster, google-assistant,
                                          files-assistant, telegram-bot, orchestrator,
                                          platform-infra, agent-skills
```

## Credenciais e Setup

### Já configurado ✅
- `GROQ_API_KEY` — Definido em `.env`
- `STABILITY_KEY` — Definido em `.env`
- LinkedIn OAuth2 — em `.claude/settings.local.json`
- Token LinkedIn — `~/.linkedin_mcp_token.json`
- **Telegram Bot Token** — Definido em `.env`
- **Telegram User ID permitido** — Definido em `.env`
- **Google OAuth2** — Credenciais em `mcp_servers/google_mcp/credentials/` (Funcionando)
- **Configuração de LLM** — Gerida em `config/llm_config.json` e sincronizada via `/brain` no Telegram.

### Requer setup manual ⚠️
- (Nenhum setup crítico pendente no momento)

## Comandos de Execução

```powershell
# Instalar todas as dependências (recomendado para novas máquinas)
pip install -r requirements.txt

# LinkedIn auto-poster (produção, 2h)
python auto_poster.py

# Telegram Bot (token já hardcoded, apenas rodar)
python bots/telegram_bot.py

# Dashboard Octogent (deve estar rodando para o bot usar o Dashboard)
octogent

# Setup Google OAuth2 (1 vez)
python mcp_servers/google_mcp/auth.py

# Criar novo tentáculo
python scripts/new_tentacle.py <nome> "<descricao>" [--mcp] [--color "#RRGGBB"]

# Teste LinkedIn sem publicar
python test_groq.py
```

## Arquitetura do Dashboard Bridge (Telegram → Octogent)

Quando o usuário pede um PDF ou PPTX no Telegram:

1. Bot detecta intenção via Groq (`_detect_intent`)
2. Bot verifica se Octogent está online: `GET http://127.0.0.1:8787/api/deck/tentacles`
3. Se online: cria terminal via `POST http://127.0.0.1:8787/api/terminals` com `initialPrompt`
4. Octogent injeta o prompt no Claude Code após **12 segundos** (tempo de boot no Windows)
5. Claude Code executa a tarefa e escreve o caminho em `outputs/.status/{task_id}.done`
6. Bot faz poll do arquivo de status (até 120s) e envia o arquivo gerado no Telegram
7. Se offline ou timeout: fallback para criação direta em Python

**Correção crítica Octogent:** `INITIAL_PROMPT_DELAY_MS` aumentado de 4s→12s no arquivo `dist/api/createApiServer-*.js` dentro da pasta do Octogent.
Se o Octogent for reinstalado/atualizado, essa edição se perde — reaplicar.

## Estado Atual (06/05/2026)
- ✅ LinkedIn auto-poster funcionando (Groq AI, 2h intervalo)
- ✅ Google MCP Server criado e configurado (Gmail, Calendar, Sheets funcionais)
- ✅ Files MCP Server criado (PDF + PPTX funcionando)
- ✅ Telegram Bot funcionando com detecção de intenção (Gmail, Calendar, Sheets, PDF, PPTX, LinkedIn)
- ✅ Octogent Dashboard rodando com 7 tentáculos configurados
- ✅ Bridge Telegram → Dashboard implementada via API HTTP
- ✅ Sistema de log em `logs/activity.log` + canal `clilink-events`
- ✅ Scripts de automação em `scripts/` (new_tentacle, sync_tentacles)
- ⚠️ Dashboard bridge em fase de testes (prompt auto-submit sendo ajustado)

## Próximos Passos
1. **Testar bridge completo** — Pedir PDF no Telegram e confirmar que aparece no Dashboard E retorna o arquivo
2. **Múltiplas tarefas simultâneas** — Implementar `asyncio.create_task()` para paralelismo no bot

## Regras para Claude
1. **SEMPRE leia este CLAUDE.md primeiro** — contém todo o estado do projeto
2. **NUNCA faça scan completo** — use Glob/Grep pontual
3. **MCP principal:** `mcp_servers/google_mcp/server.py` e `mcp_servers/files_mcp/server.py`
4. **Credenciais Google:** nunca commitar `credentials/token.json` ou `client_secret.json`
5. **Outputs:** PDFs → `outputs/pdfs/`, PPTX → `outputs/presentations/`
6. **Octogent API:** sempre via HTTP `http://127.0.0.1:8787` — subprocess não funciona no Windows sem shell=True
7. **Arquivo de status bridge:** `outputs/.status/{task_id}.done` — mecanismo de IPC entre Dashboard e bot
