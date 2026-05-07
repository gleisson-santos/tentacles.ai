# Agent: architect

## Papel
Agente responsável por decisões de arquitetura no projeto Clilink.

## Quando acionar
- Adicionar nova integração de API
- Refatorar módulos existentes
- Escalar o sistema (múltiplos posts, múltiplas contas)
- Adicionar persistência (banco de dados, logs estruturados)

## Princípios de Arquitetura do Projeto

### Atual (script único)
```
auto_poster.py → todas as funções em um arquivo
```

### Evolução recomendada (quando necessário)
```
src/
  core/scheduler.py     → lógica do loop e intervalo
  api/groq_client.py    → integração Groq
  api/stability_client.py → integração Stability AI
  api/linkedin_client.py  → integração LinkedIn
  services/news_fetcher.py → busca de notícias RSS
  services/post_builder.py → construção do post
jobs/
  run_poster.py         → entry point para produção
logs/
  poster.log            → log estruturado de execuções
```

## Decisões Registradas
- **06/05/2026:** Migrado de Gemini para Groq (LLaMA 3.3 70B) — Gemini API inativa
- **06/05/2026:** Intervalo definido como 2 horas para produção
- **Arquitetura atual:** script único — adequado para o volume atual (1 post/2h)
