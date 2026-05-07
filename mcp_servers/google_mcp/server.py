"""
Google MCP Server — Gmail + Calendar + Sheets
Rode com: python mcp_servers/google_mcp/server.py
"""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__file__))))

from mcp.server.fastmcp import FastMCP
from mcp_servers.google_mcp import gmail_tools, calendar_tools, sheets_tools

mcp = FastMCP("google-assistant")

# ── GMAIL ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def gmail_list(max_results: int = 10) -> str:
    """Lista os últimos emails da caixa de entrada."""
    emails = gmail_tools.list_emails(max_results)
    lines = [f"[{e['date'][:16]}] De: {e['from'][:40]}\n  Assunto: {e['subject']}\n  {e['snippet'][:120]}" for e in emails]
    return f"📧 {len(emails)} emails:\n\n" + "\n\n".join(lines)


@mcp.tool()
def gmail_read(email_id: str) -> str:
    """Lê o conteúdo completo de um email pelo ID."""
    e = gmail_tools.get_email(email_id)
    return f"De: {e['from']}\nPara: {e['to']}\nAssunto: {e['subject']}\nData: {e['date']}\n\n{e['body']}"


@mcp.tool()
def gmail_send(to: str, subject: str, body: str) -> str:
    """Envia um email. to=destinatário, subject=assunto, body=corpo."""
    return gmail_tools.send_email(to, subject, body)


@mcp.tool()
def gmail_delete(email_id: str) -> str:
    """Move um email para a lixeira pelo ID."""
    return gmail_tools.delete_email(email_id)


@mcp.tool()
def gmail_summarize(max_emails: int = 20) -> str:
    """Retorna resumo da caixa de entrada para análise."""
    emails = gmail_tools.summarize_inbox(max_emails)
    lines = [f"{i+1}. [{e['data'][:10]}] {e['de'][:35]} — {e['assunto']}" for i, e in enumerate(emails)]
    return f"📬 Resumo da caixa de entrada ({len(emails)} emails):\n\n" + "\n".join(lines)


# ── CALENDAR ───────────────────────────────────────────────────────────────────

@mcp.tool()
def calendar_list(days_ahead: int = 7) -> str:
    """Lista próximos eventos do calendário."""
    events = calendar_tools.list_events(days_ahead)
    if not events:
        return f"Nenhum evento nos próximos {days_ahead} dias."
    lines = [f"📅 {e['inicio'][:16]} — {e['titulo']}\n   {e['local'] or 'Sem local'}" for e in events]
    return "\n\n".join(lines)


@mcp.tool()
def calendar_today() -> str:
    """Retorna a agenda completa de hoje."""
    events = calendar_tools.get_today_schedule()
    if not events:
        return "📅 Nenhum evento hoje."
    lines = [f"• {e['inicio'][11:16]} — {e['titulo']}" for e in events]
    return "📅 Agenda de hoje:\n" + "\n".join(lines)


@mcp.tool()
def calendar_create(title: str, start: str, end: str, description: str = "", location: str = "") -> str:
    """Cria evento. start/end formato: '2026-05-07T10:00:00'"""
    return calendar_tools.create_event(title, start, end, description, location)


@mcp.tool()
def calendar_update(event_id: str, title: str = None, start: str = None, end: str = None, description: str = None) -> str:
    """Atualiza um evento existente pelo ID."""
    return calendar_tools.update_event(event_id, title, start, end, description)


@mcp.tool()
def calendar_delete(event_id: str) -> str:
    """Remove um evento do calendário pelo ID."""
    return calendar_tools.delete_event(event_id)


# ── SHEETS ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def sheets_list() -> str:
    """Lista planilhas disponíveis no Google Drive."""
    sheets = sheets_tools.list_spreadsheets()
    lines = [f"• {s['nome']} — ID: {s['id']}" for s in sheets]
    return "📊 Planilhas:\n" + "\n".join(lines)


@mcp.tool()
def sheets_read(spreadsheet_id: str, range_name: str = "Sheet1") -> str:
    """Lê dados de uma planilha. range_name ex: 'Sheet1!A1:E20'"""
    data = sheets_tools.read_sheet(spreadsheet_id, range_name)
    if not data:
        return "Planilha vazia ou range não encontrado."
    lines = [" | ".join(str(c) for c in row) for row in data]
    return f"📊 {len(data)} linhas:\n" + "\n".join(lines[:50])


@mcp.tool()
def sheets_write(spreadsheet_id: str, range_name: str, values_json: str) -> str:
    """Escreve dados. values_json = JSON de lista de listas ex: '[["A","B"],["1","2"]]'"""
    import json
    values = json.loads(values_json)
    return sheets_tools.write_sheet(spreadsheet_id, range_name, values)


@mcp.tool()
def sheets_append(spreadsheet_id: str, sheet_name: str, row_json: str) -> str:
    """Adiciona linha. row_json = JSON de lista ex: '["João","30","SP"]'"""
    import json
    row = json.loads(row_json)
    return sheets_tools.append_row(spreadsheet_id, sheet_name, row)


@mcp.tool()
def sheets_create(title: str, headers_json: str = "[]") -> str:
    """Cria nova planilha. headers_json = JSON de lista ex: '["Nome","Email","Telefone"]'"""
    import json
    headers = json.loads(headers_json)
    return sheets_tools.create_spreadsheet(title, headers or None)


if __name__ == "__main__":
    mcp.run()
