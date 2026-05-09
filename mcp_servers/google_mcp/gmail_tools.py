"""Ferramentas Gmail: listar, ler, enviar, deletar e resumir emails."""
import base64
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build

from .auth import get_credentials


def _service():
    return build("gmail", "v1", credentials=get_credentials())


def _decode_body(payload: dict) -> str:
    """Extrai texto do corpo do email (suporta plain/html e multipart)."""
    body = ""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data", "")
                body = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="replace")
                break
    else:
        data = payload.get("body", {}).get("data", "")
        if data:
            body = base64.urlsafe_b64decode(data + "==").decode("utf-8", errors="replace")
    return body.strip()


def list_emails(max_results: int = 10, label: str = "INBOX") -> list[dict]:
    """Lista emails recentes da caixa de entrada."""
    svc = _service()
    result = svc.users().messages().list(
        userId="me", maxResults=max_results, labelIds=[label]
    ).execute()

    messages = result.get("messages", [])
    emails = []
    for msg in messages:
        detail = svc.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()
        headers = {h["name"].lower(): h["value"] for h in detail["payload"]["headers"]}
        emails.append({
            "id": msg["id"],
            "from": headers.get("from", ""),
            "subject": headers.get("subject", "(sem assunto)"),
            "date": headers.get("date", ""),
            "snippet": detail.get("snippet", ""),
        })
    return emails


def get_email(email_id: str) -> dict:
    """Lê o conteúdo completo de um email pelo ID."""
    svc = _service()
    msg = svc.users().messages().get(userId="me", id=email_id, format="full").execute()
    headers = {h["name"].lower(): h["value"] for h in msg["payload"]["headers"]}
    body = _decode_body(msg["payload"])
    return {
        "id": email_id,
        "from": headers.get("from", ""),
        "to": headers.get("to", ""),
        "subject": headers.get("subject", "(sem assunto)"),
        "date": headers.get("date", ""),
        "body": body[:3000],
    }


def send_email(to: str, subject: str, body: str) -> str:
    """Envia um email."""
    svc = _service()
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    sent = svc.users().messages().send(userId="me", body={"raw": raw}).execute()
    return f"Email enviado! ID: {sent['id']}"


def delete_email(email_id: str) -> str:
    """Move email para a lixeira."""
    _service().users().messages().trash(userId="me", id=email_id).execute()
    return f"Email {email_id} movido para lixeira."


def summarize_inbox(max_emails: int = 20) -> list[dict]:
    """Retorna resumo estruturado da caixa de entrada para análise por IA."""
    emails = list_emails(max_results=max_emails)
    return [
        {
            "id": e["id"],
            "de": e["from"],
            "assunto": e["subject"],
            "data": e["date"],
            "preview": re.sub(r"\s+", " ", e["snippet"])[:200],
        }
        for e in emails
    ]
