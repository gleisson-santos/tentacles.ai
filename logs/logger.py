"""
Logger compartilhado para todos os agentes Clilink.
Grava em logs/activity.log e envia eventos para o Octogent dashboard.
"""
import subprocess
import threading
import requests
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "activity.log"
OCTOGENT_CHANNEL = "tentacles-events"

def log(agent: str, action: str, detail: str = "") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{agent.upper()}] {action}"
    if detail:
        line += f" | {detail}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def _send_octogent_event(msg: str):
    try:
        requests.post(
            f"http://127.0.0.1:8787/api/channels/{OCTOGENT_CHANNEL}/messages",
            json={"fromTerminalId": "logger", "content": msg},
            timeout=2
        )
    except Exception:
        pass

def log_octogent(agent: str, action: str, detail: str = "") -> None:
    """Envia evento para o canal Octogent (silencioso e sem travar a thread)."""
    msg = f"[{agent.upper()}] {action}"
    if detail:
        msg += f" | {detail}"
    
    # Executa em modo fire-and-forget usando Thread para não bloquear os scripts nem o bot
    threading.Thread(target=_send_octogent_event, args=(msg,), daemon=True).start()
