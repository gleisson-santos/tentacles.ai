import asyncio
import time
import subprocess
import re
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("orchestrator")

mcp = FastMCP("orchestrator")

LOG_FILE = Path("logs/activity.log")
OCTOGENT_API = "http://127.0.0.1:8787"

@mcp.tool()
def get_last_activity(lines: int = 20) -> str:
    """Retorna as últimas linhas do log de atividade global."""
    if not LOG_FILE.exists():
        return "Arquivo de log não encontrado."
    
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            last_lines = all_lines[-lines:]
            return "".join(last_lines)
    except Exception as e:
        return f"Erro ao ler logs: {str(e)}"

import subprocess
import re

@mcp.tool()
async def delegate_to_agent(agent_id: str, instruction: str) -> str:
    """
    Delega uma tarefa para outro agente de forma direta (Visual Tentacle Connection).
    """
    logger.info(f"Delegando para {agent_id}: {instruction}")
    
    # Extrair task_id se houver
    task_match = re.search(r"task_id\s+([a-zA-Z0-9-]+)", instruction)
    task_id = task_match.group(1) if task_match else f"task-{int(time.time())}"
    
    # Limpar a instrução
    clean_prompt = re.sub(r"--task_id\s+[a-zA-Z0-9-]+", "", instruction).strip()

    # Obtemos o ID do terminal atual para ser o PAI do próximo
    parent_id = os.environ.get("OCTOGENT_SESSION_ID")

    try:
        # Usamos o script de delegação de forma robusta
        # Passamos o parent_id explicitamente (sem a flag --no-parent para criar o elo visual)
        cmd = [
            "python", "scripts/delegate_task.py",
            "--agent", agent_id,
            "--prompt", clean_prompt,
            "--task_id", task_id
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return (
                f"✅ Missão delegada para '{agent_id}' (Task: {task_id}).\n"
                f"Conexão visual estabelecida. Aguardando processamento do agente..."
            )
        else:
            return f"❌ Erro na delegação: {stderr.decode()}"
            
    except Exception as e:
        return f"❌ Erro crítico: {str(e)}"

if __name__ == "__main__":
    mcp.run()
