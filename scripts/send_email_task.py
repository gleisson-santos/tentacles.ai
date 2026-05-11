import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp_servers.google_mcp import gmail_tools

def main():
    to = "glfx20@gmail.com"
    subject = "Visita de Amanhã"
    body = """Olá Caio,

Gostaria de confirmar nossa visita agendada para amanhã.

Atenciosamente,
Assistente Tentacles"""
    
    print(f"Enviando email para {to}...")
    try:
        result = gmail_tools.send_email(to, subject, body)
        print(result)
        # IPC: Agente filho deve gravar OK|mensagem em outputs/.status/{task_id}.done
        # No context this task_id is 'google-assistant-swarm-0' or derived.
        # The prompt says my terminal ID is `google-assistant-swarm-0`.
        # Usually task_id comes from delegate_task.py but here I am acting as the agent directly.
        # I'll check if there's a task_id file I should update.
        # The prompt mentions: node bin/octogent channel send ...
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
