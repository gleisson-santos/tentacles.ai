# Clilink — Plataforma de Agentes de Produtividade (GEMINI.md)

## Objetivo
Sistema multi-agente que automatiza: postagem LinkedIn, gestão de Gmail/Calendar/Sheets, criação de PDFs/PPTX e chatbot Telegram — tudo orquestrado via Gemini CLI / Claude Code + Octogent dashboard.

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
| trends-intelligence | `scripts/trends_monitor.py` | Monitoramento contínuo de notícias e tendências (2h loop) |
| files-assistant | `mcp_servers/files_mcp/server.py` | Criação de PDFs e apresentações PowerPoint |
| google-assistant | `mcp_servers/google_mcp/server.py` | Gmail, Google Calendar e Google Sheets |
| linkedin-poster | `auto_poster.py` | Auto-post LinkedIn a cada 2h (Groq + Stability AI) |
| orchestrator | `.claude/skills/proactive-agent.md` | Coordenador central, monitora canal `clilink-events` |
| platform-infra | — | `start_clilink.ps1` — launcher que sobe todos os serviços |
| telegram-bot | `bots/telegram_bot.py` | Interface Telegram → detecta intenção → executa via Dashboard |

## Estrutura de Arquivos Principais
```
Clilink/
├── CLAUDE.md                          ← Referência para Claude Code
├── GEMINI.md                          ← LEIA PRIMEIRO (Instruções para Gemini CLI)
├── auto_poster.py                     ← Loop LinkedIn (2h)
├── linkedin_mcp_server.py             ← MCP LinkedIn
├── mcp_servers/                       ← Servidores MCP (Google, Files)
├── bots/                              ← Bot Telegram
├── scripts/                           ← Utilitários (new_tentacle, sync_tentacles)
├── logs/                              ← Logs de atividade
├── outputs/                           ← Arquivos gerados (PDFs, PPTX)
└── .claude/                           ← Skills e configurações de agentes
```

## Comandos de Execução Comuns

```powershell
# Instalar dependências
pip install -r requirements.txt

# LinkedIn auto-poster
python auto_poster.py

# Telegram Bot
python bots/telegram_bot.py

# Dashboard Octogent
octogent

# Setup Google OAuth2
python mcp_servers/google_mcp/auth.py

# Criar novo tentáculo
python scripts/new_tentacle.py <nome> "<descricao>" [--mcp] [--color "#RRGGBB"]
```

## Arquitetura Bridge (Telegram → Octogent)
O bot do Telegram detecta intenções e se comunica com o Octogent via API HTTP (porta 8787). O Octogent orquestra a execução via Claude Code/Gemini CLI. Os resultados são comunicados via arquivos `.done` em `outputs/.status/`.

## Regras e Convenções para Gemini CLI
1. **Prioridade de Contexto:** Sempre consulte `GEMINI.md` e `CLAUDE.md` para entender o estado atual e as regras do projeto.
2. **Segurança de Credenciais:** Nunca versione ou exiba segredos. Atenção especial a `mcp_servers/google_mcp/credentials/` e arquivos `.env`.
3. **Gerenciamento de Arquivos:** Use `grep_search` e `glob` para buscas pontuais. Evite ler muitos arquivos simultaneamente para economizar contexto.
4. **Localização de Saídas:**
   - PDFs: `outputs/pdfs/`
   - PPTX: `outputs/presentations/`
   - Status de tarefas: `outputs/.status/`
5. **Integração Octogent:** Interações com o Dashboard devem preferencialmente usar a API HTTP `http://127.0.0.1:8787`.
6. **Scripts de Manutenção:** Ao adicionar novos agentes ou funcionalidades, utilize `scripts/new_tentacle.py` e mantenha a documentação sincronizada com `scripts/sync_tentacles.py` (se aplicável).
7. **Estilo de Código:** Siga o padrão idiomático Python 3.14 e utilize as abstrações de logging definidas em `logs/logger.py`.

## Estado Atual e Próximos Passos
Consulte a seção correspondente no `CLAUDE.md` para a atualização mais recente do status de desenvolvimento.
