"""
Auto LinkedIn Poster
Busca notícias trending no Google News, analisa com Groq (LLaMA),
gera imagem minimalista com Stability AI e publica no LinkedIn.
"""
import json
import os
import re
import tempfile
import time

import feedparser
import httpx
import requests
from groq import Groq
from logs.logger import log, log_octogent

# ── Configurações ──────────────────────────────────────────────────────────────
GROQ_API_KEY     = os.getenv("GROQ_API_KEY")
STABILITY_KEY    = os.getenv("STABILITY_KEY")
TOKEN_FILE       = os.path.expanduser("~/.linkedin_mcp_token.json")
INTERVAL_SECONDS = 2 * 60 * 60  # 2 horas (modo produção)

TOPICS = [
    "n8n automation workflow",
    "Claude Code Anthropic",
    "Manus AI agent",
    "ChatGPT OpenAI",
    "Google Gemini AI",
    "Power BI Microsoft",
    "inteligência artificial automação",
    "AI agents productivity",
    "LLM large language model",
    "no-code automation tools",
]

# Paleta por tópico para imagens consistentes e profissionais
TOPIC_STYLES = {
    "n8n":        ("interconnected nodes forming a clean flow diagram, minimalist",        "#FF6D42", "#FFFFFF"),
    "claude":     ("simple diamond speech bubble with small spark icon",                   "#D4682D", "#FFF8F4"),
    "manus":      ("minimal robotic hand making a precise gesture, flat icon",             "#6C63FF", "#FFFFFF"),
    "chatgpt":    ("simple speech bubble with subtle circuit line inside",                 "#10A37F", "#FFFFFF"),
    "gemini":     ("minimal colorful geometric gem shape, flat design",                    "#4285F4", "#FFFFFF"),
    "power bi":   ("clean bar chart with one highlighted column, minimal",                 "#F2C811", "#FFFFFF"),
    "automação":  ("three gears interlocking, flat minimal icon style",                    "#0077B5", "#F0F8FF"),
    "ai agent":   ("minimal abstract brain made of simple dots and lines",                 "#7B2FBE", "#FFFFFF"),
    "llm":        ("simple stacked horizontal lines becoming a lightbulb shape",           "#FF4B4B", "#FFFFFF"),
    "no-code":    ("minimal drag-and-drop blocks snapping together, flat icon",            "#00C9A7", "#FFFFFF"),
}

def _get_style(topic: str) -> tuple[str, str, str]:
    topic_lower = topic.lower()
    for key, style in TOPIC_STYLES.items():
        if key in topic_lower:
            return style
    return ("abstract minimal tech icon, simple geometric shape", "#0077B5", "#FFFFFF")


# ── 1. Buscar notícias ─────────────────────────────────────────────────────────
def fetch_news() -> list[dict]:
    articles = []
    for topic in TOPICS:
        query = topic.replace(" ", "+")
        url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt"
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
                summary = re.sub(r"<[^>]+>", "", entry.get("summary", ""))
                articles.append({
                    "topic": topic,
                    "title": entry.get("title", ""),
                    "summary": summary[:400],
                    "published": entry.get("published", ""),
                })
        except Exception as e:
            print(f"    Erro RSS [{topic}]: {e}")
    return articles


# ── 2a. Escrever post via Groq (modo IA) ─────────────────────────────────────
def analyze_and_write_groq(articles: list[dict]) -> dict:
    client = Groq(api_key=GROQ_API_KEY)

    articles_text = "\n---\n".join([
        f"Tópico: {a['topic']}\nTítulo: {a['title']}\nResumo: {a['summary']}"
        for a in articles[:16]
    ])

    prompt = f"""Você é especialista em conteúdo LinkedIn para o mercado tech brasileiro.

Analise as notícias abaixo e:
1. Escolha a de MAIOR potencial de engajamento no LinkedIn BR (relevância + novidade + impacto)
2. Escreva um post completo em português do Brasil com:
   - Gancho forte na 1a linha (sem emoji na abertura)
   - Desenvolvimento em tópicos curtos com emojis
   - Linguagem direta, sem enrolação
   - CTA criativo no final (ex: "Comente FLOW que te mando o passo a passo", "Comente IA que envio o guia")
3. O post deve ter entre 150 e 250 palavras

NOTICIAS:
{articles_text}

Retorne SOMENTE JSON valido, sem markdown:
{{
  "topic": "topico escolhido",
  "title": "titulo da noticia",
  "post": "texto completo do post LinkedIn",
  "image_concept": "conceito visual minimalista em ingles (ex: connected workflow nodes, chat bubble with lightning)"
}}"""

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024,
    )
    text = resp.choices[0].message.content.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


# ── 2b. Escrever post via template (modo fallback, sem IA) ────────────────────
CTAS = [
    "Comente IA aqui que te mando o passo a passo completo",
    "Comente STACK que envio o guia de ferramentas que uso",
    "Comente FLOW que te mando o tutorial gratuito",
    "Comente SIM se voce ja usa isso no seu trabalho",
    "Comente AGENTE que mando o framework que estou usando",
]

def analyze_and_write_template(articles: list[dict]) -> dict:
    # Prioriza artigos dos topicos mais estrategicos
    priority = ["claude", "n8n", "chatgpt", "gemini", "manus", "power bi", "ai agent"]
    chosen = None
    for prio in priority:
        for a in articles:
            if prio in a["topic"].lower():
                chosen = a
                break
        if chosen:
            break
    if not chosen:
        chosen = articles[0]

    cta = CTAS[hash(chosen["title"]) % len(CTAS)]
    topic_upper = chosen["topic"].split()[0].upper()

    summary_clean = chosen["summary"][:300].rstrip(".")
    title_clean = re.sub(r"\s*-\s*.*$", "", chosen["title"]).strip()

    post = f"""{title_clean}

Esse e o tipo de novidade que esta mudando como profissionais de tecnologia trabalham.

O que esta em jogo:

🔵 As ferramentas de IA estao evoluindo mais rapido do que a maioria das equipes consegue acompanhar
🔵 Quem entende o ecossistema hoje vai liderar os projetos de amanha
🔵 A diferenca entre usar IA e dominar IA esta ficando cada vez maior

{summary_clean}

O mercado nao espera.
Voce ja esta acompanhando essas mudancas?

💬 {cta} 👇"""

    return {
        "topic": chosen["topic"],
        "title": chosen["title"],
        "post": post,
        "image_concept": "abstract minimal tech icon with connected dots",
    }


def analyze_and_write(articles: list[dict]) -> dict:
    try:
        result = analyze_and_write_groq(articles)
        print("        Modo: Groq AI (LLaMA 3.3 70B)")
        return result
    except Exception as e:
        print(f"        Groq indisponivel ({str(e)[:60]}...), usando template.")
        return analyze_and_write_template(articles)


# ── 3. Gerar imagem minimalista ────────────────────────────────────────────────
def generate_image(topic: str, concept: str) -> str:
    visual_concept, accent_color, bg_color = _get_style(topic)

    prompt = (
        f"Minimalist flat vector illustration, {visual_concept}, "
        f"pure white background, maximum 2 colors, accent color {accent_color}, "
        f"clean professional design, simple geometric shapes, "
        f"modern app icon aesthetic, centered composition, generous whitespace, "
        f"no text, no letters, no numbers, no people, no faces"
    )
    negative = (
        "text, letters, words, watermark, signature, people, face, body, robot, android, "
        "photorealistic, 3d render, dark background, neon, glow, gradient overload, "
        "complex scene, cluttered, busy, low quality, blurry, noise"
    )

    resp = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={"authorization": f"Bearer {STABILITY_KEY}", "accept": "image/*"},
        files={"none": ""},
        data={
            "prompt": prompt,
            "negative_prompt": negative,
            "output_format": "jpeg",
            "aspect_ratio": "1:1",
        },
        timeout=60,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"Stability AI {resp.status_code}: {resp.text[:200]}")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg", dir=os.path.expanduser("~"))
    tmp.write(resp.content)
    tmp.close()
    return tmp.name


# ── 4. Publicar no LinkedIn ────────────────────────────────────────────────────
def publish(post_text: str, image_path: str) -> str:
    with open(TOKEN_FILE) as f:
        token_data = json.load(f)
    access_token = token_data["access_token"]
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    with httpx.Client(timeout=30) as client:
        person_urn = "urn:li:person:" + client.get(
            "https://api.linkedin.com/v2/userinfo", headers=headers
        ).json()["sub"]

        reg = client.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            headers=headers,
            json={
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": person_urn,
                    "serviceRelationships": [
                        {"relationshipType": "OWNER", "identifier": "urn:li:userGeneratedContent"}
                    ],
                }
            },
        )
        data = reg.json()["value"]
        upload_url = data["uploadMechanism"][
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]["uploadUrl"]
        asset_urn = data["asset"]

        with open(image_path, "rb") as img:
            client.put(
                upload_url,
                content=img.read(),
                headers={"Authorization": "Bearer " + access_token, "Content-Type": "image/jpeg"},
            )

        resp = client.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers,
            json={
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": post_text},
                        "shareMediaCategory": "IMAGE",
                        "media": [{
                            "status": "READY",
                            "description": {"text": post_text[:200]},
                            "media": asset_urn,
                            "title": {"text": post_text[:100]},
                        }],
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
            },
        )

    if resp.status_code in (200, 201):
        return resp.headers.get("x-restli-id", "N/A")
    raise RuntimeError(f"LinkedIn {resp.status_code}: {resp.text[:300]}")


# ── Loop principal ─────────────────────────────────────────────────────────────
def run_cycle():
    sep = "=" * 55
    print(f"\n{sep}")
    print(f"  Ciclo iniciado às {time.strftime('%H:%M:%S')}")
    print(sep)

    print("  [1/4] Buscando notícias no Google News...")
    articles = fetch_news()
    print(f"        {len(articles)} artigos coletados de {len(TOPICS)} tópicos")

    print("  [2/4] Analisando e escrevendo post com Groq AI...")
    result = analyze_and_write(articles)
    print(f"        Tema:  {result['topic']}")
    print(f"        Título: {result['title'][:70]}...")

    print("  [3/4] Gerando imagem minimalista com Stability AI...")
    image_path = generate_image(result["topic"], result["image_concept"])
    print(f"        Imagem salva: {image_path}")

    print("  [4/4] Publicando no LinkedIn...")
    post_id = publish(result["post"], image_path)
    print(f"        Publicado! ID: {post_id}")
    log("linkedin", "post_publicado", f"tema={result['topic']} | id={post_id}")
    log_octogent("linkedin", "post_publicado", f"tema={result['topic']}")

    try:
        os.remove(image_path)
    except OSError:
        pass

    print(f"\n  Próximo ciclo em {INTERVAL_SECONDS // 60} minuto(s) — {time.strftime('%H:%M:%S', time.localtime(time.time() + INTERVAL_SECONDS))}")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 55)
    print("   Auto LinkedIn Poster  -  Clilink")
    print("=" * 55)
    print(f"  Intervalo : {INTERVAL_SECONDS // 60} min(s)")
    print(f"  Topicos   : {len(TOPICS)} categorias monitoradas")
    print("  Pressione Ctrl+C para parar\n")

    while True:
        try:
            run_cycle()
        except KeyboardInterrupt:
            print("\n\n  Encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"\n  ERRO no ciclo: {e}")
            log("linkedin", "erro_ciclo", str(e)[:200])
            print(f"  Tentando novamente em {INTERVAL_SECONDS // 60} minuto(s)...")
        time.sleep(INTERVAL_SECONDS)
