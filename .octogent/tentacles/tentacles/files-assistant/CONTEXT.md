# Files Assistant — CONTEXT

## Scope
Criação de documentos profissionais: PDFs (genérico, contrato, currículo) e apresentações PowerPoint. Expõe ferramentas via MCP Server e via chamadas diretas do Telegram Bot. Arquivos gerados salvos em `outputs/`.

## Key Files
- `mcp_servers/files_mcp/server.py` — MCP Server (5 ferramentas)
- `mcp_servers/files_mcp/pdf_tools.py` — geração de PDFs com reportlab
- `mcp_servers/files_mcp/pptx_tools.py` — geração de PPTX com python-pptx
- `outputs/pdfs/` — PDFs gerados
- `outputs/presentations/` — PPTX gerados

## Key Decisions
- Diretórios `outputs/pdfs/` e `outputs/presentations/` criados automaticamente
- Nomes de arquivo gerados automaticamente com timestamp se não especificados
- Conteúdo dos documentos gerado via Groq AI antes de criar o arquivo
- Telegram Bot envia o arquivo diretamente no chat após criação

## Ferramentas MCP disponíveis
### PDF
- `pdf_create(title, sections_json, filename?)` — PDF genérico
  - `sections_json`: `[{"heading":"Título","body":"Texto..."}]`
- `pdf_contract(title, party_a, party_b, clauses_json, date, filename?)` — contrato profissional
- `pdf_resume(name, contact_json, summary, experience_json, education_json, skills_json, filename?)` — currículo

### PowerPoint
- `pptx_create(title, slides_json, filename?)` — apresentação completa
  - Tipos de slide: `title | content | section | closing`
  - `slides_json`: `[{"type":"title","title":"...","subtitle":"..."}]`
- `pptx_add_slide(pptx_path, slide_json)` — adiciona slide a PPTX existente

## Paleta visual PPTX
- Fundo: azul escuro `#1A1A2E`
- Accent: azul LinkedIn `#0077B5`
- Destaque: laranja `#FAA32C`
- Texto: branco `#FFFFFF`

## Related Tentacles
- `telegram-bot` — aciona criação via /pdf e /pptx
- `orchestrator` — delega pedidos de documentos
- `google-assistant` — futura integração para upload no Drive
