# Skill: Telegram Bot

## Papel
Interface de comando via Telegram com detecção de intenção.

## Quando acionar
- Quando o usuário pedir algo relacionado a telegram bot
- Delegado pelo orchestrator

## Comportamento
1. Leia `.octogent/tentacles/telegram-bot/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("telegram-bot", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
