# Telegram Bot — Todo

## Backlog
- [ ] Adicionar comando `/publicar` que aciona `auto_poster.py` manualmente (publica no LinkedIn agora)
- [ ] Implementar `/resumo` — envia diário às 8h com emails + agenda do dia + próximos eventos
- [ ] Adicionar intent `gmail_send` para enviar emails por voz/texto natural
- [ ] Criar intent `calendar_create` com confirmação antes de salvar o evento
- [ ] Adicionar suporte a `/status` que mostra estado dos agentes (LinkedIn poster rodando? último post?)
- [ ] Implementar inline keyboard para confirmar ações destrutivas (delete email, delete evento)
- [ ] Adicionar `/relatorio` que cria PDF semanal de atividades e envia no chat
- [ ] Criar intent `sheets_read` para consultar dados de planilhas específicas

## Concluído
- [x] Detecção de intenção via Groq AI (8 intents + general)
- [x] Gmail: listar e resumir emails reais
- [x] Calendar: agenda hoje, próximos eventos, criar evento
- [x] Sheets: listar planilhas
- [x] PDF: gera com Groq + envia arquivo no chat
- [x] PPTX: gera com Groq + envia arquivo no chat
- [x] LinkedIn: gera post pronto para copiar
- [x] Bridge Octogent: envia eventos para canal clilink-events
- [x] Proteção por User ID (só gleisson)
- [x] Log em activity.log
