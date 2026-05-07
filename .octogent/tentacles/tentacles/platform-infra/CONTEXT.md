# Platform Infra

Infraestrutura de plataforma: startup do sistema, expansão src/ e jobs agendados.

## Scope
- `start_clilink.ps1` — script launcher que sobe todos os agentes em paralelo
- `src/core/` — módulos de domínio compartilhado (hoje vazio, expansão futura)
- `src/api/` — clientes de API reutilizáveis (hoje vazio, expansão futura)
- `src/services/` — serviços de negócio (hoje vazio, expansão futura)
- `jobs/` — scripts agendados fora do loop principal (hoje vazio)
- `.gitignore` — regras de proteção de segredos

## Key Decisions

### Startup via `start_clilink.ps1`
- Abre 3 janelas PowerShell separadas: LinkedIn Auto-Poster, Octogent Dashboard e Telegram Bot
- Python hardcoded em `C:\Users\t034183\AppData\Local\Python\pythoncore-3.14-64\python.exe`
- Telegram Bot só sobe se `$env:TELEGRAM_BOT_TOKEN` estiver definido e diferente de `"SEU_TOKEN_AQUI"`
- Dashboard disponível em `http://localhost:8787` após inicialização
- Sleep de 2–3s entre processos para evitar race condition na inicialização do Octogent

### Arquitetura de expansão (documentada em `.claude/agents/architect.md`)
- **Decisão de 06/05/2026:** manter script único enquanto volume for 1 post/2h
- Evolução planejada quando necessário:
  - `src/core/scheduler.py` — lógica de loop e intervalo
  - `src/api/groq_client.py`, `stability_client.py`, `linkedin_client.py` — clientes de API
  - `src/services/news_fetcher.py`, `post_builder.py` — serviços de negócio
  - `jobs/run_poster.py` — entry point de produção separado

### `.gitignore`
- Atualmente só ignora `.octogent/` — **os segredos OAuth2 em `mcp_servers/google_mcp/credentials/` NÃO estão listados explicitamente** (risco de commit acidental)

## Conventions
- Novos módulos em `src/` devem ser importados pelos agentes existentes, não substituí-los diretamente
- Entry points de produção ficam em `jobs/`, não em `src/`
- O launcher `start_clilink.ps1` deve ser atualizado sempre que um novo agente for adicionado ao sistema

## Related Tentacles
- `orchestrator` — beneficiário principal do sistema de startup
- `linkedin-poster`, `telegram-bot` — processos iniciados por este launcher
