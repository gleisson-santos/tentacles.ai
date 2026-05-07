import os
import json
import httpx
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Universal Brain")

ROOT_DIR = Path(__file__).parent.parent.parent
CONFIG_FILE = ROOT_DIR / "config" / "llm_config.json"
ENV_FILE = ROOT_DIR / ".env"
OCTOGENT_API = "http://127.0.0.1:8787"

def _load_config():
    if not CONFIG_FILE.exists():
        return {
            "active_provider": "openrouter",
            "providers": {
                "openrouter": {"model": "x-ai/grok-beta", "api_key_env": "OPENROUTER_API_KEY"},
                "groq": {"model": "llama-3.3-70b-versatile", "api_key_env": "GROQ_API_KEY"},
                "openai": {"model": "gpt-4o", "api_key_env": "OPENAI_API_KEY"}
            }
        }
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

@mcp.tool()
def setup_x_monitor(bearer_token: str) -> str:
    """
    Configura o X Monitor enviando as credenciais diretamente para a API do Octogent.
    """
    payload = {
        "x": {
            "bearerToken": bearer_token,
            "terms": [
                "Artificial Intelligence", "Automation", "Claude AI", 
                "Grok AI", "n8n", "DeepSeek", "Llama 3"
            ]
        }
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.patch(f"{OCTOGENT_API}/api/monitor/config", json=payload)
            if resp.status_code == 200:
                # Também salva no .env para persistência
                update_env_key("X_BEARER_TOKEN", bearer_token)
                return "✅ X Monitor configurado e ativado com sucesso no Dashboard!"
            else:
                return f"❌ Erro API Octogent ({resp.status_code}): {resp.text}"
    except Exception as e:
        return f"❌ Falha ao conectar na API do Dashboard: {e}"

@mcp.tool()
def get_current_llm_config() -> str:
    """Retorna a configuração atual e verifica se a API Key está presente."""
    config = _load_config()
    active = config["active_provider"]
    provider_data = config["providers"].get(active, {})
    model = provider_data.get("model", "desconhecido")
    key_env = provider_data.get("api_key_env")
    
    has_key = os.getenv(key_env) is not None
    key_status = "✅ Chave configurada" if has_key else "❌ Chave AUSENTE no .env"
    
    return f"Provedor: {active}\nModelo: {model}\nStatus: {key_status}"

@mcp.tool()
def update_env_key(key_name: str, key_value: str) -> str:
    """Atualiza ou adiciona uma chave secreta no arquivo .env"""
    lines = []
    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()
    
    new_lines = []
    found = False
    for line in lines:
        if line.startswith(f"{key_name}="):
            new_lines.append(f"{key_name}={key_value}\n")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f"{key_name}={key_value}\n")
    
    with open(ENV_FILE, "w") as f:
        f.writelines(new_lines)
    
    os.environ[key_name] = key_value
    return f"✅ Chave {key_name} salva com sucesso no .env"

@mcp.tool()
def set_active_llm(provider: str, model: str = None) -> str:
    """Altera o provedor e/ou modelo ativo dinamicamente."""
    config = _load_config()
    provider = provider.lower()
    
    if provider not in config["providers"]:
        config["providers"][provider] = {"model": model, "api_key_env": f"{provider.upper()}_API_KEY"}
    
    config["active_provider"] = provider
    if model:
        config["providers"][provider]["model"] = model
        
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    
    key_env = config["providers"][provider]["api_key_env"]
    if not os.getenv(key_env):
        return f"⚠️ Provedor alterado para {provider}, mas a chave {key_env} não foi encontrada."
    
    return f"✅ Cérebro atualizado: {provider} ({model or config['providers'][provider]['model']})"

@mcp.tool()
def query_llm(prompt: str, system_prompt: str = None) -> str:
    config = _load_config()
    active_provider = config["active_provider"]
    provider_data = config["providers"].get(active_provider)
    if not provider_data: return f"Erro: Provedor '{active_provider}' não configurado."
    
    model = provider_data["model"]
    api_key = os.getenv(provider_data["api_key_env"])
    if not api_key: return f"❌ Erro: API Key ({provider_data['api_key_env']}) faltando."

    if active_provider == "openrouter":
        return _query_openrouter(prompt, model, system_prompt, api_key)
    elif active_provider == "groq":
        return _query_groq(prompt, model, system_prompt, api_key)
    elif active_provider == "openai":
        return _query_openai(prompt, model, system_prompt, api_key)
    return f"Erro: Provedor '{active_provider}' não suportado."

def _query_openrouter(prompt: str, model: str, system: str, api_key: str) -> str:
    messages = []
    if system: messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages}
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
    except Exception as e: return f"Erro OpenRouter: {e}"

def _query_groq(prompt: str, model: str, system: str, api_key: str) -> str:
    messages = []
    if system: messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages}
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
    except Exception as e: return f"Erro Groq: {e}"

def _query_openai(prompt: str, model: str, system: str, api_key: str) -> str:
    messages = []
    if system: messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages}
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
    except Exception as e: return f"Erro OpenAI: {e}"

if __name__ == "__main__":
    mcp.run()
