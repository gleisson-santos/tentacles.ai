"""
Telegram Bot — Assistente Clilink
Detecta intenção via Groq e executa ações reais (Gmail, Calendar, Sheets, PDF, PPTX, LinkedIn).
"""
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

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from mcp_servers.google_mcp import gmail_tools, calendar_tools, sheets_tools
from mcp_servers.files_mcp import pdf_tools, pptx_tools
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


def _octogent_running() -> bool:
    """Verifica se o servidor Octogent está no ar via HTTP."""
    try:
        urllib.request.urlopen(f"{OCTOGENT_API}/api/deck/tentacles", timeout=2)
        return True
    except Exception:
        return False


def _spawn_terminal(task_id: str, name: str, tentacle_id: str, prompt: str) -> str | None:
    """Cria um terminal visível no Dashboard via API HTTP. Retorna terminal_id ou None."""
    status_file = STATUS_DIR / f"{task_id}.done"
    STATUS_DIR.mkdir(parents=True, exist_ok=True)

    full_prompt = (
        f"{prompt}\n\n"
        f"IMPORTANTE: Quando o arquivo estiver criado, execute exatamente este comando Bash:\n"
        f"echo <caminho_do_arquivo> > \"{status_file}\"\n"
        f"(substitua <caminho_do_arquivo> pelo caminho absoluto real do arquivo gerado, sem espacos extras)"
    )

    payload = json.dumps({
        "name": name,
        "tentacleId": tentacle_id,
        "initialPrompt": full_prompt,
        "workspaceMode": "shared",
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            f"{OCTOGENT_API}/api/terminals",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("terminalId")
    except Exception:
        return None


async def _poll_result(task_id: str, timeout: int = 120) -> str | None:
    """Aguarda arquivo de status gerado pelo terminal do Dashboard."""
    status_file = STATUS_DIR / f"{task_id}.done"
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        await asyncio.sleep(3)
        if status_file.exists():
            path = status_file.read_text(encoding="utf-8").strip()
            status_file.unlink(missing_ok=True)
            return path
    return None


async def _execute_via_dashboard(
    update,
    task_id: str,
    terminal_name: str,
    tentacle_id: str,
    prompt: str,
    fallback_fn,
) -> tuple:
    """
    Tenta executar via terminal do Dashboard.
    Se Octogent não estiver rodando ou der timeout, usa fallback_fn() direto.
    Retorna (file_path, result_text).
    """
    if not _octogent_running():
        log("telegram", "octogent_offline_fallback", terminal_name)
        return fallback_fn()

    status = await update.message.reply_text(
        "Tarefa enviada para o *Dashboard Octogent*!\n"
        "Acompanhe o tentaculo trabalhando em tempo real.\n"
        "O arquivo chegara aqui assim que ficar pronto...",
        parse_mode="Markdown",
    )
    log_octogent("telegram", "spawning_terminal", terminal_name)

    terminal_id = _spawn_terminal(task_id, terminal_name, tentacle_id, prompt)
    if not terminal_id:
        await status.edit_text("Dashboard nao respondeu, criando diretamente...")
        return fallback_fn()

    # Pausa mínima para a animação do Dashboard ser visível
    await asyncio.sleep(5)

    # Aguarda resultado no canal
    result_path = await _poll_result(task_id, timeout=90)

    if result_path and Path(result_path).exists():
        await status.delete()
        log_octogent("telegram", "terminal_concluiu", result_path)
        fname = Path(result_path).name
        return result_path, f"Arquivo criado pelo Dashboard: `{fname}`"

    # Timeout — cria direto como fallback
    await status.edit_text("Tempo esgotado no Dashboard, criando diretamente...")
    return fallback_fn()


def _is_allowed(user_id: int) -> bool:
    return ALLOWED_USER_ID == 0 or user_id == ALLOWED_USER_ID


def _groq(messages: list, temperature: float = 0.3, max_tokens: int = 1024) -> str:
    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def _parse_json(text: str) -> dict:
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def _add_one_hour(dt_str: str) -> str:
    return (datetime.fromisoformat(dt_str) + timedelta(hours=1)).isoformat()


# ── Detecção de intenção ────────────────────────────────────────────────────────

def _detect_intent(user_msg: str) -> dict:
    today = datetime.now().strftime("%Y-%m-%d")
    weekday = datetime.now().strftime("%A")
    prompt = f"""Analise a mensagem e retorne SOMENTE JSON válido:
{{"intent": "<intent>", "params": {{}}}}

Intents disponíveis:
- gmail_list       → listar emails, ver caixa de entrada
- gmail_summarize  → resumo/quantidade de emails
- calendar_today   → agenda hoje, compromissos de hoje
- calendar_list    → próximos eventos, agenda semana
- calendar_create  → criar/agendar/marcar evento ou reunião
  params: {{"title":"","start":"YYYY-MM-DDTHH:MM:00","end":"YYYY-MM-DDTHH:MM:00","description":""}}
- sheets_list      → listar planilhas do Drive
- pdf_create       → criar PDF ou documento
  params: {{"title":"","topic":""}}
- pptx_create      → criar apresentação/slides/PowerPoint
  params: {{"title":"","topic":""}}
- linkedin_post    → criar/escrever post para LinkedIn
  params: {{"topic":""}}
- general          → qualquer outra conversa ou pergunta

Hoje é {today} ({weekday}). Calcule datas relativas ("amanhã", "sexta-feira", etc.).
Para horários sem data, assuma hoje. Para "às 14h" use T14:00:00.

Mensagem: "{user_msg}"
"""
    try:
        return _parse_json(_groq([{"role": "user", "content": prompt}]))
    except Exception:
        return {"intent": "general", "params": {}}


# ── Handlers de ação ───────────────────────────────────────────────────────────

def _handle_gmail_list() -> str:
    emails = gmail_tools.list_emails(10)
    if not emails:
        return "📧 Caixa de entrada vazia."
    lines = [
        f"*{i+1}.* [{e['date'][:16]}]\n  De: {e['from'][:40]}\n  {e['subject']}"
        for i, e in enumerate(emails)
    ]
    return f"📧 *{len(emails)} emails recentes:*\n\n" + "\n\n".join(lines)


def _handle_gmail_summarize() -> str:
    emails = gmail_tools.summarize_inbox(20)
    if not emails:
        return "📧 Caixa de entrada vazia."
    lines = [f"{i+1}. [{e['data'][:10]}] {e['de'][:30]} — {e['assunto']}" for i, e in enumerate(emails)]
    return f"📬 *Resumo — {len(emails)} emails:*\n\n" + "\n".join(lines)


def _handle_calendar_today() -> str:
    events = calendar_tools.get_today_schedule()
    if not events:
        return "📅 Nenhum evento hoje. Dia livre!"
    lines = [f"• {e['inicio'][11:16]} — *{e['titulo']}*" for e in events]
    return "📅 *Sua agenda de hoje:*\n" + "\n".join(lines)


def _handle_calendar_list() -> str:
    events = calendar_tools.list_events(7)
    if not events:
        return "📅 Nenhum evento nos próximos 7 dias."
    lines = [f"📅 {e['inicio'][:16]} — *{e['titulo']}*" for e in events]
    return "*Próximos 7 dias:*\n" + "\n".join(lines)


def _handle_calendar_create(params: dict) -> str:
    title = params.get("title", "")
    start = params.get("start", "")
    if not title or not start:
        return "Preciso do título e horário. Ex: _'Agendar reunião de vendas amanhã às 14h'_"
    end = params.get("end") or _add_one_hour(start)
    result = calendar_tools.create_event(title, start, end, params.get("description", ""), "")
    return f"✅ *Evento criado!*\n📅 {title}\n🕐 {start[:16]}"


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
        f'{{"type":"closing","title":"Obrigado!","subtitle":"contato@clilink.ai"}}]'
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


def _handle_general(user_msg: str) -> str:
    return _groq([
        {"role": "system", "content":
            "Você é o assistente Clilink, agente de produtividade inteligente. "
            "Pode ajudar com Gmail, Calendar, Sheets, LinkedIn, PDFs e apresentações. "
            "Responda em português do Brasil de forma direta e útil."
        },
        {"role": "user", "content": user_msg},
    ], temperature=0.7)


# ── Envio de mensagem (com suporte a arquivos) ─────────────────────────────────

async def _reply(update: Update, text: str, file_path: str = None):
    if file_path and os.path.exists(file_path):
        await update.message.reply_document(
            document=open(file_path, "rb"),
            caption=text,
            parse_mode="Markdown",
        )
        return
    for i in range(0, len(text), 4000):
        await update.message.reply_text(text[i:i+4000], parse_mode="Markdown")


# ── Comandos /cmd ──────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ Acesso não autorizado.")
        return
    log_octogent("telegram", "bot_iniciado")
    await update.message.reply_text(
        "👋 Olá! Sou o assistente *Clilink*.\n\n"
        "📧 /gmail — Emails recentes\n"
        "📅 /agenda — Agenda de hoje\n"
        "📊 /planilhas — Listar planilhas\n"
        "💼 /linkedin — Criar post LinkedIn\n"
        "📄 /pdf — Criar documento PDF\n"
        "📊 /pptx — Criar apresentação\n\n"
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
    await update.message.reply_text("✍️ Qual tema você quer para o post LinkedIn?")
    context.user_data["pending"] = "linkedin_post"


async def cmd_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    await update.message.reply_text("📄 Sobre qual assunto você quer criar o PDF?")
    context.user_data["pending"] = "pdf_create"


async def cmd_pptx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id): return
    await update.message.reply_text("📊 Sobre qual assunto você quer criar a apresentação?")
    context.user_data["pending"] = "pptx_create"


# ── Handler principal de mensagens ─────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("⛔ Acesso não autorizado.")
        return

    user_msg = update.message.text
    await update.message.chat.send_action("typing")
    log("telegram", "mensagem", user_msg[:80])
    log_octogent("telegram", "mensagem_recebida", user_msg[:60])

    # Ações pendentes dos comandos /pdf /pptx /linkedin
    pending = context.user_data.pop("pending", None)
    if pending == "linkedin_post":
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
            f"Voce e o agente files-assistant do Clilink.\n"
            f"Leia .octogent/tentacles/files-assistant/CONTEXT.md para contexto.\n\n"
            f"TAREFA: Crie um PDF profissional em portugues com titulo '{user_msg}'.\n"
            f"Use a ferramenta MCP pdf_create com 3-4 secoes bem elaboradas.\n"
            f"O arquivo sera salvo em outputs/pdfs/ automaticamente."
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
            f"Voce e o agente files-assistant do Clilink.\n"
            f"Leia .octogent/tentacles/files-assistant/CONTEXT.md para contexto.\n\n"
            f"TAREFA: Crie uma apresentacao PowerPoint profissional em portugues sobre '{user_msg}'.\n"
            f"Use a ferramenta MCP pptx_create com 5 slides profissionais.\n"
            f"O arquivo sera salvo em outputs/presentations/ automaticamente."
        )
        file_path, result = await _execute_via_dashboard(
            update, task_id, f"PPTX: {user_msg[:25]}", "files-assistant",
            prompt, lambda: _handle_pptx_create(user_msg),
        )
        await _reply(update, result, file_path)
        return

    # Detecção automática de intenção
    detected = _detect_intent(user_msg)
    intent = detected.get("intent", "general")
    params = detected.get("params", {})

    file_path = None
    try:
        if intent == "gmail_list":
            result = _handle_gmail_list()
        elif intent == "gmail_summarize":
            result = _handle_gmail_summarize()
        elif intent == "calendar_today":
            result = _handle_calendar_today()
        elif intent == "calendar_list":
            result = _handle_calendar_list()
        elif intent == "calendar_create":
            result = _handle_calendar_create(params)
        elif intent == "sheets_list":
            result = _handle_sheets_list()
        elif intent == "pdf_create":
            await update.message.chat.send_action("upload_document")
            topic = params.get("topic", user_msg)
            title = params.get("title", "") or topic
            task_id = f"pdf-{int(_time.time())}"
            prompt = (
                f"Voce e o agente files-assistant do Clilink.\n"
                f"Leia .octogent/tentacles/files-assistant/CONTEXT.md para contexto.\n\n"
                f"TAREFA: Crie um PDF profissional em portugues com titulo '{title}' sobre: {topic}.\n"
                f"Use a ferramenta MCP pdf_create com 3-4 secoes bem elaboradas.\n"
                f"O arquivo sera salvo em outputs/pdfs/ automaticamente."
            )
            file_path, result = await _execute_via_dashboard(
                update, task_id, f"PDF: {title[:25]}", "files-assistant",
                prompt, lambda: _handle_pdf_create(topic, title),
            )
        elif intent == "pptx_create":
            await update.message.chat.send_action("upload_document")
            topic = params.get("topic", user_msg)
            title = params.get("title", "") or topic
            task_id = f"pptx-{int(_time.time())}"
            prompt = (
                f"Voce e o agente files-assistant do Clilink.\n"
                f"Leia .octogent/tentacles/files-assistant/CONTEXT.md para contexto.\n\n"
                f"TAREFA: Crie uma apresentacao PowerPoint sobre '{topic}' com titulo '{title}'.\n"
                f"Use a ferramenta MCP pptx_create com 5 slides profissionais em portugues.\n"
                f"O arquivo sera salvo em outputs/presentations/ automaticamente."
            )
            file_path, result = await _execute_via_dashboard(
                update, task_id, f"PPTX: {title[:25]}", "files-assistant",
                prompt, lambda: _handle_pptx_create(topic, title),
            )
        elif intent == "linkedin_post":
            result = _handle_linkedin_post(params.get("topic", user_msg))
        else:
            result = _handle_general(user_msg)

        log("telegram", f"acao_{intent}", user_msg[:60])
        log_octogent("telegram", f"acao_{intent}", user_msg[:50])

    except Exception as e:
        result = f"❌ Erro: {str(e)[:300]}"
        log("telegram", "erro", str(e)[:150])
        log_octogent("telegram", "erro", str(e)[:100])

    await _reply(update, result, file_path)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start",     cmd_start))
    app.add_handler(CommandHandler("gmail",     cmd_gmail))
    app.add_handler(CommandHandler("agenda",    cmd_agenda))
    app.add_handler(CommandHandler("planilhas", cmd_planilhas))
    app.add_handler(CommandHandler("linkedin",  cmd_linkedin))
    app.add_handler(CommandHandler("pdf",       cmd_pdf))
    app.add_handler(CommandHandler("pptx",      cmd_pptx))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("=" * 55)
    print("   Telegram Bot Clilink — iniciado")
    print("=" * 55)
    print("  Pressione Ctrl+C para parar\n")
    log_octogent("telegram", "bot_iniciado", "polling ativo")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
