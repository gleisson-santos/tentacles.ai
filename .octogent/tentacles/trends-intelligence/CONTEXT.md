# Trends Intelligence

Monitoramento dinâmico de tendências globais e notícias em tempo real.

## Scope
Este agente monitora RSS feeds, Google News e outras fontes de tendências. Ele é altamente configurável: o usuário pode alterar os termos de busca e o intervalo de atualização diretamente pelo Dashboard ou editando o arquivo de configuração.

## Key Files
- `scripts/trends_monitor.py (Serviço Externo)` — script principal de execução
- `config/monitor_config.json` — arquivo de configuração dinâmica (termos e intervalo)

## Dynamic Configuration
Os termos de busca são lidos de `config/monitor_config.json`. Ao adicionar novos termos no Dashboard, este agente atualiza seu comportamento no próximo ciclo.

## Related Tentacles
- `linkedin-poster` — consome os dados de tendências para criar posts
- `orchestrator` — coordena a frequência de monitoramento
