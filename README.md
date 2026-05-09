# 🐙 Tentacles.AI — Multi-Agent Productivity Platform

<div align="center">

**Uma plataforma de agentes de IA que trabalham juntos para automatizar sua vida digital.**

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-22-green?logo=node.js)](https://nodejs.org)
[![FastMCP](https://img.shields.io/badge/MCP-FastMCP-purple)](https://github.com/jlowin/fastmcp)
[![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20OpenRouter-orange)](https://groq.com)
[![Octogent](https://img.shields.io/badge/Dashboard-Octogent-blueviolet)](https://octogent.com)

</div>

---

## 🌟 Visão do Projeto

**Tentacles.AI** é uma plataforma de automação inteligente construída sobre o **Protocolo MCP (Model Context Protocol)** e o **Dashboard Octogent**. Ela funciona como um "polvo digital" — um coordenador central (Octoboss) com múltiplos tentáculos especializados, cada um sendo um agente autônomo com ferramentas reais.

A proposta é simples: você escreve uma mensagem no **Telegram** como faria com um assistente humano. A plataforma detecta sua intenção, roteia para o agente correto, executa a tarefa com IA de verdade e te envia a confirmação — tudo enquanto você observa a "dança dos tentáculos" no Dashboard.

```
"Envia um email para João confirmando a reunião de amanhã"
        ↓ Telegram Bot detecta intenção
        ↓ Orchestrator assume e delega
        ↓ Google Assistant abre, executa, confirma
        ✅ "E-mail enviado para João com sucesso!" (no Telegram)
```

---

## 🏗️ Arquitetura Multi-Agente

```
┌─────────────────────────────────────────────────────────────────┐
│                    OCTOGENT DASHBOARD (porta 8787)              │
│                                                                 │
│                         🐙 Octoboss                            │
│                        (Coordenador)                           │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐              │
│         │           │       │       │            │              │
│    🎭 Orchestrator  │  📧 Google   │  📄 Files  │              │
│    (Maestro)        │  Assistant  │  Assistant  │              │
│         │           │             │             │              │
│         │      📱 Telegram   🎬 Reels    💼 LinkedIn           │
│         │           Bot     Factory      Poster                │
│         │                                                       │
│    🛠️ Platform   📚 Agent                                      │
│       Infra       Skills                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo de Dados Principal

```
[Usuário] → [Telegram] → [Bot (intenção)] → [Orchestrator]
                                                    ↓
                                        [Agente Especializado]
                                        (Google/Files/LinkedIn)
                                                    ↓
                                        [outputs/.status/*.done]
                                                    ↓
                                [Telegram] ← [Confirmação] ← [Bot]
```

---

## 🦑 Os 8 Tentáculos

### 🎭 Orchestrator (O Maestro)
**Papel:** Coordenador central que analisa contexto e delega tarefas para os agentes especializados sem executar nada diretamente.

**Ferramentas MCP:**
- `get_last_activity(lines)` — Lê o log de atividade para entender o contexto
- `delegate_to_agent(agent_id, instruction)` — Abre terminal no Dashboard para o agente alvo

**Regra de Ouro:** O Orchestrator **nunca** envia e-mails, cria arquivos ou acessa APIs diretamente. Ele apenas delega.

---

### 📧 Google Assistant (O Administrador)
**Papel:** Gerencia toda a suíte Google — emails, calendário e planilhas.

**Ferramentas MCP:**
| Ferramenta | Ação |
|-----------|------|
| `list_emails(max_results)` | Lista emails recentes |
| `read_email(message_id)` | Lê conteúdo completo |
| `send_email(to, subject, body)` | Envia email |
| `delete_email(message_id)` | Move para lixeira |
| `summarize_inbox()` | Resumo executivo da inbox |
| `get_today_schedule()` | Agenda do dia |
| `list_events(max_results)` | Próximos eventos |
| `create_event(title, start, end, ...)` | Cria evento no calendário |
| `list_spreadsheets()` | Lista planilhas no Drive |
| `read_spreadsheet(spreadsheet_id, range)` | Lê dados de planilha |
| `write_to_spreadsheet(...)` | Escreve em planilha |

**Auth:** OAuth2 via `mcp_servers/google_mcp/auth.py` → salva em `credentials/token.json`

---

### 📄 Files Assistant (O Criador de Documentos)
**Papel:** Gera documentos profissionais com conteúdo criado por IA.

**Ferramentas MCP:**
- `pdf_create(title, sections)` — PDF com seções formatadas → `outputs/pdfs/`
- `pptx_create(title, slides)` — PowerPoint com slides estruturados → `outputs/presentations/`

**Pipeline:** LLM gera estrutura JSON → Tools renderizam o documento → Bot envia o arquivo no Telegram

---

### 💼 LinkedIn Poster (O Publicitário)
**Papel:** Automatiza a presença no LinkedIn com posts ricos (texto + imagem gerada por IA).

**Ferramentas MCP:**
- `authenticate()` — OAuth2 LinkedIn (abre browser)
- `check_auth_status()` — Verifica token ativo
- `fetch_url_content(url)` — Scraping de artigos para inspiração
- `generate_image(prompt)` — Gera imagem com Stability AI ($0.03/img)
- `create_post(text, visibility)` — Publica post de texto
- `create_post_with_image(text, image_path)` — Publica post com imagem

**Auto-poster:** `auto_poster.py` executa ciclo completo a cada 2h (tendências → texto → imagem → post)

---

### 🎬 Fábrica de Reels (O Criador de Conteúdo)
**Papel:** Transforma vídeos do YouTube em roteiros otimizados para Reels/Shorts.

**Pipeline:**
```
URL YouTube → Transcrição → Análise por LLM → Roteiro para Reels
```

**Sem FFmpeg:** Trabalha com texto e roteiro, não com edição de vídeo diretamente.

---

### 🛠️ Platform Infra (O Engenheiro)
**Papel:** Monitoramento técnico da plataforma e gestão de recursos.

**Ferramentas MCP:**
- `check_platform_health()` — Status: Dashboard (8787), Bot, Monitor
- `get_system_resources()` — Uso de disco por pasta de output
- `cleanup_temp_files(days)` — Limpeza de arquivos antigos

---

### 📱 Telegram Bot (A Interface)
**Papel:** Porta de entrada para todos os serviços via linguagem natural.

**Intenções detectadas automaticamente:**
| Intenção | Exemplo |
|---------|---------|
| `gmail_send` | "Envia email para fulano@email.com sobre X" |
| `gmail_list` | "Mostra meus emails recentes" |
| `gmail_summarize` | "Resume minha inbox" |
| `calendar_today` | "O que tenho hoje?" |
| `calendar_create` | "Agenda reunião amanhã às 14h" |
| `sheets_list` | "Lista minhas planilhas" |
| `pdf_create` | "Cria um PDF sobre dieta cetogênica" |
| `pptx_create` | "Faz uma apresentação sobre IA" |
| `linkedin_post` | "Cria post LinkedIn sobre futuro da IA" |

**Comandos diretos:** `/gmail` `/agenda` `/planilhas` `/linkedin` `/pdf` `/pptx` `/brain`

---

### 📚 Agent Skills (O Manual)
**Papel:** Repositório de instruções detalhadas de comportamento para cada agente.

**Localização:** `.claude/skills/*.md` — cada arquivo é a "mente" de um tentáculo.

---

## 🔧 Stack Técnica Detalhada

### LLMs & IA
```
OpenRouter (grok-4.1-fast) ← LLM principal (velocidade + custo)
Groq (llama-3.3-70b)       ← LLM alternativo (fallback)
Stability AI (core)        ← Geração de imagens (~$0.03/img)
```

### Protocolo MCP (Model Context Protocol)
Todos os agentes expõem ferramentas via **FastMCP**, o que permite que LLMs como Claude e Gemini as utilizem nativamente sem precisar de código extra.

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("nome-do-agente")

@mcp.tool()
def minha_ferramenta(param: str) -> str:
    """Descrição que o LLM vai usar para decidir quando chamar."""
    return resultado
```

### Dashboard (Octogent)
Interface visual em tempo real que mostra os agentes como "polvos" animados em um grafo. Cada terminal aberto no Dashboard é um agente executando uma tarefa.

```
Comunicação:
POST http://127.0.0.1:8787/api/terminals  ← Cria terminal (abre agente)
GET  http://127.0.0.1:8787/api/ui-state   ← Estado atual da UI
```

### IPC Bridge (Telegram ↔ Dashboard)
```
Mecanismo de arquivos .done para sincronização assíncrona:
1. Bot cria terminal no Dashboard
2. Bot faz polling de outputs/.status/{task_id}.done
3. Agente executa e grava: "OK|Mensagem de sucesso" no .done
4. Bot lê e envia confirmação ao usuário
```

---

## 📁 Estrutura do Projeto

```
tentacles/
├── 📋 CLAUDE.md               ← Memória operacional (Claude)
├── 📋 GEMINI.md               ← Memória operacional (Gemini)
├── 📊 DEV_PROGRESS.md         ← Log de progresso e roadmap
│
├── 🤖 auto_poster.py          ← Loop LinkedIn autônomo
│
├── 🔌 mcp_servers/            ← Servidores MCP por agente
│   ├── google_mcp/            ← Gmail + Calendar + Sheets
│   ├── files_mcp/             ← PDF + PowerPoint
│   ├── linkedin_mcp/          ← LinkedIn + Stability AI
│   ├── reels-factory/         ← YouTube → Reels
│   ├── orchestrator/          ← Delegação inteligente
│   ├── platform-infra/        ← Monitoramento
│   └── llm_bridge/            ← Multi-LLM switcher
│
├── 📱 bots/
│   └── telegram_bot.py        ← Bot principal (12+ intenções)
│
├── 🛠️ scripts/
│   ├── delegate_task.py       ← Delegação forçada via API
│   ├── new_tentacle.py        ← Criador de agentes
│   ├── sync_tentacles.py      ← Sincronização de docs
│   └── trends_monitor.py      ← Monitor de tendências
│
├── 📝 logs/
│   ├── logger.py              ← Logger compartilhado
│   └── activity.log           ← Histórico de ações
│
├── 📦 outputs/
│   ├── pdfs/                  ← PDFs gerados
│   ├── presentations/         ← PPTX gerados
│   └── .status/               ← Bridge IPC
│
└── ⚙️ .octogent/
    ├── state/deck.json        ← Estado do Dashboard
    └── tentacles/             ← Contexto persistente por agente
```

---

## 🚀 Como Usar

### 1. Setup Inicial

```powershell
# Clonar e configurar
git clone <repo>
cd tentacles

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves

# Instalar dependências
.\setup.ps1
```

**Variáveis necessárias no `.env`:**
```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
ALLOWED_USER_ID=seu_telegram_id
OPENROUTER_API_KEY=sk-or-...
GROQ_API_KEY=gsk_...
STABILITY_KEY=sk-...
LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...
```

### 2. Autenticações OAuth2

```powershell
# Google (Gmail, Calendar, Sheets)
python mcp_servers/google_mcp/auth.py
# Abre browser, faz login, salva token.json

# LinkedIn
# Abrir agente linkedin-poster no Dashboard e rodar authenticate()
```

### 3. Iniciar a Plataforma

```powershell
.\start_tentacles.ps1
# Abre o Dashboard em http://localhost:8787
# Sobe o Bot do Telegram
# Inicia o Monitor de Tendências
```

### 4. Usar pelo Telegram

Fale naturalmente com o bot:
```
"Envia um email para fulano@gmail.com sobre a reunião de amanhã"
"Cria um PDF sobre marketing digital"
"Quais são meus compromissos de hoje?"
"Faz uma apresentação sobre inteligência artificial"
"Cria um post no LinkedIn sobre inovação tecnológica"
```

---

## 🧠 Integração com LLMs

O sistema suporta múltiplos providers via `/brain` no Telegram:

```
/brain grok       ← usa x-ai/grok-4.1-fast via OpenRouter
/brain groq       ← usa llama-3.3-70b via Groq  
/brain gemini     ← usa Gemini via Google
```

O **Claude Code** e o **Gemini CLI** são usados como "runtime" dos agentes no Dashboard — eles recebem os prompts e executam as tarefas usando as ferramentas MCP disponíveis.

---

## 🗺️ Roadmap

### Em Progresso 🟡
- [ ] Integração completa do LinkedIn Poster ao fluxo de orquestração
- [ ] Confirmação padronizada de tarefas via Telegram
- [ ] Trends Intelligence em modo loop contínuo

### Planejado 📋
- [ ] Múltiplas tarefas simultâneas no Bot (`asyncio.create_task`)
- [ ] Agente de WhatsApp (Evolution API)
- [ ] Memória persistente de preferências do usuário
- [ ] Dashboard com gráfico de produtividade semanal
- [ ] Notificações proativas via Telegram (lembretes, alertas)

### Futuro 🔮
- [ ] Geração de Reels com IA de vídeo (Runway, Pika)
- [ ] Integração com Notion / Obsidian
- [ ] Multi-usuário (ALLOWED_USER_IDs múltiplos)
- [ ] Análise de sentimento em emails
- [ ] Agente de monitoramento de concorrentes

---

## 🔐 Segurança

> **IMPORTANTE:** Os seguintes arquivos contêm credenciais sensíveis e **NUNCA** devem ser commitados:

```
.env
mcp_servers/google_mcp/credentials/token.json
mcp_servers/google_mcp/credentials/client_secret.json
~/.linkedin_mcp_token.json
```

Todos já estão no `.gitignore`. Verifique antes de cada `git push`.

---

## 🤝 Diferenciais do Sistema

| Característica | Descrição |
|---------------|-----------|
| **Visual-First** | Veja os agentes trabalhando em tempo real no Dashboard |
| **MCP Nativo** | Ferramentas expostas como padrão aberto, não wrappers |
| **Multi-LLM** | Troca de provider em runtime via Telegram |
| **Orquestração Real** | Maestro delega → agentes filhos executam → confirmação automática |
| **Bridge Assíncrona** | IPC via arquivos .done — sem WebSockets, sem filas complexas |
| **Fallback Inteligente** | Se o Dashboard cair, o Bot executa localmente |
| **Log Unificado** | Toda ação registrada em `activity.log` + canal Octogent |

---

<div align="center">

**🐙 Tentacles.AI** — *Seu exército de agentes inteligentes, trabalhando em sincronia.*

</div>
