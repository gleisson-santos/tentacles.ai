import os
import sys
import json
import httpx
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

def query_llm(prompt, system_prompt=None):
    config = load_config()
    active_provider = config.get("active_provider", "groq")
    provider_data = config.get("providers", {}).get(active_provider)
    
    if not provider_data:
        return f"Error: Provider '{active_provider}' not configured."
    
    model = provider_data.get("model")
    api_key = os.getenv(provider_data.get("api_key_env"))
    
    if not api_key:
        return f"❌ Error: API Key ({provider_data.get('api_key_env')}) not found in .env."

    print("\n(esc to interrupt) 🧠 Pensando...", flush=True)
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        if active_provider == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
        elif active_provider == "openai":
            url = "https://api.openai.com/v1/chat/completions"
        elif active_provider == "openrouter":
            url = "https://openrouter.ai/api/v1/chat/completions"
        else:
            return f"Error: Provider '{active_provider}' not supported."

        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                url,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages}
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
            return content
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
        "Você é o Tentacles Agent, um assistente de produtividade. "
        "Você tem acesso ao contexto do projeto Tentacles. "
        "Siga as instruções do usuário de forma concisa e eficiente. "
        "Sempre responda em Português do Brasil."
    )

    # Check if initial prompt was passed as argument (non-interactive mode)
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        result = query_llm(prompt, system_prompt)
        print(f"\n{result}\n")
        return

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
