import asyncio
import json
import logging
import os
import re
import sys
import time as _time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from mcp_servers.google_mcp import gmail_tools, calendar_tools, sheets_tools
from mcp_servers.files_mcp import pdf_tools, pptx_tools
from mcp_servers.llm_bridge import server as llm_bridge
from logs.logger import log, log_octogent

# ── Configuração ───────────────────────────────────────────────────────────────
TELEGRAM_TOKEN  = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY    = os.getenv("GROQ_API_KEY")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "0"))

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
groq_client = Groq(api_key=GROQ_API_KEY)

# ── Dashboard bridge ───────────────────────────────────────────────────────────

ROOT_DIR = Path(__file__).parent.parent
OCTOGENT_API = "http://127.0.0.1:8787"
STATUS_DIR = ROOT_DIR / "outputs" / ".status"

def _is_allowed(user_id: int) -> bool:
    return user_id == ALLOWED_USER_ID

def _parse_json(text: str) -> any:
    # Limpa markdown blocks se houver
    text = re.sub(r"```json\s*|\s*```", "", text).strip()
    return json.loads(text)

def _groq(messages: list, temperature: float = 0.3, max_tokens: int = 1024) -> str:
    try:
        resp = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Erro Groq: {e}"

def _detect_intent(text: str) -> dict:
    prompt = f"""
    Analise a intenção do usuário abaixo e retorne um JSON com 'intent' e 'params'.
    Intenções possíveis:
    - gmail_list: listar emails recentes
    - gmail_summarize: resumir caixa de entrada
    - calendar_today: agenda de hoje
    - calendar_list: listar próximos eventos
    - calendar_create: criar evento (precisa de title, start e opcional description, end)
    - sheets_list: listar planilhas no drive
    - pdf_create: criar um documento PDF (precisa de topic)
    - pptx_create: criar uma apresentação PowerPoint (precisa de topic)
    - linkedin_post: criar um post para LinkedIn (precisa de topic)
    - linkedin_analyze: analisar notícias e sugerir posts (manual trigger)
    - general: conversa comum

    FORMATO: {{"intent": "...", "params": {{...}}}}
    USUÁRIO: {text}
    """
    raw = _groq([{"role": "user", "content": prompt}], temperature=0.1)
    try:
        return _parse_json(raw)
    except:
        return {"intent": "general", "params": {}}

# ── Handlers de Negócio ────────────────────────────────────────────────────────

def _handle_gmail_list() -> str:
    messages = gmail_tools.list_messages(max_results=5)
    if not messages:
        return "📭 Nenhum email encontrado."
    lines = [f"📧 *{m['assunto']}*\n   De: {m['remetente']}" for m in messages]
    return "📥 *Emails recentes:*\n\n" + "\n\n".join(lines)

def _handle_gmail_summarize() -> str:
    messages = gmail_tools.list_messages(max_results=10)
    if not messages:
        return "📭 Caixa de entrada vazia."
    context = "\n".join([f"Assunto: {m['assunto']} | De: {m['remetente']}" for m in messages])
    summary = _groq([
        {"role": "system", "content": "Resuma os emails abaixo em 3-4 pontos principais em português."},
        {"role": "user", "content": context}
    ])
    return f"📝 *Resumo da Inbox:*\n\n{summary}"

def _handle_calendar_today() -> str:
    events = calendar_tools.get_today_events()
    if not events:
        return "📅 Nenhum compromisso para hoje."
    lines = [f"⏰ {e['inicio'][11:16]} — *{e['titulo']}*" for e in events]
    return "📅 *Agenda de Hoje:*\n\n" + "\n".join(lines)

def _handle_calendar_list() -> str:
    events = calendar_tools.list_upcoming_events(max_results=10)
    if not events:
        return "📅 Nenhum evento futuro."
    lines = [f"📅 {e['inicio'][:10]} {e['inicio'][11:16]} — *{e['titulo']}*" for e in events]
    return "🗓️ *Próximos Eventos:*\n\n" + "\n".join(lines)

def _handle_calendar_create(params: dict) -> str:
    title = params.get("title", "")
    start = params.get("start", "")
    if not title or not start:
        return "Preciso do título e horário. Ex: _'Agendar reunião de vendas amanhã às 14h'_"
    end = params.get("end") or _add_one_hour(start)
    result = calendar_tools.create_event(title, start, end, params.get("description", ""), "")
    return f"✅ *Evento criado!*\n📅 {title}\n🕐 {start[:16]}"

def _add_one_hour(iso_date: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        return (dt + timedelta(hours=1)).isoformat()
    except:
        return iso_date

def _handle_sheets_list() -> str:
    sheets = sheets_tools.list_spreadsheets()
    if not sheets:
        return "📊 Nenhuma planilha encontrada no Drive."
    lines = [f"• *{s['nome']}*\n  ID: `{s['id']}`" for s in sheets]
    return "📊 *Suas planilhas:*\n\n" + "\n\n".join(lines)

def _handle_pdf_create(topic: str, title: str = "") -> tuple:
    title = title or topic
    raw = _groq([{"role": "user", "content":
        f"Escreva um documento profissional em português sobre: {topic}. "
        f"Divida em 3-4 seções. Retorne SOMENTE JSON: "
        f'[{{"heading":"Título da seção","body":"Texto completo..."}}]'
    }], temperature=0.5, max_tokens=1500)
    try:
        sections = _parse_json(raw)
    except Exception:
        sections = [{"heading": topic, "body": raw}]
    path = pdf_tools.create_pdf(title, sections)
    return str(path), f"✅ *PDF criado:* `{Path(path).name}`"

def _handle_pptx_create(topic: str, title: str = "") -> tuple:
    title = title or topic
    raw = _groq([{"role": "user", "content":
        f"Crie uma apresentação em português sobre: {topic}. "
        f"Retorne SOMENTE JSON com 5 slides:\n"
        f'[{{"type":"title","title":"{title}","subtitle":"Subtítulo descritivo"}},'
        f'{{"type":"content","title":"Tópico","bullets":["Ponto 1","Ponto 2","Ponto 3"]}},'
        f'{{"type":"content","title":"Tópico 2","bullets":["Ponto 1","Ponto 2"]}},'
        f'{{"type":"content","title":"Tópico 3","bullets":["Ponto 1","Ponto 2"]}},'
        f'{{"type":"closing","title":"Obrigado!","subtitle":"contato@Tentacles.ai"}}]'
    }], temperature=0.5, max_tokens=1500)
    try:
        slides = _parse_json(raw)
    except Exception:
        slides = [{"type": "title", "title": title, "subtitle": topic}]
    path = pptx_tools.create_presentation(title, slides)
    return str(path), f"✅ *Apresentação criada:* `{Path(path).name}`"

def _handle_linkedin_post(topic: str) -> str:
    text = _groq([
        {"role": "system", "content": "Você é especialista em conteúdo LinkedIn para o mercado tech brasileiro."},
        {"role": "user", "content":
            f"Escreva um post completo para LinkedIn sobre: {topic}. "
            f"Use emojis, tópicos curtos, linguagem direta e CTA criativo no final. "
            f"Entre 150-250 palavras. Retorne apenas o texto do post."
        },
    ], temperature=0.7, max_tokens=600)
    return f"💼 *Post LinkedIn pronto:*\n\n{text}"

def _handle_brain_status() -> str:
    try:
        status = llm_bridge.get_current_llm_config()
        return f"🧠 *Status do Cérebro Universal:*\n{status}\n\nPara mudar:\n`/brain provedor modelo`\n\nPara salvar chave:\n`/brain set_key NOME_DA_CHAVE VALOR`"
    except Exception as e:
        return f"❌ Erro ao ler config: {e}"

def _handle_brain_set(provider: str, model: str = None) -> str:
    try:
        result = llm_bridge.set_active_llm(provider, model)
        return result
    except Exception as e:
        return f"❌ Erro ao atualizar cérebro: {e}"

def _handle_general(user_msg: str) -> str:
    return _groq([
        {"role": "system", "content":
            "Você é o assistente Tentacles, agente de produtividade inteligente. "
            "Pode ajudar com Gmail, Calendar, Sheets, LinkedIn, PDFs e apresentações. "
            "Responda em português do Brasil de forma direta e útil."
        },
        {"role": "user", "content": user_msg},
    ], temperature=0.7)

# ── Dashboard Bridge ──────────────────────────────────────────────────────────

async def _execute_via_dashboard(update, task_id, name, tentacle_id, prompt, fallback_fn):
    try:
        # 1. Verifica se o Dashboard está online e pega o provedor preferido
        try:
            with urllib.request.urlopen(f"{OCTOGENT_API}/api/ui-state", timeout=2) as resp:
                ui_state = json.loads(resp.read().decode())
                preferred_provider = ui_state.get("preferredAgentProvider", "claude-code")
        except:
            preferred_provider = "claude-code"
            # Fallback para o fallback se o dashboard estiver offline
            log("telegram", "dashboard_offline", f"fallback para {tentacle_id}")
            if asyncio.iscoroutinefunction(fallback_fn):
                return await fallback_fn()
            return fallback_fn()

        # O payload e a requisição devem estar DENTRO do try principal
        payload = json.dumps({
            "name": name,
            "tentacleId": tentacle_id,
            "initialPrompt": prompt,
            "agentProvider": preferred_provider,
            "workspaceMode": "shared"
        }).encode()

        req = urllib.request.Request(f"{OCTOGENT_API}/api/terminals", data=payload)
        req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                terminal_id = data.get("terminalId")
        except Exception as e:
            log("telegram", "erro_dashboard_api", str(e))
            if asyncio.iscoroutinefunction(fallback_fn):
                return await fallback_fn()
            return fallback_fn()

        await update.message.reply_text(f"🚀 Enviado para o Dashboard via Agente `{preferred_provider}` (ID: `{terminal_id}`).\nAguardando conclusão...")

        # O arquivo .done deve ser gerado com o terminal_id
        status_file = STATUS_DIR / f"{terminal_id}.done"
        STATUS_DIR.mkdir(parents=True, exist_ok=True)

        max_retries = 40 # Aumentado para 160 segundos
        for _ in range(max_retries):
            if status_file.exists():
                file_path = status_file.read_text().strip()
                # Se for um arquivo temporário de status que contém o path
                if os.path.exists(file_path):
                    status_file.unlink()
                    return file_path, f"✅ Tarefa concluída via Dashboard!"
                else:
                    # Se o arquivo .done for apenas uma flag
                    status_file.unlink()
                    return None, f"✅ Tarefa concluída!"
            await asyncio.sleep(4)

        return None, "⚠️ Timeout: A tarefa está demorando muito no Dashboard. Verifique a tela de terminais."

    except Exception as e:
        log("telegram", "erro_geral_dashboard", str(e))
        return None, f"❌ Erro ao comunicar com Dashboard: {e}"

# ── Handlers Telegram ─────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ Acesso não autorizado.")
        return
    log_octogent("telegram", "bot_iniciado")
    await update.message.reply_text(
        "👋 Olá! Sou o assistente *Tentacles*.\n\n"
        "📧 /gmail — Emails recentes\n"
        "📅 /agenda — Agenda de hoje\n"
        "📊 /planilhas — Listar planilhas\n"
        "💼 /linkedin — Criar post LinkedIn\n"
        "📄 /pdf — Criar documento PDF\n"
        "📊 /pptx — Criar apresentação\n"
        "🧠 /brain — Configurar IA (Grok, Gemini, etc)\n\n"
        "Ou simplesmente me diga o que precisa! 🚀",
        parse_mode="Markdown",
    )

async def cmd_gmail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    await update.message.chat.send_action("typing")
    try:
        result = _handle_gmail_list()
        log("telegram", "gmail_list"); log_octogent("telegram", "gmail_list")
    except Exception as e:
        result = f"❌ Erro Gmail: {str(e)[:200]}"
    await _reply(update, result)

async def cmd_agenda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    await update.message.chat.send_action("typing")
    try:
        result = _handle_calendar_today()
        log("telegram", "calendar_today"); log_octogent("telegram", "calendar_today")
    except Exception as e:
        result = f"❌ Erro Calendar: {str(e)[:200]}"
    await _reply(update, result)

async def cmd_planilhas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    await update.message.chat.send_action("typing")
    try:
        result = _handle_sheets_list()
        log("telegram", "sheets_list"); log_octogent("telegram", "sheets_list")
    except Exception as e:
        result = f"❌ Erro Sheets: {str(e)[:200]}"
    await _reply(update, result)

async def cmd_linkedin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    await update.message.reply_text("💼 Escolha uma opção:\n\n1. Escrever sobre um *tema específico* (digite o tema)\n2. *Analisar tendências* e sugerir posts (digite 'analisar')")
    context.user_data["pending"] = "linkedin_choice"

async def cmd_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    await update.message.reply_text("📄 Sobre qual assunto você quer criar o PDF?")
    context.user_data["pending"] = "pdf_create"

async def cmd_pptx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    await update.message.reply_text("📊 Sobre qual assunto você quer criar a apresentação?")
    context.user_data["pending"] = "pptx_create"

async def cmd_brain(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    args = context.args
    if not args:
        await update.message.reply_text(_handle_brain_status(), parse_mode="Markdown")
        return
    
    subcmd = args[0].lower()
    if subcmd == "set_key" and len(args) >= 3:
        key_name = args[1].upper()
        key_value = args[2]
        result = llm_bridge.update_env_key(key_name, key_value)
        await update.message.reply_text(result)
        return

    provider = subcmd
    model = args[1] if len(args) > 1 else None
    result = _handle_brain_set(provider, model)
    await update.message.reply_text(result)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ Acesso não autorizado.")
        return

    user_msg = update.message.text
    await update.message.chat.send_action("typing")
    log("telegram", "mensagem", user_msg[:80])
    log_octogent("telegram", "mensagem_recebida", user_msg[:60])

    pending = context.user_data.pop("pending", None)
    
    if pending == "linkedin_choice":
        if "analisar" in user_msg.lower():
            await update.message.reply_text("🔍 Buscando tendências e preparando análise no Dashboard...")
            task_id = f"ln-an-{int(_time.time())}"
            prompt = (
                "Voce e o agente linkedin-poster do Tentacles.\n"
                "TAREFA: Busque noticias trending via Google News, analise-as e sugira 3 temas de posts.\n"
                "Depois de analisar, gere um post completo para o tema mais forte, gere a imagem e publique.\n"
                "Ao final, escreva 'POST_DONE: [TEMA]' no canal tentacles-events."
            )
            file_path, result = await _execute_via_dashboard(
                update, task_id, "LinkedIn: Análise de Tendências", "linkedin-poster",
                prompt, lambda: "⚠️ Dashboard offline. Não consigo buscar notícias em tempo real agora."
            )
            await _reply(update, result, file_path)
            return
        else:
            try:
                result = _handle_linkedin_post(user_msg)
                log_octogent("telegram", "linkedin_post_gerado", user_msg[:50])
            except Exception as e:
                result = f"❌ Erro: {str(e)[:200]}"
            await _reply(update, result)
            return

    if pending == "pdf_create":
        await update.message.chat.send_action("upload_document")
        task_id = f"pdf-{int(_time.time())}"
        prompt = (
            f"Voce e o agente files-assistant do Tentacles.\n"
            f"TAREFA: Crie um PDF profissional em portugues sobre: {user_msg}.\n"
            f"Use a ferramenta MCP pdf_create.\n"
            f"Ao concluir, grave o caminho do PDF em outputs/.status/{task_id}.done"
        )
        file_path, result = await _execute_via_dashboard(
            update, task_id, f"PDF: {user_msg[:25]}", "files-assistant",
            prompt, lambda: _handle_pdf_create(user_msg),
        )
        await _reply(update, result, file_path)
        return

    if pending == "pptx_create":
        await update.message.chat.send_action("upload_document")
        task_id = f"pptx-{int(_time.time())}"
        prompt = (
            f"Voce e o agente files-assistant do Tentacles.\n"
            f"TAREFA: Crie um PowerPoint profissional em portugues sobre: {user_msg}.\n"
            f"Use a ferramenta MCP pptx_create.\n"
            f"Ao concluir, grave o caminho do arquivo em outputs/.status/{task_id}.done"
        )
        file_path, result = await _execute_via_dashboard(
            update, task_id, f"PPTX: {user_msg[:25]}", "files-assistant",
            prompt, lambda: _handle_pptx_create(user_msg),
        )
        await _reply(update, result, file_path)
        return

    detected = _detect_intent(user_msg)
    intent = detected.get("intent", "general")
    params = detected.get("params", {})

    file_path = None
    try:
        if intent == "linkedin_analyze":
            await update.message.reply_text("🔍 Analisando tendências no Dashboard...")
            task_id = f"ln-an-{int(_time.time())}"
            prompt = "Buscando noticias e gerando post automatico no Dashboard..."
            file_path, result = await _execute_via_dashboard(update, task_id, "LinkedIn: Auto Análise", "linkedin-poster", prompt, lambda: "Dashboard offline.")
        elif intent == "linkedin_post":
            result = _handle_linkedin_post(params.get("topic", user_msg))
        elif intent == "gmail_list":
            result = _handle_gmail_list()
        elif intent == "calendar_today":
            result = _handle_calendar_today()
        else:
            result = _handle_general(user_msg)
    except Exception as e:
        result = f"❌ Erro: {str(e)[:300]}"

    await _reply(update, result, file_path)

async def _reply(update: Update, text: str, file_path: str = None):
    if file_path and os.path.exists(file_path):
        await update.message.reply_document(document=open(file_path, "rb"), caption=text, parse_mode="Markdown")
        return
    for i in range(0, len(text), 4000):
        await update.message.reply_text(text[i:i+4000], parse_mode="Markdown")

def main():
    if not TELEGRAM_TOKEN:
        print("❌ ERRO: TELEGRAM_BOT_TOKEN não encontrado no .env")
        return

    print("=" * 55)
    print("   Telegram Bot Tentacles — Iniciando...")
    print("=" * 55)

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start",     cmd_start))
    app.add_handler(CommandHandler("gmail",     cmd_gmail))
    app.add_handler(CommandHandler("agenda",    cmd_agenda))
    app.add_handler(CommandHandler("planilhas", cmd_planilhas))
    app.add_handler(CommandHandler("linkedin",  cmd_linkedin))
    app.add_handler(CommandHandler("pdf",       cmd_pdf))
    app.add_handler(CommandHandler("pptx",      cmd_pptx))
    app.add_handler(CommandHandler("brain",     cmd_brain))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    max_retries = 5
    for attempt in range(max_retries):
        try:
            print(f"📡 Tentativa de conexão {attempt + 1}/{max_retries}...")
            log_octogent("telegram", "bot_iniciado", "polling ativo")
            app.run_polling(close_loop=False)
            break
        except Exception as e:
            print(f"⚠️ Erro de rede no Telegram: {e}")
            if attempt < max_retries - 1:
                _time.sleep(10)
            else:
                print("❌ Falha crítica ao conectar no Telegram após várias tentativas.")

if __name__ == "__main__":
    main()
