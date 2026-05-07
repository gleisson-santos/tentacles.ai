# Linkedin Poster

## Scope
Automação completa de postagem no LinkedIn: busca notícias no Google News, analisa com Groq AI (LLaMA 3.3 70B), gera imagem minimalista com Stability AI e publica a cada 2 horas.

## Key Files
- `auto_poster.py` — loop principal (fetch → write → image → publish)
- `linkedin_mcp_server.py` — servidor MCP com ferramentas LinkedIn para Claude Code
- `test_groq.py` — teste local sem publicar
- `test_producao.py` — teste com publicação real
- `~/.linkedin_mcp_token.json` — token OAuth2 LinkedIn

## Key Decisions
- Groq AI como primário, template como fallback se API cair
- Stability AI `v2beta/stable-image/generate/core` para imagens 1:1
- Intervalo de 2h (7200s) para respeitar rate limits do LinkedIn
- 10 tópicos monitorados em rotação (n8n, Claude, ChatGPT, Gemini, Power BI, etc.)
- Paleta de cores por tópico para identidade visual consistente

## Conventions
- Posts: 150–250 palavras, gancho na 1ª linha, emojis nos tópicos, CTA no final
- Imagens: fundo branco, máximo 2 cores, sem texto, sem faces
- JSON retornado pelo Groq: `{topic, title, post, image_concept}`
- Log de cada publicação em `logs/activity.log` + canal Octogent

## MCP Tools disponíveis (linkedin-poster)
- `authenticate` — fluxo OAuth2
- `check_auth_status` — valida token
- `create_post` — posta texto
- `create_post_with_image` — posta com imagem
- `generate_image` — gera via Stability AI
- `fetch_url_content` — lê URLs

## Related Tentacles
- `orchestrator` — recebe pedidos de post manual
- `telegram-bot` — pode acionar post via comando /linkedin
