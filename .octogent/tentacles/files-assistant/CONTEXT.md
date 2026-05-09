# Files Assistant

## Scope
Criação de documentos profissionais (PDF e PowerPoint) via MCP. O agente é responsável por transformar dados estruturados em arquivos visuais de alta qualidade, seguindo a identidade visual Clilink.

## Key Files
- `mcp_servers/files_mcp/server.py` — Servidor MCP Principal (FastMCP)
- `mcp_servers/files_mcp/pdf_tools.py` — Lógica de geração de PDFs (ReportLab)
- `mcp_servers/files_mcp/pptx_tools.py` — Lógica de geração de PowerPoint (python-pptx)
- `scripts/generate_ww2_pdf.py` — Script customizado para PDF histórico vibrante
- `scripts/generate_timesheet.py` — Script customizado para planilha de ponto Excel
- `scripts/generate_ai_pptx.py` — Script customizado para apresentação de IA corporativa
- `outputs/pdfs/` — Diretório de saída para PDFs
- `outputs/planilhas/` — Diretório de saída para planilhas Excel
- `outputs/presentations/` — Diretório de saída para PPTX

## Responsabilidades
- **Geração de Documentos Genéricos:** Criar PDFs a partir de seções de texto e cabeçalhos.
- **Documentos Especializados:** Criar contratos formais e currículos profissionais com layouts otimizados.
- **Apresentações Visuais:** Criar e editar apresentações PowerPoint (slides de título, conteúdo, seções e encerramento).
- **Consistência Visual:** Garantir que os documentos sigam padrões profissionais de formatação e cores.

## Ferramentas MCP disponíveis (files-assistant)

### PDF Tools
- `pdf_create(title, sections_json, filename)`: Cria um PDF genérico.
    - `sections_json`: `[{"heading": "Título", "body": "Texto..."}]`
- `pdf_contract(title, party_a, party_b, clauses_json, date, filename)`: Cria um contrato formal.
    - `clauses_json`: `["Cláusula 1...", "Cláusula 2..."]`
- `pdf_resume(name, contact_json, summary, experience_json, education_json, skills_json, filename)`: Cria um currículo profissional.
    - `contact_json`: `{"email": "...", "phone": "...", "linkedin": "...", "city": "..."}`
    - `experience_json`: `[{"company": "...", "role": "...", "period": "...", "description": "..."}]`
    - `education_json`: `[{"institution": "...", "degree": "...", "period": "..."}]`
    - `skills_json`: `["Python", "React", "..."]`

### PowerPoint Tools
- `pptx_create(title, slides_json, filename)`: Cria uma apresentação completa.
    - `slides_json`: Lista de objetos com `type` (`title`, `content`, `section`, `closing`) e dados específicos.
- `pptx_add_slide(pptx_path, slide_json)`: Adiciona um slide a um arquivo existente.

## Identidade Visual (PowerPoint)
A paleta de cores padrão Clilink utilizada nas apresentações é:
- **DARK:** `#1A1A2E` (Fundo de títulos e encerramento)
- **BLUE:** `#0077B5` (Headers e seções)
- **ACCENT:** `#FAA32C` (Destaques e subtítulos)
- **WHITE:** `#FFFFFF` (Fundo de conteúdo)

## Key Decisions
- Utilização de `FastMCP` para exposição simplificada das ferramentas.
- Separação de lógica de ferramentas (`*_tools.py`) do servidor MCP (`server.py`).
- Uso de JSON strings para passar estruturas complexas via MCP.
- Layout de currículo utiliza azul Clilink (`#0077B5`) para cabeçalhos e divisores.

## Conventions
- Nomes de arquivos devem ser sanitizados (geralmente lowercase com underscores).
- Caminhos de saída são centralizados em `outputs/`.
- O servidor MCP deve ser executado a partir da raiz do projeto para correta resolução de módulos.

## Related Tentacles
- `orchestrator` — Coordenador principal que solicita a criação de documentos.
- `trends-intelligence` — Fornece dados analíticos para relatórios e apresentações.

