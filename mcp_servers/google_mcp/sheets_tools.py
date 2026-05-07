"""Ferramentas Google Sheets: ler, escrever, criar planilhas e adicionar linhas."""
from googleapiclient.discovery import build

from .auth import get_credentials


def _service():
    return build("sheets", "v4", credentials=get_credentials())


def _drive():
    from googleapiclient.discovery import build as _build
    from .auth import get_credentials as _gc
    return _build("drive", "v3", credentials=_gc())


def list_spreadsheets(max_results: int = 20) -> list[dict]:
    """Lista planilhas disponíveis no Google Drive."""
    result = _drive().files().list(
        q="mimeType='application/vnd.google-apps.spreadsheet'",
        pageSize=max_results,
        fields="files(id, name, modifiedTime)",
    ).execute()
    return [
        {"id": f["id"], "nome": f["name"], "modificado": f.get("modifiedTime", "")}
        for f in result.get("files", [])
    ]


def read_sheet(spreadsheet_id: str, range_name: str = "Sheet1") -> list[list]:
    """Lê dados de um range da planilha. Ex: range_name='Sheet1!A1:E20'"""
    result = _service().spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()
    return result.get("values", [])


def write_sheet(spreadsheet_id: str, range_name: str, values: list[list]) -> str:
    """Escreve dados em um range. values = lista de linhas."""
    body = {"values": values}
    result = _service().spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body=body,
    ).execute()
    return f"{result.get('updatedCells', 0)} células atualizadas."


def append_row(spreadsheet_id: str, sheet_name: str, values: list) -> str:
    """Adiciona uma nova linha ao final da planilha."""
    body = {"values": [values]}
    result = _service().spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()
    return f"Linha adicionada: {result.get('updates', {}).get('updatedRange', '')}"


def create_spreadsheet(title: str, headers: list[str] = None) -> str:
    """Cria uma nova planilha e retorna o ID e link."""
    body = {"properties": {"title": title}}
    sheet = _service().spreadsheets().create(body=body, fields="spreadsheetId").execute()
    sid = sheet["spreadsheetId"]
    if headers:
        write_sheet(sid, "Sheet1!A1", [headers])
    return f"Planilha criada! ID: {sid} — https://docs.google.com/spreadsheets/d/{sid}"
