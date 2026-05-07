"""Ferramentas Google Calendar: listar, criar, editar e deletar eventos."""
from datetime import datetime, timedelta, timezone

from googleapiclient.discovery import build

from .auth import get_credentials


def _service():
    return build("calendar", "v3", credentials=get_credentials())


def _fmt(dt_str: str) -> dict:
    """Converte string ISO para formato dateTime do Google Calendar."""
    return {"dateTime": dt_str, "timeZone": "America/Sao_Paulo"}


def list_events(days_ahead: int = 7, max_results: int = 20) -> list[dict]:
    """Lista próximos eventos do calendário."""
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days_ahead)
    result = _service().events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=end.isoformat(),
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = []
    for e in result.get("items", []):
        start = e["start"].get("dateTime", e["start"].get("date", ""))
        end_t = e["end"].get("dateTime", e["end"].get("date", ""))
        events.append({
            "id": e["id"],
            "titulo": e.get("summary", "(sem título)"),
            "inicio": start,
            "fim": end_t,
            "local": e.get("location", ""),
            "descricao": e.get("description", "")[:200],
            "participantes": [a["email"] for a in e.get("attendees", [])],
        })
    return events


def get_today_schedule() -> list[dict]:
    """Retorna a agenda de hoje."""
    return list_events(days_ahead=1)


def create_event(
    title: str,
    start: str,
    end: str,
    description: str = "",
    location: str = "",
    attendees: list[str] = None,
) -> str:
    """Cria um novo evento. start/end no formato ISO: '2026-05-07T10:00:00'"""
    body = {
        "summary": title,
        "description": description,
        "location": location,
        "start": _fmt(start),
        "end": _fmt(end),
    }
    if attendees:
        body["attendees"] = [{"email": e} for e in attendees]

    event = _service().events().insert(calendarId="primary", body=body).execute()
    return f"Evento criado! ID: {event['id']} — Link: {event.get('htmlLink', '')}"


def update_event(
    event_id: str,
    title: str = None,
    start: str = None,
    end: str = None,
    description: str = None,
    location: str = None,
) -> str:
    """Atualiza campos de um evento existente."""
    svc = _service()
    event = svc.events().get(calendarId="primary", eventId=event_id).execute()
    if title:
        event["summary"] = title
    if description:
        event["description"] = description
    if location:
        event["location"] = location
    if start:
        event["start"] = _fmt(start)
    if end:
        event["end"] = _fmt(end)
    svc.events().update(calendarId="primary", eventId=event_id, body=event).execute()
    return f"Evento {event_id} atualizado com sucesso."


def delete_event(event_id: str) -> str:
    """Remove um evento do calendário."""
    _service().events().delete(calendarId="primary", eventId=event_id).execute()
    return f"Evento {event_id} removido."
