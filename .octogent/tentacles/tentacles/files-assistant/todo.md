# Files Assistant — Todo

## Backlog
- [ ] Adicionar `pdf_invoice(...)` para notas fiscais e orçamentos
- [ ] Implementar `pdf_report(data_json, title)` para relatórios com tabelas e gráficos
- [ ] Adicionar upload automático para Google Drive após criar arquivo
- [ ] Criar `pptx_from_outline(outline_text)` que converte texto livre em slides
- [ ] Adicionar suporte a logo personalizada nos PDFs e PPTXs
- [ ] Implementar preview de thumbnail antes de enviar o arquivo
- [ ] Adicionar `pdf_merge(paths_json)` para combinar PDFs existentes

## Concluído
- [x] MCP Server com 5 ferramentas (PDF + PPTX)
- [x] PDF genérico, contrato e currículo
- [x] PPTX com 4 tipos de slide (title, content, section, closing)
- [x] Diretórios outputs/ criados automaticamente
- [x] Integração Telegram: gera conteúdo com Groq e envia arquivo no chat
- [x] Registrado no settings.local.json
