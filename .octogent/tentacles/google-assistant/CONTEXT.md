# Google Assistant

## Scope
Integração completa com Gmail, Google Calendar e Google Sheets via OAuth2. Expõe ferramentas via MCP Server (FastMCP) para Claude Code e via chamadas diretas do Telegram Bot.

## Key Files
- `mcp_servers/google_mcp/server.py` — MCP Server principal (14 ferramentas)
- `mcp_servers/google_mcp/auth.py` — OAuth2 setup (rodar 1x para gerar token)
- `mcp_servers/google_mcp/gmail_tools.py` — funções Gmail
- `mcp_servers/google_mcp/calendar_tools.py` — funções Calendar
- `mcp_servers/google_mcp/sheets_tools.py` — funções Sheets
- `mcp_servers/google_mcp/credentials/token.json` — token OAuth2 (não commitar)
- `mcp_servers/google_mcp/credentials/client_secret.json` — app credentials (não commitar)

## Scopes OAuth2 ativos
- `gmail.modify` — ler, enviar, deletar emails
- `calendar` — criar, editar, deletar eventos
- `spreadsheets` — ler e escrever planilhas
- `drive.readonly` — listar arquivos no Drive

## Key Decisions
- Token é salvo em `credentials/token.json` e renovado automaticamente
- Se token expirar, `get_credentials()` usa refresh_token automaticamente
- MCP Server usa stdio transport (registrado no settings.local.json)
- Fuso horário: America/Sao_Paulo (UTC-3) para Calendar

## Ferramentas MCP disponíveis
### Gmail
- `gmail_list(max_results)` — lista emails recentes
- `gmail_read(email_id)` — lê email completo
- `gmail_send(to, subject, body)` — envia email
- `gmail_delete(email_id)` — move para lixeira
- `gmail_summarize(max_emails)` — resumo da caixa de entrada

### Calendar
- `calendar_list(days_ahead)` — próximos eventos
- `calendar_today()` — agenda de hoje
- `calendar_create(title, start, end, description, location)` — cria evento
- `calendar_update(event_id, ...)` — atualiza evento
- `calendar_delete(event_id)` — remove evento

### Sheets
- `sheets_list()` — lista planilhas no Drive
- `sheets_read(spreadsheet_id, range_name)` — lê dados
- `sheets_write(spreadsheet_id, range_name, values_json)` — escreve dados
- `sheets_append(spreadsheet_id, sheet_name, row_json)` — adiciona linha
- `sheets_create(title, headers_json)` — cria planilha nova

## Related Tentacles
- `telegram-bot` — chama ferramentas diretamente via import
- `orchestrator` — delega pedidos Gmail/Calendar/Sheets
