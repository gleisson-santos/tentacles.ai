# Command: init

## O que faz
Garante que o projeto está corretamente inicializado com memória persistente e estrutura de agentes.

## Quando usar
- Início de nova sessão após fechar o terminal
- Após clonar o repositório em nova máquina
- Quando a estrutura `.claude/` parecer incompleta

## Checklist de Inicialização

```
[ ] CLAUDE.md existe e está atualizado
[ ] .claude/skills/project-context.md existe
[ ] .claude/skills/bootstrap-project.md existe
[ ] .claude/rules/efficiency.md existe
[ ] .claude/agents/architect.md existe
[ ] .claude/commands/init.md existe
[ ] auto_poster.py usa Groq (não Gemini)
[ ] INTERVAL_SECONDS = 7200
[ ] Token LinkedIn presente em ~/.linkedin_mcp_token.json
```

## Como executar

Cole no Claude:
```
Leia o CLAUDE.md e me diga o estado atual do projeto Clilink.
```

Claude deve responder com o estado atual sem fazer scan do repositório.

## Para rodar o sistema
```powershell
# Nova janela PowerShell dedicada:
cd C:\Users\t034183\Desktop\Clilink
python auto_poster.py

# Testar sem publicar:
python test_groq.py

# Testar com publicação real:
python test_producao.py
```
