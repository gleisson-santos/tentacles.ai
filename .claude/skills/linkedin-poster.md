# Skill: Linkedin Poster

## Papel
Postagem automática no LinkedIn

## Quando acionar
- Quando o usuário pedir algo relacionado a linkedin poster
- Delegado pelo orchestrator

## Comportamento
1. Leia `.octogent/tentacles/linkedin-poster/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("linkedin-poster", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
