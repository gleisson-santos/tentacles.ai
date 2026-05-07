import feedparser
import json
import os
import time
import requests
from pathlib import Path
from datetime import datetime

# ── Configurações ──────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent
OUTPUT_FILE = ROOT_DIR / "outputs" / "trends_data.json"
CONFIG_FILE = ROOT_DIR / "config" / "monitor_config.json"
OCTOGENT_API = "http://127.0.0.1:8787"

# TENTACULO_ID deve bater com o nome da pasta em .octogent/tentacles/
TENTACULO_ID = "trends-intelligence"

def update_tentacle_status(state, tool_name=None):
    """
    Atualiza o estado visual do tentáculo no Dashboard.
    States: 'idle', 'processing', 'error'
    """
    try:
        # Envia evento de troca de estado para a API do Octogent
        # O Octogent Dashboard monitora esses eventos para animar os ícones
        payload = {
            "type": "terminal-state-changed",
            "terminalId": "trends-monitor-service", # ID virtual do serviço
            "tentacleId": TENTACULO_ID,
            "agentRuntimeState": state,
            "toolName": tool_name
        }
        # Nota: A animação real depende do Dashboard receber esse via WebSocket ou polling.
        # Como o script é externo, enviamos via log de canal que o Octogent lê.
        log_msg = f"[{state.upper()}] " + (f"Ferramenta: {tool_name}" if tool_name else "")
        requests.post(f"{OCTOGENT_API}/api/channels/send", json={
            "channelId": "clilink-events", 
            "message": f"[TENTACLE:{TENTACULO_ID}] {log_msg}"
        }, timeout=2)
    except:
        pass

def load_search_terms():
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config.get("searchTerms", ["Artificial Intelligence", "Automation"])
    except:
        pass
    return ["Artificial Intelligence", "Automation"]

def fetch_google_news(terms):
    query = "+OR+".join([t.replace(" ", "+") for t in terms])
    url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    try:
        feed = feedparser.parse(url)
        news_items = []
        for entry in feed.entries[:10]:
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "source": "Google News"
            })
        return news_items
    except Exception as e:
        print(f"❌ Erro: {e}")
        return []

def update_monitor():
    update_tentacle_status("processing", "GoogleNewsSearch")
    terms = load_search_terms()
    print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] Buscando por: {', '.join(terms)}")
    
    data = {
        "last_update": datetime.now().isoformat(),
        "search_terms": terms,
        "google_news": fetch_google_news(terms),
        "youtube_trends": [{"title": f"Destaque: {terms[0]}", "source": "YouTube"}]
    }
    
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    update_tentacle_status("idle")
    print("✅ Trends Data atualizado.")

if __name__ == "__main__":
    print("=" * 55)
    print("   TENTACLES Trends Intelligence (Tentáculo Ativo)")
    print("=" * 55)
    while True:
        try:
            update_monitor()
        except Exception as e:
            print(f"❌ Erro: {e}")
            update_tentacle_status("error", str(e))
        
        interval = 120
        try:
            with open(CONFIG_FILE, "r") as f: interval = json.load(f).get("refreshIntervalMinutes", 120)
        except: pass
        
        print(f"💤 Próximo ciclo em {interval} minutos...\n")
        time.sleep(interval * 60)
