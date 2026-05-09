# Telegram Bot

## Scope
Interface de comando via Telegram com detecção de intenção. Atua como o ponto de entrada principal para o usuário final, orquestrando execuções locais ou via Dashboard.

## Responsabilidades
- **Interface Homem-Máquina:** Gerenciar a comunicação bidirecional com o usuário.
- **Detecção de Intenção:** Processar mensagens naturais para identificar ações (Gmail, Calendar, PDFs, etc).
- **Orquestração de Tarefas:** Decidir entre execução local síncrona ou delegação para agentes especializados via Octogent Dashboard.
- **Monitoramento de Status:** Acompanhar a conclusão de tarefas assíncronas e entregar resultados (arquivos, confirmações).
- **Gestão de Configuração:** Prover comandos para ajustar o provedor e modelo de IA global (/brain).

## Comandos Disponíveis
- `/start` — Menu inicial e boas-vindas.
- `/gmail` — Listagem de e-mails recentes.
- `/agenda` — Compromissos de hoje no Google Calendar.
- `/planilhas` — Listagem de planilhas no Google Sheets.
- `/linkedin` — Menu para criação de posts ou análise de tendências.
- `/pdf` — Gatilho para criação de documento PDF (via Dashboard).
- `/pptx` — Gatilho para criação de apresentação PowerPoint (via Dashboard).
- `/brain` — Configuração do cérebro universal (OpenRouter/Groq/Gemini).

## Ferramentas (Agente)
- **Telegram SDK:** `python-telegram-bot` para interface de chat e envio de documentos.
- **OpenRouter/Groq:** Motor de inferência para detecção de intenção.
- **LLM Bridge:** `mcp_servers/llm_bridge/server.py` para gestão centralizada de modelos.
- **Octogent API Bridge:** Criação de terminais dinâmicos via `http://127.0.0.1:8787/api/terminals`.
- **Google Workspace SDKs:** Acesso via `gmail_tools`, `calendar_tools` e `sheets_tools`.
- **Document Tools:** Fallback local com `pdf_tools` e `pptx_tools`.

## Key Files
- `bots/telegram_bot.py` — Código principal do bot, handlers e lógica de bridge.
- `logs/logger.py` — Sistema de log centralizado (log e log_octogent).
- `mcp_servers/llm_bridge/server.py` — Gestão de modelos de IA e chaves de API.
- `outputs/.status/` — Pasta onde são monitorados arquivos `.done` para retorno de tarefas do Dashboard.

## Key Decisions
- **Híbrido de Execução:** Consultas rápidas (Gmail/Calendar) são feitas localmente. Tarefas longas ou complexas (PDF, PPTX, análise de tendências) são delegadas ao Dashboard para evitar travamento do bot (polling).
- **Dashboard Bridge:** O bot cria um terminal no Dashboard com um prompt específico e monitora a criação de um arquivo `{terminal_id}.done` em `outputs/.status/` para saber quando a tarefa terminou.
- **Segurança:** Bloqueio por ID de usuário fixo (`ALLOWED_USER_ID`) definido no `.env`.

## Conventions
- Usar `log_octogent` para eventos visíveis no Dashboard.
- Todas as mensagens de resposta devem ser em Português (Brasil).

## Related Tentacles
- `orchestrator` — Coordenador principal.
- `files-assistant` — Delegado via Dashboard para criação de documentos complexos.
- `linkedin-poster` — Delegado via Dashboard para análise de tendências e postagens automáticas.

