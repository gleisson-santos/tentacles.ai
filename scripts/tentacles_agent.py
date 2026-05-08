import os
import sys
import json
import httpx
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

ROOT_DIR = Path(__file__).parent.parent
CONFIG_FILE = ROOT_DIR / "config" / "llm_config.json"

def load_config():
    if not CONFIG_FILE.exists():
        return {
            "active_provider": "groq",
            "providers": {
                "groq": {"model": "llama-3.3-70b-versatile", "api_key_env": "GROQ_API_KEY"}
            }
        }
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def execute_command(command):
    """Executa um comando no shell e retorna o output."""
    try:
        print(f"🛠️ Executando: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        output = result.stdout + result.stderr
        return output if output else "Comando executado (sem saída)."
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"

def query_llm(prompt, system_prompt=None, messages=None):
    config = load_config()
    active_provider = config.get("active_provider", "groq")
    provider_data = config.get("providers", {}).get(active_provider)
    
    if not provider_data:
        return f"Error: Provider '{active_provider}' not configured."
    
    model = provider_data.get("model")
    api_key = os.getenv(provider_data.get("api_key_env"))
    
    if not api_key:
        return f"❌ Error: API Key ({provider_data.get('api_key_env')}) not found in .env."

    if messages is None:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

    # Definição da ferramenta de shell
    tools = [
        {
            "type": "function",
            "function": {
                "name": "execute_shell_command",
                "description": "Executa um comando no terminal (bash/powershell) para ler, criar ou modificar arquivos e gerenciar o projeto.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "O comando exato a ser executado."}
                    },
                    "required": ["command"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "run_python_code",
                "description": "Executa código Python diretamente. Útil para usar as ferramentas de PDF, PPTX e Google do projeto.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "O código Python a ser executado."}
                    },
                    "required": ["code"]
                }
            }
        }
    ]

    # Configuração de URL e Headers
    if active_provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
    elif active_provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
    elif active_provider == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
    else:
        return f"Error: Provider '{active_provider}' not supported."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://tentacles.ai",
        "X-Title": "Tentacles Universal Agent"
    }

    try:
        print("\n(esc to interrupt) 🧠 Pensando...", flush=True)

        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                url,
                headers=headers,
                json={
                    "model": model, 
                    "messages": messages,
                    "tools": tools,
                    "tool_choice": "auto"
                }
            )
            resp.raise_for_status()
            response_json = resp.json()
            
            # Debug: Se quiser ver a resposta completa, descomente a linha abaixo
            # print(f"\nDEBUG: Resposta: {json.dumps(response_json, indent=2)}")

            if "choices" not in response_json or not response_json["choices"]:
                return f"❌ Erro: Resposta inválida do provedor: {response_json}"

            message = response_json["choices"][0]["message"]

            if message.get("tool_calls"):
                for tool_call in message["tool_calls"]:
                    fn_name = tool_call["function"]["name"]
                    args_str = tool_call["function"]["arguments"]
                    try:
                        args = json.loads(args_str)
                    except:
                        args = {}
                    
                    print(f"\n🔧 [AGENTE AGINDO]: {fn_name}(...)")
                    
                    if fn_name == "execute_shell_command":
                        cmd_output = execute_command(args.get("command", ""))
                    elif fn_name == "run_python_code":
                        # Salva em um arquivo temporário e executa
                        temp_file = ROOT_DIR / ".temp_agent_script.py"
                        code = args.get("code", "")
                        # Adiciona o ROOT_DIR ao sys.path no script gerado
                        full_code = f"import sys\nfrom pathlib import Path\nsys.path.insert(0, r'{ROOT_DIR}')\n" + code
                        with open(temp_file, "w", encoding="utf-8") as f:
                            f.write(full_code)
                        cmd_output = execute_command(f"python {temp_file}")
                        if temp_file.exists():
                            os.remove(temp_file)
                    else:
                        cmd_output = f"Erro: Ferramenta {fn_name} não implementada."

                    messages.append(message)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": fn_name,
                        "content": cmd_output
                    })
                    
                    return query_llm(None, messages=messages)
            
            return message.get("content", "Sem resposta do modelo.")
    except Exception as e:
        return f"❌ Erro ao consultar LLM ({active_provider}): {e}"

def main():
    print("===============================================")
    print("   Tentacles Agent — Universal Brain CLI")
    print("===============================================")
    print(f"Provider: {load_config().get('active_provider')}")
    print("Type 'exit' or 'quit' to leave.")
    print("-----------------------------------------------")

    system_prompt = (
        "Você é o ORQUESTRADOR do projeto Tentacles, um assistente de produtividade de ELITE. "
        "DIRETRIZ CRÍTICA: Você NUNCA dá desculpas ou sugere que o usuário instale algo. VOCÊ AGE. "
        "Você conhece e pode usar os outros agentes deste projeto:\n"
        "- Files Assistant (mcp_servers/files_mcp): Especialista em PDFs e PPTX.\n"
        "- Google Assistant (mcp_servers/google_mcp): Gmail, Calendar, Sheets.\n"
        "- LinkedIn Poster (auto_poster.py): Postagens automáticas.\n\n"
        "Se o usuário pedir algo como 'Gerar um PDF', use o 'execute_shell_command' para:\n"
        "1. Tentar acionar o servidor MCP correspondente em 'mcp_servers/'.\n"
        "2. OU escrever e executar seu próprio script Python IMEDIATAMENTE.\n"
        "NÃO mostre o código para o usuário antes de executá-lo. Execute e entregue o resultado."
        "\nSempre responda em Português do Brasil."
    )

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        result = query_llm(prompt, system_prompt)
        print(f"\n{result}\n")

    while True:
        try:
            print("\n> ", end="", flush=True)
            user_input = sys.stdin.readline()
            if not user_input:
                break
            
            user_input = user_input.strip()
            if user_input.lower() in ["exit", "quit"]:
                break
            if not user_input:
                continue
                
            result = query_llm(user_input, system_prompt)
            print(f"\n{result}")
            
        except KeyboardInterrupt:
            print("\nInterrompido pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro inesperado: {e}")

if __name__ == "__main__":
    main()
