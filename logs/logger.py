"""
Logger compartilhado para todos os agentes Clilink.
Grava em logs/activity.log e envia eventos para o Octogent dashboard.
"""
import subprocess
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "activity.log"
OCTOGENT_CHANNEL = "clilink-events"


def log(agent: str, action: str, detail: str = "") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{agent.upper()}] {action}"
    if detail:
        line += f" | {detail}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_octogent(agent: str, action: str, detail: str = "") -> None:
    """Envia evento para o canal Octogent (silencioso se não estiver rodando)."""
    msg = f"[{agent.upper()}] {action}"
    if detail:
        msg += f" | {detail}"
    try:
        safe_msg = msg.replace('"', '\\"')
        subprocess.run(
            f'octogent channel send {OCTOGENT_CHANNEL} "{safe_msg}"',
            capture_output=True, timeout=5, shell=True,
        )
    except Exception:
        pass
