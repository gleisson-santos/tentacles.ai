"""
Files MCP Server — PDF + PowerPoint
Rode com: python mcp_servers/files_mcp/server.py
"""
import json
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__file__))))

from mcp.server.fastmcp import FastMCP
from mcp_servers.files_mcp import pdf_tools, pptx_tools

mcp = FastMCP("files-assistant")

# ── PDF ────────────────────────────────────────────────────────────────────────

@mcp.tool()
def pdf_create(title: str, sections_json: str, filename: str = None) -> str:
    """
    Cria PDF genérico.
    sections_json = JSON: '[{"heading":"Título","body":"Texto..."}]'
    """
    sections = json.loads(sections_json)
    path = pdf_tools.create_pdf(title, sections, filename)
    return f"✅ PDF criado: {path}"


@mcp.tool()
def pdf_contract(
    title: str,
    party_a: str,
    party_b: str,
    clauses_json: str,
    date: str,
    filename: str = None,
) -> str:
    """
    Cria contrato PDF profissional.
    clauses_json = JSON: '["Cláusula 1...","Cláusula 2..."]'
    """
    clauses = json.loads(clauses_json)
    path = pdf_tools.create_contract(title, party_a, party_b, clauses, date, filename)
    return f"✅ Contrato criado: {path}"


@mcp.tool()
def pdf_resume(
    name: str,
    contact_json: str,
    summary: str,
    experience_json: str,
    education_json: str,
    skills_json: str,
    filename: str = None,
) -> str:
    """
    Cria currículo PDF profissional.
    contact_json = '{"email":"","phone":"","linkedin":"","city":""}'
    experience_json = '[{"company":"","role":"","period":"","description":""}]'
    education_json = '[{"institution":"","degree":"","period":""}]'
    skills_json = '["Python","Power BI","n8n"]'
    """
    path = pdf_tools.create_resume(
        name,
        json.loads(contact_json),
        summary,
        json.loads(experience_json),
        json.loads(education_json),
        json.loads(skills_json),
        filename,
    )
    return f"✅ Currículo criado: {path}"


# ── PPTX ───────────────────────────────────────────────────────────────────────

@mcp.tool()
def pptx_create(title: str, slides_json: str, filename: str = None) -> str:
    """
    Cria apresentação PowerPoint.
    slides_json = JSON com lista de slides:
    '[
      {"type":"title","title":"Minha Apresentação","subtitle":"Subtítulo"},
      {"type":"content","title":"Tópico","bullets":["Ponto 1","Ponto 2"]},
      {"type":"section","title":"Nova Seção"},
      {"type":"closing","title":"Obrigado!","subtitle":"contato@email.com"}
    ]'
    Tipos: title | content | section | closing
    """
    slides = json.loads(slides_json)
    path = pptx_tools.create_presentation(title, slides, filename)
    return f"✅ Apresentação criada: {path}"


@mcp.tool()
def pptx_add_slide(pptx_path: str, slide_json: str) -> str:
    """
    Adiciona slide a apresentação existente.
    slide_json = '{"type":"content","title":"Novo slide","bullets":["item"]}'
    """
    slide = json.loads(slide_json)
    return pptx_tools.add_slide(pptx_path, slide)


if __name__ == "__main__":
    mcp.run()
