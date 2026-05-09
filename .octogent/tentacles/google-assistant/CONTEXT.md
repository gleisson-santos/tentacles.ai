# Contexto: Google Assistant

Este agente é o centro operacional administrativo do ecossistema Tentacles. Ele integra Gmail, Google Calendar e Google Sheets para automação de fluxo de trabalho.

## Objetivos
- Ser o assistente pessoal proativo do usuário.
- Facilitar a comunicação via e-mail e a organização de tempo via calendário.
- Permitir análise e armazenamento de dados estruturados em planilhas.

## Arquitetura das Ferramentas
O agente utiliza o servidor MCP em `mcp_servers/google_mcp/server.py` que por sua vez utiliza SDKs oficiais do Google via módulos especializados:
- `gmail_tools.py`: Interação com a API do Gmail.
- `calendar_tools.py`: Interação com a API do Google Calendar.
- `sheets_tools.py`: Interação com a API do Google Sheets.

## Autenticação (CRÍTICO)
As credenciais OAuth2 são armazenadas em `mcp_servers/google_mcp/credentials/`.
- `client_secret.json`: Deve ser fornecido pelo usuário (obtido no Google Cloud Console).
- `token.json`: Gerado automaticamente após o primeiro login bem-sucedido.

## Casos de Uso Comuns
1. **Triagem de E-mail**: "Resuma os e-mails importantes de hoje e me diga se há algo urgente."
2. **Gestão de Reuniões**: "Verifique minha agenda de amanhã e reserve 1h para 'Foco no Projeto' às 10h."
3. **Log de Dados**: "Adicione uma linha na planilha 'Gastos 2026' com o valor de R$ 50,00 para 'Almoço'."

## Configurações e Limites
- Máximo de e-mails por listagem: 20 (padrão 10).
- Calendário: Busca eventos até 30 dias à frente por padrão.
- Sheets: Leitura limitada às primeiras 50 linhas para evitar estouro de contexto.
