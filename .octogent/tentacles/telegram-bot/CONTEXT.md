# Telegram Bot

## Scope
Interface de usuário via Telegram. Recebe mensagens, detecta intenção com Groq AI e executa ações reais nos outros agentes (Gmail, Calendar, Sheets, PDF, PPTX, LinkedIn). Envia eventos para o canal Octogent `clilink-events`.

## Key Files
- `bots/telegram_bot.py` — bot principal
- `logs/logger.py` — log local + bridge Octogent

## Configuração
- Token: variável `TELEGRAM_BOT_TOKEN` (default hardcoded)
- User ID autorizado: `205798346` (único usuário permitido)
- Groq Model: `llama-3.3-70b-versatile`
- Canal Octogent: `clilink-events`

## Fluxo de uma mensagem
```
Usuário → Telegram
    → detect_intent() via Groq (JSON com intent + params)
    → roteamento por intent:
        gmail_list/summarize  → gmail_tools.list_emails()
        calendar_today/list   → calendar_tools.get_today_schedule()
        calendar_create       → calendar_tools.create_event()
        sheets_list           → sheets_tools.list_spreadsheets()
        pdf_create            → pdf_tools.create_pdf() + envia arquivo
        pptx_create           → pptx_tools.create_presentation() + envia arquivo
        linkedin_post         → Groq gera texto do post
        general               → Groq responde diretamente
    → log_octogent() → canal clilink-events
    → resposta ao usuário
```

## Comandos disponíveis
- `/start` — menu principal
- `/gmail` — lista 10 emails recentes
- `/agenda` — agenda de hoje
- `/planilhas` — lista planilhas do Drive
- `/linkedin` — inicia fluxo de criação de post
- `/pdf` — inicia criação de PDF (pergunta o assunto)
- `/pptx` — inicia criação de apresentação (pergunta o assunto)

## Key Decisions
- Intenção detectada por Groq (não por keywords simples) para suportar linguagem natural
- Arquivos PDF/PPTX enviados diretamente no chat via `reply_document`
- Contexto de múltiplos turnos via `context.user_data["pending"]` para /pdf e /pptx
- Markdown habilitado nas respostas
- Mensagens >4000 chars divididas automaticamente

## Related Tentacles
- `google-assistant` — chama gmail_tools, calendar_tools, sheets_tools diretamente
- `files-assistant` — chama pdf_tools, pptx_tools diretamente
- `linkedin-poster` — gera posts via Groq (sem publicar automaticamente)
- `orchestrator` — recebe resumo das ações via canal clilink-events
