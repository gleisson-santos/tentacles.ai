# LinkedIn Poster — Todo

## Em andamento
- [ ] Monitorar estabilidade do loop de 2h em produção

## Backlog
- [ ] Adicionar detecção de posts duplicados (evitar repetir tema da última postagem)
- [ ] Implementar fila de tópicos para não repetir o mesmo tópico nas últimas 5 postagens
- [ ] Adicionar suporte a carrossel (múltiplas imagens) para maior engajamento
- [ ] Criar relatório semanal de performance (likes, comentários) via Sheets
- [ ] Adicionar webhook de notificação no Telegram quando post for publicado
- [ ] Testar fallback de imagem quando Stability AI falhar (usar placeholder)

## Concluído
- [x] Loop principal de 2h com Groq AI
- [x] Geração de imagem com Stability AI
- [x] Fallback via template quando Groq cair
- [x] Log em `logs/activity.log`
- [x] Notificação no canal Octogent após publicação
- [x] MCP Server registrado no settings.local.json
