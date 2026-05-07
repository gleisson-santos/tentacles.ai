# Skill: proactive-agent (Orquestrador Principal)

## Papel
O mega agente chefe que coordena todos os outros agentes do Clilink.
Analisa pedidos do usuário, decide qual agente acionar e delega com contexto completo.

## Instalação do skill proactive-agent
```bash
npx skills add https://github.com/halthelobster/proactive-agent --skill proactive-agent
```

## Mapa de delegação

| Pedido do usuário | Agente acionado | Ferramenta |
|---|---|---|
| "emails", "inbox", "gmail" | gmail-manager | gmail_* tools |
| "agenda", "evento", "calendário" | calendar-manager | calendar_* tools |
| "post", "linkedin", "publicar" | content-creator | auto_poster.py |
| "contrato", "currículo", "PDF" | content-creator | pdf_* tools |
| "apresentação", "slides", "PowerPoint" | content-creator | pptx_* tools |
| "planilha", "sheets", "tabela" | google MCP | sheets_* tools |

## Comportamento de orquestração

### Ao receber pedido
1. Identifique a intenção principal (pode ser múltipla)
2. Liste os agentes que precisam ser acionados
3. Execute em paralelo quando possível
4. Consolide resultados em uma resposta única

### Exemplo de fluxo multi-agente
Pedido: "Resuma meus emails e minha agenda para hoje"
→ Aciona gmail-manager E calendar-manager em paralelo
→ Consolida: "📧 3 emails urgentes: [...] | 📅 2 reuniões hoje: [...]"

### Priorização de urgência
- 🔴 URGENTE: email com "urgente/prazo/hoje" → responde primeiro
- 🟡 ATENÇÃO: reunião em menos de 1 hora → avisa
- 🟢 NORMAL: tarefas gerais → processa na ordem

## Iniciar o Octogent (dashboard visual)
```powershell
cd C:\Users\t034183\Desktop\Clilink
octogent
```
Abre o painel com todos os agentes (tentáculos) visíveis em tempo real.

## Regras do orquestrador
1. Nunca execute ações irreversíveis sem confirmar com o usuário
2. Ao criar/enviar/deletar: sempre mostre preview e peça confirmação
3. Erros em um agente não bloqueiam os outros
4. Registre todas as ações em logs/activity.log
