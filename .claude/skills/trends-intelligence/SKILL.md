---
name: trends-intelligence
description: Habilidade de trends-intelligence integrada ao ecossistema Tentacles.
---

# Skill: Trends Intelligence

## Papel
Monitoramento contínuo de tendências e notícias via RSS/Google News.

## Quando acionar
- Quando o usuário pedir algo relacionado a trends intelligence
- Delegado pelo orchestrator

## Comportamento
1. Leia `.octogent/tentacles/trends-intelligence/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("trends-intelligence", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
