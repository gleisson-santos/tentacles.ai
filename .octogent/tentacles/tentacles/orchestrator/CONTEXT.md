# Orchestrator — CONTEXT

## Scope
Agente coordenador central do Clilink. Monitora o canal `clilink-events` no Octogent, delega tarefas para os tentáculos corretos e mantém visão geral do estado do sistema. Corresponde ao skill `proactive-agent.md`.

## Key Files
- `.claude/skills/proactive-agent.md` — comportamento do orquestrador
- `logs/activity.log` — registro de todas as ações de todos os agentes
- `logs/logger.py` — funções `log()` e `log_octogent()` compartilhadas

## Canal Octogent
- **Nome:** `clilink-events`
- **Monitora eventos de:** linkedin-poster, google-assistant, files-assistant, telegram-bot
- **Formato dos eventos:** `[AGENTE] acao | detalhe`

## Mapa de delegação
| Pedido recebido | Delega para | Via |
|----------------|-------------|-----|
| emails / gmail / inbox | google-assistant | gmail_tools |
| agenda / evento / calendário | google-assistant | calendar_tools |
| planilha / sheets / tabela | google-assistant | sheets_tools |
| post LinkedIn / publicar | linkedin-poster | auto_poster.py |
| PDF / contrato / currículo | files-assistant | pdf_tools |
| apresentação / slides | files-assistant | pptx_tools |
| Telegram mensagem | telegram-bot | handle_message() |

## Key Decisions
- Nunca executa ações irreversíveis sem confirmar com o usuário
- Sempre mostra preview antes de criar/enviar/deletar
- Erros em um agente não bloqueiam os outros
- Todas as ações registradas em `logs/activity.log`

## Related Tentacles
- Todos os outros tentáculos reportam para este via canal clilink-events
