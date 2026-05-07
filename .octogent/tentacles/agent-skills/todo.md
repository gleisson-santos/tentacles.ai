# Agent Skills — Backlog

## Segurança de configuração
- **Mover `LINKEDIN_CLIENT_SECRET` para variável de ambiente** — hoje a chave secreta do LinkedIn OAuth2 está em texto plano dentro de `settings.local.json` no campo `env` do MCP `linkedin-poster`. Mover para `$env:LINKEDIN_CLIENT_SECRET` e referenciar via variável no settings para evitar exposição acidental.

## Skills faltantes
- **Criar `sheets-manager.md`** — a skill de Google Sheets não existe ainda; apenas `gmail-manager.md` e `calendar-manager.md` estão criadas. Criar skill com comportamento para listagem, leitura, escrita e criação de planilhas, espelhando o padrão das outras skills Google.

## Atualização de skills existentes
- **Atualizar `content-creator.md` com ferramentas MCP reais** — a skill lista nomes de funções como `pdf_create()` mas não documenta os parâmetros completos (como `sections_json`, `slides_json` com tipos `title|content|section|closing`). Sincronizar com o `CONTEXT.md` do `files-assistant` que tem a documentação completa.

## Checklist de inicialização
- **Expandir `commands/init.md`** — o checklist atual cobre só o LinkedIn Poster. Adicionar verificações para: Google OAuth2 token presente, Telegram Bot token configurado, MCP Servers respondendo, `outputs/pdfs/` e `outputs/presentations/` existindo.
