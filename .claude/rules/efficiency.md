# Rules: efficiency

## Regras de Eficiência de Tokens

### OBRIGATÓRIO ao iniciar qualquer sessão
1. Leia `CLAUDE.md` primeiro — contém todo o contexto do projeto
2. NÃO faça scan completo do repositório (`ls -r`, `Get-ChildItem -Recurse` sem filtro)
3. Use `Glob` com padrão específico ou `Grep` pontual para encontrar o que precisa

### Ao editar código
- Leia APENAS o arquivo relevante, não o projeto inteiro
- Prefira `Edit` (diff) a `Write` (reescrita completa)
- Se precisar entender uma função, leia só a seção relevante com `offset` + `limit`

### Ao criar arquivos
- Verifique se já existe com `Glob` antes de criar
- Nunca crie documentação não solicitada (README, changelog, etc.)
- Não adicione comentários desnecessários no código

### Ao debugar
- Leia o traceback completo antes de ler código
- Procure o símbolo exato com `Grep` em vez de ler o arquivo inteiro
- Teste a hipótese mais simples primeiro

### Proibido
- Ler múltiplos arquivos grandes sem necessidade
- Reescrever arquivos que só precisam de edição pontual
- Criar arquivos intermediários de análise ou planejamento
- Repetir contexto já presente no CLAUDE.md
