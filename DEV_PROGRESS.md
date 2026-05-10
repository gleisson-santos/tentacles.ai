# 🐙 Tentacles — Dev Progress Log

> Última atualização: 09/05/2026 — Sessão: Orquestração Visual & Delegação Multi-Agente

---

## ✅ O que está FUNCIONANDO (Consolidado)

### Plataforma & Dashboard
- [x] Octogent Dashboard rodando na porta `8787`
- [x] Gráfico de orquestração com 8 tentáculos visíveis
- [x] Animações de bolinha pulsando por agente ativo
- [x] Launcher `start_tentacles.ps1` sobe todos os serviços
- [x] Canal `tentacles-events` para comunicação entre agentes
- [x] Log global em `logs/activity.log`

### Telegram Bot
- [x] Bot rodando com detecção de intenção via LLM (OpenRouter / Groq)
- [x] Intenções reconhecidas: `gmail_list`, `gmail_send`, `gmail_summarize`, `calendar_today`, `calendar_list`, `calendar_create`, `sheets_list`, `pdf_create`, `pptx_create`, `linkedin_post`, `linkedin_analyze`, `general`
- [x] Bridge Telegram → Dashboard funcionando via API HTTP
- [x] **CORRIGIDO**: Bot 100% assíncrono (logger em thread separada, sem travas)
- [x] Polling de arquivo `.done` para confirmação de tarefa
- [x] Fallback local quando Dashboard está offline
- [x] Comando `/brain` para trocar LLM em runtime

### Google Assistant
- [x] MCP completo: Gmail, Calendar, Sheets
- [x] OAuth2 configurado e funcionando
- [x] Skill documentada com todas as ferramentas disponíveis
- [x] Envio de e-mails executado com sucesso via Telegram

### Files Assistant
- [x] Geração de PDF via `reportlab` + `pypdf`
- [x] Geração de PPTX via `python-pptx`
- [x] MCP completo com `pdf_create` e `pptx_create`
- [x] Outputs em `outputs/pdfs/` e `outputs/presentations/`

### Fábrica de Reels (ex-Content Recycler)
- [x] Rebranding completo (pasta, CONTEXT.md, skill, todo.md)
- [x] MCP com ferramentas de transcrição via YouTube
- [x] Sem dependência de FFmpeg

### Orchestrator
- [x] MCP com `get_last_activity()` e `delegate_to_agent()`
- [x] Skill atualizada com regras de delegação
- [x] CONTEXT.md com "Proibições de auto-execução"
- [x] Script `scripts/delegate_task.py` para forçar delegação real via API

### Platform Infra
- [x] MCP com `check_platform_health()`, `get_system_resources()`, `cleanup_temp_files()`
- [x] Verifica porta 8787, processos Python ativos, uso de disco

### LinkedIn Poster (MCP Existente — Integração Pendente)
- [x] MCP em `mcp_servers/linkedin_mcp/server.py` completamente implementado
  - `authenticate()` — OAuth2 LinkedIn
  - `check_auth_status()` — Verifica token
  - `fetch_url_content()` — Scraping de artigos
  - `generate_image()` — Stability AI
  - `create_post()` — Post texto puro
  - `create_post_with_image()` — Post com imagem
- [x] `auto_poster.py` com loop de 2h funcionando
- [x] **CORRIGIDO**: CONTEXT.md aponta para `mcp_servers/linkedin_mcp/`
- [x] Skill atualizada e integrada ao fluxo do Orchestrator via Telegram

---

## 🐛 Bugs Conhecidos

| Bug | Status | Local | Descrição |
|-----|--------|-------|-----------|
| Orchestrator auto-executa | ⚠️ Parcial | `bots/telegram_bot.py` | Mesmo com prompt proibindo, o agente às vezes usa sub-agent interno em vez da ferramenta |
| Confirmação Telegram | ⚠️ Parcial | Bridge `.done` | A confirmação genérica às vezes aparece antes do agente filho escrever a mensagem real |
| LinkedIn MCP path | 🟢 Fechado | `CONTEXT.md` | Aponta para pasta correta (`linkedin_mcp`) |
| `spawn_workers.js` | 🟢 Fechado | Raiz do projeto | Arquivo legado removido e no gitignore |

---

## 🔧 Pendências Técnicas

### Concluído Recente (Sprints 1, 2 e 3)
1. **LinkedIn Poster — Conectado ao Octogent** ✅
2. **Fluxo de Confirmação no Telegram** ✅ (Monitora task_id.done)
3. **Delegação Visual Estável** ✅ (parentTerminalId no Orchestrator)
4. - [x] **LIMPEZA**: Logs antigos (Clilink) removidos definitivamente
- [x] **GEMINI**: Agregador de uso injetando métricas reais no Dashboard
- [x] **GITHUB**: Dashboard integrado com `gh cli` (PATH corrigido e LIVE)
- [x] **KPIs**: Top-right metrics (Session/Week) preenchidos via Gemini Snapshot

### Média Prioridade
4. **Múltiplas tarefas simultâneas** — `asyncio.create_task()` no Bot
5. **Trends Intelligence** — Reativar monitoramento contínuo (loop)
6. **Limpeza automática de terminais** — Remover terminais antigos do Dashboard via API
7. **Tests** — `tests/` tem arquivos mas precisam de mais cobertura

### Baixa Prioridade
8. **Fábrica de Reels** — Integrar geração de roteiro com IA + publicação no Telegram
9. **Agent Skills** — Documentar melhor o repositório de skills

---

## 🚀 Próximos Passos (Para Hoje à Noite)

### Próxima Etapa: Refinamentos Finais
1. Integrar Fábrica de Reels (Roteiro via IA -> Telegram)
2. LinkedIn Poster: Finalizar skill e integração total
3. Agent Skills: Melhorar documentação do repositório

---

## 💡 Ideias Futuras

| Ideia | Complexidade | Impacto |
|-------|-------------|---------|
| Agente de memória persistente (lembra preferências do usuário) | Alta | Alto |
| Dashboard com gráfico de produtividade semanal | Média | Médio |
| Agente de WhatsApp (Evolution API) | Alta | Alto |
| Geração automática de Reels com IA de vídeo | Alta | Alto |
| Notificações proativas (ex: lembrete de calendário via Telegram) | Média | Alto |
| Análise de sentimento de e-mails | Baixa | Médio |
| Multi-usuário (mais de 1 ALLOWED_USER_ID) | Média | Médio |
| Integração com Notion/Obsidian | Média | Médio |

---

## 📦 Estado dos Agentes

| Agente | MCP | Skill | CONTEXT.md | Telegram | Status |
|--------|-----|-------|------------|---------|--------|
| Google Assistant | ✅ `google_mcp/` | ✅ Completa | ✅ Atualizado | ✅ | 🟢 Funcional |
| Files Assistant | ✅ `files_mcp/` | ✅ Completa | ✅ | ✅ | 🟢 Funcional |
| Fábrica de Reels | ✅ `reels-factory/` | ✅ Completa | ✅ | ⚠️ Parcial | 🟡 Em Progresso |
| Orchestrator | ✅ `orchestrator/` | ✅ Atualizada | ✅ Com proibições | ✅ | 🟡 Em Progresso |
| Platform Infra | ✅ `platform-infra/` | ✅ Atualizada | ⚠️ | — | 🟡 Em Progresso |
| LinkedIn Poster | ✅ `linkedin_mcp/` | ⚠️ Desatualizada | 🔴 Path errado | ⚠️ Parcial | 🔴 Incompleto |
| Telegram Bot | — | ✅ | ✅ | — | 🟢 Funcional |
| Agent Skills | ⚠️ | ⚠️ | ⚠️ | — | 🟡 Esqueleto |
