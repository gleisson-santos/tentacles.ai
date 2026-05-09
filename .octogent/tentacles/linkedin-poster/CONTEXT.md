# LinkedIn Poster

## Scope
Automação completa de postagens no LinkedIn com IA de texto (Groq/OpenRouter) e imagem (Stability AI). Suporta posts com texto puro e posts com imagem gerada.

## Key Files
- `mcp_servers/linkedin_mcp/server.py` — **MCP principal** (usar este, não linkedin-poster/)
- `auto_poster.py` — Loop autônomo de postagem a cada 2h
- `~/.linkedin_mcp_token.json` — Token OAuth2 (não commitar)

## Ferramentas MCP Disponíveis
- `authenticate()` — OAuth2 LinkedIn (abre browser, salva token)
- `check_auth_status()` — Verifica se token está válido
- `fetch_url_content(url)` — Scraping de artigo para inspiração
- `generate_image(prompt)` — Imagem via Stability AI Core
- `create_post(text, visibility)` — Publica post de texto
- `create_post_with_image(text, image_path)` — Publica post com imagem

## Variáveis de Ambiente Necessárias
```
LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...
LINKEDIN_REDIRECT_URI=http://localhost:3000/callback
STABILITY_API_KEY=sk-...
```

## Fluxo de Autenticação
1. Configurar variáveis no `.env`
2. Abrir tentáculo no Dashboard e rodar `authenticate()`
3. Browser abre → autorizar → token salvo em `~/.linkedin_mcp_token.json`
4. Verificar com `check_auth_status()`

## Integração com Orchestrator
Quando delegado pelo Orchestrator via Telegram, o agente deve:
1. Receber o tema/conteúdo via prompt
2. Opcionalmente buscar notícias com `fetch_url_content()`
3. Gerar imagem com `generate_image()`
4. Publicar com `create_post_with_image()`
5. Gravar `OK|Post publicado: [TEMA]` em `outputs/.status/{task_id}.done`

## Key Decisions
- Token LinkedIn armazenado em `~/.linkedin_mcp_token.json` (fora do repo)
- Stability AI Core escolhido por custo ($0.03/img) vs qualidade
- `auto_poster.py` opera independente do Dashboard (pode rodar em background)

## Related Tentacles
- `orchestrator` — coordenador (delega pedidos de post do Telegram)
- `trends-intelligence` — fornece temas para postagens automáticas
