
# Skill: project-context

## O que é
Resumo rápido do projeto para orientar Claude no início de qualquer sessão sem precisar reler código.

## Como usar
Leia este arquivo quando o usuário abrir uma nova sessão e perguntar sobre o projeto.

## Contexto do Projeto Clilink

**O que faz:** Posta automaticamente no LinkedIn a cada 2 horas usando Groq AI para gerar o texto e Stability AI para gerar a imagem.

**Arquivo principal:** `auto_poster.py`
- Função `fetch_news()` → busca RSS do Google News
- Função `analyze_and_write_groq()` → chama Groq (llama-3.3-70b-versatile)
- Função `generate_image()` → chama Stability AI
- Função `publish()` → publica no LinkedIn via OAuth2
- `INTERVAL_SECONDS = 7200` (2 horas)

**Para testar sem publicar:** `python test_groq.py`
**Para testar com publicação:** `python test_producao.py`
**Para rodar em produção:** `python auto_poster.py` (nova janela PowerShell)

**Dependências instaladas:** `feedparser`, `httpx`, `requests`, `groq`

**Token LinkedIn:** `~/.linkedin_mcp_token.json`

**Não existe:** banco de dados, framework web, Docker — é um script Python puro.
