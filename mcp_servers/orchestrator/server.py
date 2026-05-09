import os
import logging
import httpx
import json
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

@mcp.tool()
async def delegate_to_agent(agent_id: str, instruction: str) -> str:
    """
    Delega uma tarefa para outro agente, criando um novo terminal conectado ao Octoboss.
    Isso mantém o agente no círculo principal do Dashboard sem 'puxá-lo' para o Orchestrator.
    """
    logger.info(f"Delegando para {agent_id}: {instruction}")
    
    payload = {
        "name": f"Tarefa: {agent_id.replace('-', ' ').title()}",
        "tentacleId": agent_id,
        "initialPrompt": instruction,
        "agentProvider": "claude-code",
        "workspaceMode": "shared"
        # parentTerminalId removido para manter no círculo central
    }
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(f"{OCTOGENT_API}/api/terminals", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return (
                    f"✅ Ordem enviada! O tentáculo '{agent_id}' foi acionado no círculo central. "
                    f"ID da Tarefa: {data.get('terminalId')}. "
                    f"Estarei aqui piscando e monitorando o progresso..."
                )
            else:
                return f"❌ Falha ao acionar agente: {resp.text}"
    except Exception as e:
        return f"❌ Erro de comunicação: {str(e)}"

if __name__ == "__main__":
    mcp.run()
