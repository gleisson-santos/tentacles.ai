# Tentacles — GEMINI.md (Memória Operacional para Gemini CLI)

## Objetivo
Sistema multi-agente que automatiza: postagem LinkedIn, gestão de Gmail/Calendar/Sheets, criação de PDFs/PPTX, transcrição YouTube → Reels, chatbot Telegram com intenção inteligente — tudo orquestrado visualmente via Octogent Dashboard.

## Tech Stack
- **LLM principal:** OpenRouter — `x-ai/grok-4.1-fast`
- **LLM alternativo:** Groq API — `llama-3.3-70b-versatile`
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
| `orchestrator` | `mcp_servers/orchestrator/server.py` | Coordenador central — delega tarefas via `delegate_task.py` |
| `google-assistant` | `mcp_servers/google_mcp/server.py` | Gmail, Calendar, Sheets (OAuth2 ativo) |
| `files-assistant` | `mcp_servers/files_mcp/server.py` | PDF + PowerPoint via MCP |
| `linkedin-poster` | `mcp_servers/linkedin_mcp/server.py` | Post LinkedIn com texto + imagem (Stability AI) |
| `reels-factory` | `mcp_servers/reels-factory/server.py` | Transcrição YouTube → roteiro Reels |
| `platform-infra` | `mcp_servers/platform-infra/server.py` | Diagnóstico de serviços (porta, disco, processos) |
| `telegram-bot` | `bots/telegram_bot.py` | Interface de comando + bridge para Dashboard |
| `agent-skills` | `.claude/skills/` | Repositório de comportamentos dos agentes |

## Estrutura de Arquivos Principais

```
tentacles/
├── CLAUDE.md / GEMINI.md              ← Memória operacional
├── DEV_PROGRESS.md                    ← Log de progresso (bugs, pendências, roadmap)
├── auto_poster.py                     ← Loop LinkedIn (2h)
│
├── mcp_servers/
│   ├── google_mcp/                    ← Gmail + Calendar + Sheets
│   ├── files_mcp/                     ← PDF + PPTX
│   ├── linkedin_mcp/                  ← LinkedIn (atenção: underscore, não hífen)
│   ├── reels-factory/                 ← YouTube → Reels
│   ├── orchestrator/                  ← Delegação (get_last_activity, delegate_to_agent)
│   ├── platform-infra/                ← Saúde do sistema
│   └── llm_bridge/                    ← Switcher multi-LLM
│
├── bots/telegram_bot.py               ← Bot Telegram com 12+ intenções
├── scripts/
│   ├── delegate_task.py               ← Força criação de terminal real no Dashboard
│   ├── new_tentacle.py                ← Cria novo tentáculo completo
│   └── trends_monitor.py             ← Monitor de tendências (loop)
│
├── logs/logger.py                     ← Log local + canal tentacles-events
└── outputs/.status/                   ← IPC: {task_id}.done com "OK|mensagem"
```

## Fluxo de Orquestração Principal

```
Telegram → Bot (intent detection) → Dashboard API → Orchestrator Terminal
    → scripts/delegate_task.py → Google Assistant Terminal
    → outputs/.status/{task_id}.done → Telegram ✅
```

## Arquitetura do Gráfico de Orquestração (Hierarquia)

- **Lógica de hierarquia:** `octogent/apps/web/src/app/hooks/useCanvasGraphData.ts`
- **Curvatura das lines:** `octogent/apps/web/src/components/canvas/OctopusNode.tsx`
- **Animações/bolinhas:** `octogent/apps/web/src/components/CanvasPrimaryView.tsx`

O sistema suporta Deep Nesting (Pai > Filho > Neto) via `parentTerminalId`.
Para manter agentes no círculo central (sem hierarquia), **não passar** `parentTerminalId`.

## Comandos de Execução Comuns

```powershell
# Iniciar todos os serviços
.\start_tentacles.ps1

# Setup inicial (1ª vez ou novo PC)
.\setup.ps1

# Criar novo tentáculo
python scripts/new_tentacle.py <nome> "<descricao>" [--mcp] [--color "#RRGGBB"]

# Delegar tarefa manualmente (debug)
python scripts/delegate_task.py --agent google-assistant --prompt "ENVIE EMAIL: ..." --task_id debug-01

# Autenticação Google (se token expirar)
python mcp_servers/google_mcp/auth.py
```

## Estado Atual (10/05/2026)

### ✅ Funcional
- Orquestração visual com 8 tentáculos
- Bridge Telegram ↔ Dashboard ↔ Agente
- Google Assistant (Gmail, Calendar, Sheets)
- Files Assistant (PDF, PPTX)
- Fábrica de Reels (rebrandeada, MCP ativo)
- Orchestrator + Platform Infra com MCPs reais
- Multi-LLM via `/brain` no Telegram
- **Trends Intelligence:** Monitoramento contínuo (30m) com busca exata
- **Octogent Analytics:** Integração de uso do Gemini e métricas GitHub LIVE

### 🔴 Pendente
- LinkedIn Poster: integração ao fluxo de delegação
- Confirmação "OK|mensagem" padronizada para todos os agentes filhos
- Fábrica de Reels: Integrar geração de roteiro com IA + publicação no Telegram

## Regras e Convenções para Gemini CLI

1. **Prioridade de Contexto:** Leia `CLAUDE.md` + `DEV_PROGRESS.md` antes de qualquer sessão
2. **Segurança:** Nunca versione `token.json`, `client_secret.json` ou `.env`
3. **Buscas:** Use `grep_search` e `list_dir` — evite ler muitos arquivos simultaneamente
4. **Outputs:** PDFs → `outputs/pdfs/` | PPTX → `outputs/presentations/` | Status → `outputs/.status/`
5. **API Octogent:** Sempre HTTP `http://127.0.0.1:8787` — não subprocess sem `shell=True`
6. **LinkedIn MCP:** `mcp_servers/linkedin_mcp/` (underscore!) — não confundir com `linkedin-poster/`
7. **Delegação:** Usar `scripts/delegate_task.py` para abrir terminais reais no Dashboard
8. **IPC:** Agente filho deve gravar `OK|mensagem` em `outputs/.status/{task_id}.done`
9. **Novos agentes:** Usar `scripts/new_tentacle.py` + atualizar `CLAUDE.md` e `DEV_PROGRESS.md`
