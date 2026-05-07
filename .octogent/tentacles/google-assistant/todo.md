# Google Assistant — Todo

## Em andamento
- [ ] Validar fluxo OAuth2 completo com token real

## Backlog
- [ ] Adicionar `gmail_search(query)` para busca avançada por remetente/assunto
- [ ] Implementar `gmail_label(email_id, label)` para organizar emails
- [ ] Adicionar `calendar_find_free_slot(duration_minutes)` para sugerir horários livres
- [ ] Criar `sheets_create_report(data, title)` para relatórios automáticos
- [ ] Implementar log de ações Google em `logs/activity.log` via logger compartilhado
- [ ] Adicionar suporte a Google Drive upload (para PDFs gerados)
- [ ] Criar resumo diário automático (emails + agenda) via Telegram às 8h

## Concluído
- [x] MCP Server com 14 ferramentas (Gmail + Calendar + Sheets)
- [x] OAuth2 com renovação automática de token
- [x] Integração direta no Telegram Bot (chamada sem passar pelo MCP)
- [x] Registrado no settings.local.json
- [x] Credentials OAuth2 configuradas
