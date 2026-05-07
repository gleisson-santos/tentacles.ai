"""
Autenticação OAuth2 para Google APIs (Gmail, Calendar, Sheets).
Execute este arquivo diretamente para fazer o setup inicial:
  python mcp_servers/google_mcp/auth.py
"""
import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]

CREDS_DIR = Path(__file__).parent / "credentials"
TOKEN_FILE = CREDS_DIR / "token.json"
SECRET_FILE = CREDS_DIR / "client_secret.json"


def get_credentials() -> Credentials:
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not SECRET_FILE.exists():
                raise FileNotFoundError(
                    f"\n{'='*55}\n"
                    f"  SETUP NECESSÁRIO\n"
                    f"{'='*55}\n"
                    f"  1. Acesse: https://console.cloud.google.com\n"
                    f"  2. Crie um projeto e ative: Gmail API, Calendar API, Sheets API\n"
                    f"  3. Crie credenciais OAuth2 (tipo: Desktop App)\n"
                    f"  4. Baixe o JSON e salve em:\n"
                    f"     {SECRET_FILE}\n"
                    f"  5. Execute novamente: python mcp_servers/google_mcp/auth.py\n"
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(SECRET_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        CREDS_DIR.mkdir(parents=True, exist_ok=True)
        TOKEN_FILE.write_text(creds.to_json())
        print(f"  Token salvo em: {TOKEN_FILE}")
    return creds


if __name__ == "__main__":
    print("Iniciando autenticação Google...")
    creds = get_credentials()
    print("Autenticação concluída com sucesso!")
    print(f"Token válido até: {creds.expiry}")
