import sys
import httpx
import argparse
import os

OCTOGENT_API = "http://127.0.0.1:8787"

def delegate(agent_id, prompt, task_id, no_parent=False):
    # Comando de animação para o Dashboard
    visual_echo = f"echo 'Iniciando tarefa {task_id} no agente {agent_id}...'\n"
    
    # Adiciona a instrução de status ao prompt do filho para o Telegram receber a confirmação
    final_prompt = (
        f"{visual_echo}"
        f"{prompt}\n\n"
        f"IMPORTANTE: Ao concluir com sucesso, grave 'OK|Sua mensagem de confirmação' "
        f"no arquivo: outputs/.status/{task_id}.done"
    )
    # Obter a preferência de agente da API (Gemini vs Claude)
    preferred_provider = "gemini-cli"
    try:
        with httpx.Client(timeout=5) as client:
            ui_resp = client.get(f"{OCTOGENT_API}/api/ui-state")
            if ui_resp.status_code == 200:
                preferred_provider = ui_resp.json().get("preferredAgentProvider", "gemini-cli")
    except Exception:
        pass

    parent_id = None if no_parent else os.environ.get("OCTOGENT_SESSION_ID")

    payload = {
        "name": f"Tarefa: {agent_id.replace('-', ' ').title()}",
        "tentacleId": agent_id,
        "initialPrompt": final_prompt,
        "agentProvider": preferred_provider,
        "workspaceMode": "shared",
        "parentTerminalId": parent_id
    }
    
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(f"{OCTOGENT_API}/api/terminals", json=payload)
            if resp.status_code in [200, 201]:
                data = resp.json()
                print(f"SUCCESS: Terminal {agent_id} criado com ID {data.get('terminalId')}")
            else:
                print(f"ERROR: Falha na API ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"FATAL: Erro de conexão: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--task_id", required=True)
    parser.add_argument("--no-parent", action="store_true", help="Evita aninhamento de terminais")
    args = parser.parse_args()
    
    delegate(args.agent, args.prompt, args.task_id, args.no_parent)
