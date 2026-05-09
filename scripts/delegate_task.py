import sys
import httpx
import argparse
import os

OCTOGENT_API = "http://127.0.0.1:8787"

def delegate(agent_id, prompt, task_id):
    # Adiciona a instrução de status ao prompt do filho para o Telegram receber a confirmação
    final_prompt = (
        f"{prompt}\n\n"
        f"IMPORTANTE: Ao concluir com sucesso, grave 'OK|Sua mensagem de confirmação' "
        f"no arquivo: outputs/.status/{task_id}.done"
    )
    
    payload = {
        "name": f"Tarefa: {agent_id.replace('-', ' ').title()}",
        "tentacleId": agent_id,
        "initialPrompt": final_prompt,
        "agentProvider": "claude-code",
        "workspaceMode": "shared"
    }
    
    try:
        with httpx.Client(timeout=10) as client:
            resp = client.post(f"{OCTOGENT_API}/api/terminals", json=payload)
            if resp.status_code == 200:
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
    args = parser.parse_args()
    
    delegate(args.agent, args.prompt, args.task_id)
