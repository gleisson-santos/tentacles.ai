import feedparser
import json
import os
import sys
import time
import requests
import urllib.parse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv()

# ── Configurações ──────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent
OUTPUT_FILE = ROOT_DIR / "outputs" / "trends_data.json"
CONFIG_FILE = ROOT_DIR / "config" / "monitor_config.json"
TENTACULO_ID = "trends-intelligence"

# Inicializa Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_octogent_api():
    return os.getenv("OCTOGENT_API_URL", "http://127.0.0.1:8787")

def update_tentacle_status(state, detail=""):
    """
    Atualiza o estado visual e log do tentáculo no Dashboard.
    """
    api_url = get_octogent_api()
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{state.upper()}] {detail}")
    
    try:
        msg = f"[TENTACLE:{TENTACULO_ID}] {state.upper()}: {detail}"
        # Rota correta para mensagens de evento
        requests.post(f"{api_url}/api/channels/tentacles-events/messages", json={
            "fromTerminalId": "trends-monitor-script",
            "content": msg
        }, timeout=0.5)
        
        # Opcional: Atualizar status do tentáculo via API se disponível
        # requests.post(f"{api_url}/api/deck/tentacles/{TENTACULO_ID}/status", json={"status": state}, timeout=0.5)
    except:
        pass

def load_config():
    defaults = {
        "searchTerms": ["Artificial Intelligence", "Automation"],
        "refreshIntervalMinutes": 1
    }
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in defaults.items():
                    if k not in data:
                        data[k] = v
                return data
    except Exception as e:
        print(f"⚠️ Erro ao carregar config: {e}")
    return defaults

def summarize_news(title, source):
    """
    Usa Groq para criar um resumo rápido e atraente da notícia.
    """
    try:
        prompt = f"Crie um resumo atraente e informativo (em 2-3 parágrafos) sobre esta notícia: '{title}'. Fonte: {source}. Foco em impacto tecnológico e tendências de mercado."
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Resumo temporariamente indisponível. (Erro: {e})"

def fetch_google_news(terms):
    clean_terms = [t.strip().replace("\n", "").replace("\r", "") for t in terms[:5]]
    query = " OR ".join([f'"{t}"' for t in clean_terms])
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    
    try:
        feed = feedparser.parse(url)
        news_items = []
        # Pegamos os 5 mais recentes para resumir
        for entry in feed.entries[:5]:
            update_tentacle_status("processing", f"Resumindo: {entry.title[:30]}...")
            summary = summarize_news(entry.title, "Google News")
            
            # Hora da análise (agora)
            analysis_time = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published, # Data original
                "analysis_time": analysis_time, # Data do resumo
                "source": "Google News",
                "summary": summary
            })
        return news_items
    except Exception as e:
        update_tentacle_status("error", f"Falha News: {str(e)[:50]}")
        return []

def update_monitor():
    config = load_config()
    terms = config["searchTerms"]
    
    update_tentacle_status("active", f"Iniciando monitoramento de {len(terms)} tópicos...")
    
    news = fetch_google_news(terms)
    
    data = {
        "last_update": datetime.now().isoformat(),
        "search_terms": terms,
        "google_news": news
    }
    
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    update_tentacle_status("idle", f"Monitor atualizado com {len(news)} resumos de IA.")
    return config["refreshIntervalMinutes"]

if __name__ == "__main__":
    once = "--once" in sys.argv
    loop = "--loop" in sys.argv
    
    if loop:
        print("🔄 Modo MONITORAMENTO ATIVO iniciado (Ctrl+C para parar)")
        while True:
            interval = update_monitor()
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] 💤 Aguardando {interval} minutos para próxima atualização...")
            time.sleep(interval * 60)
    else:
        update_monitor()
