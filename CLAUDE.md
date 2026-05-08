# Tentacles — Plataforma de Agentes de Produtividade

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
| agent-skills | `mcp_servers/agent-skills/server.py` | Repositório de comportamentos e instruções detalhadas de ... |
| files-assistant | `mcp_servers/files-assistant/server.py` | Criação de documentos profissionais (PDF e PowerPoint) vi... |
| google-assistant | `mcp_servers/google-assistant/server.py` | Gerenciamento de Gmail, Google Calendar e Google Sheets v... |
| linkedin-poster | `mcp_servers/linkedin-poster/server.py` | Automação de postagens no LinkedIn com IA de texto e imagem. |
| orchestrator | `mcp_servers/orchestrator/server.py` | Coordenador central do ecossistema Tentacles. Monitora ev... |
| platform-infra | `mcp_servers/platform-infra/server.py` | Infraestrutura de inicialização e monitoramento de serviços. |
| telegram-bot | `mcp_servers/telegram-bot/server.py` | Interface de comando via Telegram com detecção de intenção. |
| trends-intelligence | `mcp_servers/trends-intelligence/server.py` | Monitoramento contínuo de tendências e notícias via RSS/G... |





















































## Estrutura de Arquivos
```
Tentacles/
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
# Setup profissional (Python + Node + CLI Link)
./setup.ps1

# Iniciar plataforma completa
./start_tentacles.ps1

# Criar novo tentáculo
python scripts/new_tentacle.py <nome> "<descricao>" [--mcp] [--color "#RRGGBB"]
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

## Arquitetura do Gráfico de Orquestração (Hierarquia)

O Dashboard utiliza um sistema de grafos dinâmicos para visualizar a relação entre agentes:

1.  **Lógica de Hierarquia:** Localizada em `octogent/apps/web/src/app/hooks/useCanvasGraphData.ts`. 
    -   Utiliza o `parentTerminalId` dos terminais para deduzir a paternidade entre tentáculos.
    -   Se um tentáculo B possui um terminal cujo pai está no tentáculo A, o gráfico desenha uma linha de A para B.
    -   Caso contrário, o tentáculo é conectado ao `Octoboss` (nó central).

2.  **Visualização de Linhas (Edges):**
    -   **Curvatura (Bézier):** Definida em `octogent/apps/web/src/components/canvas/OctopusNode.tsx` via função `buildEdgePath`. Utiliza curvas quadráticas para um visual orgânico.
    -   **Filtro de Duplicidade:** Implementado em `CanvasPrimaryView.tsx` usando um mapa `uniqueEdges` para evitar múltiplas linhas entre os mesmos dois nós.

3.  **Animações e Cores:**
    -   **Atividade:** Pequenos pontos coloridos que percorrem as linhas usando SVG `animateMotion`.
    -   **Cores:** Os tentáculos herdam cores definidas no Deck ou geradas aleatoriamente via `hashString(tentacleId)`.
    -   **Status:** As bordas e expressões dos polvos mudam conforme o `AgentState` (idle, active, blocked).

## Estado Atual (06/05/2026)
- ✅ LinkedIn auto-poster funcionando (Groq AI, 2h intervalo)
- ✅ Google MCP Server criado e configurado (Gmail, Calendar, Sheets funcionais)
- ✅ Files MCP Server criado (PDF + PPTX funcionando)
- ✅ Telegram Bot funcionando com detecção de intenção (Gmail, Calendar, Sheets, PDF, PPTX, LinkedIn)
- ✅ Octogent Dashboard rodando com 7 tentáculos configurados
- ✅ Bridge Telegram → Dashboard implementada via API HTTP
- ✅ Sistema de log em `logs/activity.log` + canal `Tentacles-events`
- ✅ Scripts de automação em `scripts/` (new_tentacle, sync_tentacles)
- ✅ Monitoramento de Tendências (Trends Intelligence) migrado para lógica orientada a Agente (Terminal)
- ✅ Suporte multi-CLI (Claude Code / Gemini CLI / Tentacles Agent) configurável via Settings no Dashboard
- ✅ Persistência de configurações do 'Universal Brain' (Multi-LLM) integrada ao Dashboard e .env
- ✅ Bridge Telegram↔Dashboard aprimorada com polling de status e retorno automático de arquivos
- ✅ Correção de SyntaxError no Telegram Bot e melhoria na resiliência da Bridge
- ✅ Monitoramento de Tendências (Trends Intelligence) agora opera em modo contínuo (--loop) via Agente
- ✅ Limpeza automática de terminais obsoletos no Dashboard para melhor organização


## Próximos Passos
1. **Validar animações** — Confirmar se o tentáculo Trends Intelligence permanece animado durante todo o processo de resumo.
2. **Múltiplas tarefas simultâneas** — Implementar `asyncio.create_task()` para paralelismo no bot.


## Regras para Claude
1. **SEMPRE leia este CLAUDE.md primeiro** — contém todo o estado do projeto
2. **NUNCA faça scan completo** — use Glob/Grep pontual
3. **MCP principal:** `mcp_servers/google_mcp/server.py` e `mcp_servers/files_mcp/server.py`
4. **Credenciais Google:** nunca commitar `credentials/token.json` ou `client_secret.json`
5. **Outputs:** PDFs → `outputs/pdfs/`, PPTX → `outputs/presentations/`
6. **Octogent API:** sempre via HTTP `http://127.0.0.1:8787` — subprocess não funciona no Windows sem shell=True
7. **Arquivo de status bridge:** `outputs/.status/{task_id}.done` — mecanismo de IPC entre Dashboard e bot
