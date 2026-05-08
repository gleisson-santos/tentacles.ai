import feedparser
import json
import os
import sys
import time
import httpx
import asyncio
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

async def update_tentacle_status(state, detail=""):
    """
    Atualiza o estado visual e log do tentáculo no Dashboard.
    """
    api_url = get_octogent_api()
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{state.upper()}] {detail}")
    
    try:
        msg = f"[TENTACLE:{TENTACULO_ID}] {state.upper()}: {detail}"
        async with httpx.AsyncClient(timeout=1) as client:
            # Envia mensagem para o canal
            await client.post(f"{api_url}/api/channels/tentacles-events/messages", json={
                "fromTerminalId": "trends-monitor-script",
                "content": msg
            })
            
            # Tenta atualizar o status diretamente para forçar animação se suportado
            try:
                await client.post(f"{api_url}/api/deck/tentacles/{TENTACULO_ID}/status", json={
                    "status": "working" if state.lower() in ["active", "processing"] else "idle",
                    "label": detail[:30]
                })
            except:
                pass
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

async def summarize_news(title, source):
    """
    Usa Groq para criar um resumo rápido e atraente da notícia.
    """
    try:
        prompt = f"Crie um resumo atraente e informativo (em 2-3 parágrafos) sobre esta notícia: '{title}'. Fonte: {source}. Foco em impacto tecnológico e tendências de mercado."
        
        # Faz a chamada Groq de forma não bloqueante
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Resumo temporariamente indisponível. (Erro: {e})"

async def fetch_google_news(terms):
    clean_terms = [t.strip().replace("\n", "").replace("\r", "") for t in terms[:5]]
    query = " OR ".join([f'"{t}"' for t in clean_terms])
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    
    try:
        # feedparser é síncrono, rodamos em thread
        feed = await asyncio.to_thread(feedparser.parse, url)
        news_items = []
        # Pegamos os 5 mais recentes para resumir
        for entry in feed.entries[:5]:
            await update_tentacle_status("processing", f"Resumindo: {entry.title[:30]}...")
            summary = await summarize_news(entry.title, "Google News")
            
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
        await update_tentacle_status("error", f"Falha News: {str(e)[:50]}")
        return []

async def update_monitor():
    config = load_config()
    terms = config["searchTerms"]
    
    await update_tentacle_status("active", f"Iniciando monitoramento de {len(terms)} tópicos...")
    
    news = await fetch_google_news(terms)
    
    data = {
        "last_update": datetime.now().isoformat(),
        "search_terms": terms,
        "google_news": news
    }
    
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    await update_tentacle_status("idle", f"Monitor atualizado com {len(news)} resumos de IA.")
    return config["refreshIntervalMinutes"]

async def main_async():
    once = "--once" in sys.argv
    loop = "--loop" in sys.argv
    
    if loop:
        print("🔄 Modo MONITORAMENTO ATIVO iniciado (Ctrl+C para parar)")
        while True:
            interval = await update_monitor()
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] 💤 Aguardando {interval} minutos para próxima atualização...")
            await asyncio.sleep(interval * 60)
    else:
        await update_monitor()

if __name__ == "__main__":
    asyncio.run(main_async())
