# Tentacles — Plataforma de Agentes de Produtividade

> **LEIA ESTE ARQUIVO PRIMEIRO em toda sessão.** Ele é a memória operacional do projeto.

## Objetivo
Sistema multi-agente que automatiza: envio/gestão de Gmail, agendamento no Google Calendar, análise de Google Sheets, postagem LinkedIn (texto + imagem), criação de PDFs/PPTX, transcrição de YouTube → Reels, chatbot Telegram com intenção inteligente — tudo orquestrado visualmente via Octogent Dashboard.

## Tech Stack
- **LLM principal:** OpenRouter — `x-ai/grok-4.1-fast` (via `mcp_servers/llm_bridge/`)
- **LLM alternativo:** Groq API — `llama-3.3-70b-versatile`
- **IA de imagem:** Stability AI — `v2beta/stable-image/generate/core`
- **LinkedIn:** OAuth2 + LinkedIn API v2 (token em `~/.linkedin_mcp_token.json`)
- **Google:** Gmail API + Calendar API + Sheets API + Drive API (OAuth2 em `mcp_servers/google_mcp/credentials/`)
- **Telegram:** python-telegram-bot v20+ (token em `.env`)
- **PDF:** reportlab + pypdf
- **PowerPoint:** python-pptx
- **Dashboard:** Octogent (porta `8787`) — fonte local em `octogent/`
- **MCP Protocol:** FastMCP (todos os servidores)
- **Delegação:** `scripts/delegate_task.py` — cria terminais via API do Octogent
- **Runtime:** Python 3.14 + Node.js 22 (Octogent)

## Mapa de Agentes (Tentáculos Octogent)

| Agente | MCP Server | Skill | Status |
|--------|-----------|-------|--------|
| `orchestrator` | `mcp_servers/orchestrator/server.py` | `.claude/skills/orchestrator.md` | 🟡 Funcional (delegação parcial) |
| `google-assistant` | `mcp_servers/google_mcp/server.py` | `.claude/skills/google-assistant.md` | 🟢 Funcional |
| `files-assistant` | `mcp_servers/files_mcp/server.py` | `.claude/skills/files-assistant.md` | 🟢 Funcional |
| `linkedin-poster` | `mcp_servers/linkedin_mcp/server.py` | `.claude/skills/linkedin-poster.md` | 🔴 MCP OK, integração pendente |
| `reels-factory` | `mcp_servers/reels-factory/server.py` | `.claude/skills/reels-factory.md` | 🟡 Em progresso |
| `platform-infra` | `mcp_servers/platform-infra/server.py` | `.claude/skills/platform-infra.md` | 🟡 Funcional |
| `telegram-bot` | `bots/telegram_bot.py` | `.claude/skills/telegram-bot.md` | 🟢 Funcional |
| `agent-skills` | — | `.claude/skills/agent-skills.md` | 🟡 Esqueleto |

## Estrutura de Arquivos

```
tentacles/
├── CLAUDE.md                          ← LEIA PRIMEIRO (memória operacional)
├── GEMINI.md                          ← Instruções para Gemini CLI
├── DEV_PROGRESS.md                    ← Log de progresso e bugs
├── README.md                          ← Documentação pública do projeto
│
├── auto_poster.py                     ← Loop LinkedIn autônomo (2h)
├── spawn_workers.js                   ← [LEGADO] pode ser removido
│
├── mcp_servers/
│   ├── google_mcp/                    ← Gmail + Calendar + Sheets
│   │   ├── server.py                  ← MCP principal
│   │   ├── auth.py                    ← OAuth2 setup (rodar 1x)
│   │   ├── gmail_tools.py
│   │   ├── calendar_tools.py
│   │   ├── sheets_tools.py
│   │   └── credentials/               ← token.json + client_secret.json (NÃO commitar)
│   ├── files_mcp/                     ← PDF + PPTX
│   │   ├── server.py
│   │   ├── pdf_tools.py
│   │   └── pptx_tools.py
│   ├── linkedin_mcp/                  ← LinkedIn OAuth2 + Posting + Stability AI
│   │   └── server.py                  ← authenticate, create_post, create_post_with_image, generate_image
│   ├── reels-factory/                 ← Transcrição YouTube → Reels
│   │   └── server.py
│   ├── orchestrator/                  ← Delegação via API Octogent
│   │   └── server.py                  ← get_last_activity, delegate_to_agent
│   ├── platform-infra/                ← Monitoramento de serviços
│   │   └── server.py                  ← check_platform_health, get_system_resources
│   ├── llm_bridge/                    ← Multi-LLM switcher (Grok, Groq, Gemini)
│   │   └── server.py
│   └── files-assistant/               ← Alias/wrapper (usa files_mcp internamente)
│
├── bots/
│   └── telegram_bot.py                ← Bot principal (detecção de intenção + bridge)
│
├── scripts/
│   ├── new_tentacle.py                ← Criador de novos tentáculos
│   ├── sync_tentacles.py              ← Sincroniza mapa de agentes no CLAUDE.md
│   ├── delegate_task.py               ← Força delegação via API (evita auto-exec do Orchestrator)
│   └── trends_monitor.py              ← Monitor de tendências (modo loop)
│
├── logs/
│   ├── logger.py                      ← Logger compartilhado (log + canal tentacles-events)
│   └── activity.log                   ← Histórico de todas as ações
│
├── outputs/
│   ├── pdfs/                          ← PDFs gerados
│   ├── presentations/                 ← PPTX gerados
│   ├── transcripts/                   ← Transcrições YouTube
│   └── .status/                       ← IPC Bridge: {task_id}.done com "OK|mensagem" ou caminho
│
├── .claude/
│   ├── settings.local.json            ← MCPs registrados + permissões
│   └── skills/                        ← Instruções de comportamento por agente
│       ├── orchestrator.md
│       ├── google-assistant.md
│       ├── files-assistant.md
│       ├── linkedin-poster.md
│       ├── reels-factory.md
│       ├── platform-infra.md
│       ├── telegram-bot.md
│       ├── trends-intelligence.md
│       └── proactive-agent.md
│
└── .octogent/
    ├── state/deck.json                ← Estado visual do Dashboard (cores, posições)
    └── tentacles/                     ← Estado persistente de cada agente
        ├── google-assistant/CONTEXT.md
        ├── files-assistant/CONTEXT.md
        ├── linkedin-poster/CONTEXT.md
        ├── orchestrator/CONTEXT.md
        ├── platform-infra/CONTEXT.md
        ├── reels-factory/CONTEXT.md
        ├── telegram-bot/CONTEXT.md
        └── agent-skills/CONTEXT.md
```

## Fluxo de Orquestração (Telegram → Dashboard → Agente → Telegram)

```
Usuário (Telegram)
    ↓ mensagem
Telegram Bot
    ↓ _detect_intent() via LLM
    ↓ identifica: gmail_send / pdf_create / calendar_create / etc.
    ↓ POST http://127.0.0.1:8787/api/terminals (tentacleId: "orchestrator")
Orchestrator (Dashboard — Terminal visual)
    ↓ lê instrução do prompt
    ↓ executa: python scripts/delegate_task.py --agent google-assistant --prompt "..." --task_id XXX
API Octogent
    ↓ cria terminal para o agente filho (mantém no círculo principal do gráfico)
Google Assistant (Dashboard — Terminal visual)
    ↓ executa a tarefa (enviar email, criar evento, etc.)
    ↓ grava: outputs/.status/{task_id}.done com "OK|Mensagem de sucesso"
Telegram Bot (polling)
    ↓ lê o arquivo .done
    ↓ envia "✅ E-mail enviado para X" para o usuário
Usuário (Telegram) ← confirmação
```

## Arquitetura Bridge (IPC via arquivos .done)

```python
# O agente filho deve gravar:
with open(f"outputs/.status/{task_id}.done", "w") as f:
    f.write("OK|E-mail enviado com sucesso para fulano@email.com")

# O Bot lê e converte:
# "OK|mensagem" → "✅ mensagem"
# caminho de arquivo → envia o arquivo no Telegram
# qualquer outro texto → "✅ texto"
```

## Credenciais e Setup

### ✅ Configurado e Funcionando
- `GROQ_API_KEY` — `.env`
- `OPENROUTER_API_KEY` — `.env`
- `STABILITY_KEY` — `.env`
- `TELEGRAM_BOT_TOKEN` — `.env`
- `ALLOWED_USER_ID` — `.env`
- Google OAuth2 — `mcp_servers/google_mcp/credentials/token.json` (Funcionando)
- LinkedIn OAuth2 — `~/.linkedin_mcp_token.json`

### ⚠️ Verificar Antes de Usar
- LinkedIn token pode expirar. Rodar `authenticate()` no MCP se der 401.
- Google token se renova automaticamente, mas se expirar, rodar `python mcp_servers/google_mcp/auth.py`.

## Comandos de Execução

```powershell
# Iniciar toda a plataforma
.\start_tentacles.ps1

# Setup inicial (1ª vez)
.\setup.ps1

# Criar novo tentáculo
python scripts/new_tentacle.py <nome> "<descricao>" [--mcp] [--color "#RRGGBB"]

# Forçar delegação manual (útil para debug)
python scripts/delegate_task.py --agent google-assistant --prompt "..." --task_id debug-001

# Rodar autenticação Google (se token expirar)
python mcp_servers/google_mcp/auth.py
```

## Arquitetura do Gráfico de Orquestração

- **Hierarquia:** `octogent/apps/web/src/app/hooks/useCanvasGraphData.ts`
  - Usa `parentTerminalId` para criar linhas Pai → Filho
  - Sem `parentTerminalId`: conecta ao Octoboss central
- **Curvatura das linhas:** `octogent/apps/web/src/components/canvas/OctopusNode.tsx`
- **Animações (bolinhas):** `octogent/apps/web/src/components/CanvasPrimaryView.tsx`

> **CRÍTICO:** `INITIAL_PROMPT_DELAY_MS` está aumentado de 4s → 12s em `octogent/dist/api/createApiServer-*.js`. Se o Octogent for reinstalado, reaplicar essa mudança.

## Estado Atual (09/05/2026)

### ✅ Implementado
- Orquestração visual completa com 8 tentáculos no Dashboard
- Bridge Telegram ↔ Dashboard ↔ Agente (polling de status)
- Google Assistant totalmente funcional (Gmail, Calendar, Sheets)
- Files Assistant funcional (PDF, PPTX)
- Fábrica de Reels rebrandeada e com MCP de transcrição
- Orchestrator com `delegate_to_agent()` e script de delegação forçada
- Platform Infra com diagnóstico de saúde do sistema
- Multi-LLM via `/brain` no Telegram (Grok, Groq, Gemini)
- Log de atividade + canal `tentacles-events`

### 🔴 Pendente
- LinkedIn Poster: integração completa com o Orchestrator
- Confirmação de tarefa no Telegram ainda genérica (não usa "OK|mensagem")
- Trends Intelligence: reativar modo loop

## Regras para Claude

1. **SEMPRE leia este CLAUDE.md primeiro**
2. **NUNCA scan completo** — use `grep_search` ou `list_dir` pontual
3. **Credenciais Google:** nunca commitar `token.json` ou `client_secret.json`
4. **Outputs:** PDFs → `outputs/pdfs/`, PPTX → `outputs/presentations/`
5. **API Octogent:** sempre `http://127.0.0.1:8787` — não usar subprocess sem `shell=True`
6. **IPC Bridge:** `outputs/.status/{task_id}.done` — o agente filho grava `OK|mensagem`
7. **Delegação:** usar `scripts/delegate_task.py` para forçar abertura de terminal real
8. **LinkedIn MCP:** está em `mcp_servers/linkedin_mcp/` (com underscore), não `linkedin-poster/`
