# Platform Infra — Backlog

## Segurança / Credenciais
- **Corrigir `.gitignore`** — adicionar `mcp_servers/google_mcp/credentials/token.json`, `mcp_servers/google_mcp/credentials/client_secret.json` e `~/.linkedin_mcp_token.json` para evitar commit acidental de tokens OAuth2. Hoje o `.gitignore` só lista `.octogent/`.

## Launcher
- **Tornar `start_clilink.ps1` portável** — substituir caminhos hardcoded de Python e diretório por detecção automática (`Get-Command python` + `$PSScriptRoot`), permitindo rodar em outra máquina sem edição manual.

## Expansão src/
- **Extrair clientes de API de `auto_poster.py` para `src/api/`** — criar `groq_client.py`, `stability_client.py` e `linkedin_client.py` reutilizáveis para que outros agentes (Telegram Bot, por exemplo) possam importá-los sem duplicar lógica.

## Jobs
- **Criar `jobs/run_poster.py`** — entry point de produção separado conforme planejado em `.claude/agents/architect.md`, com tratamento de erro, logging estruturado e suporte a execução via agendador externo (Task Scheduler do Windows ou similar).
