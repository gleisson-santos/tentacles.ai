
# Skill: bootstrap-project

## Propósito
Skill reutilizável para inicializar qualquer novo projeto com estrutura de memória persistente, regras de eficiência e arquitetura modular de agentes. Use este prompt no início de qualquer novo projeto.

---

## Prompt para usar em novos projetos

Cole o texto abaixo ao iniciar um projeto novo:

```
Initialize this repository using a structured AI-agent architecture AND persist this behavior as a reusable skill.

GOAL: Create a scalable, token-efficient project structure with persistent memory and modular agent capabilities.

STEP 1 — CLAUDE.md
- Se não existir: crie com nome do projeto, objetivo, tech stack, estrutura de pastas, regras, estado atual e próximos passos
- Se existir: atualize sem sobrescrever dados importantes

STEP 2 — AGENT STRUCTURE
Crie (se não existir):
.claude/skills/
.claude/rules/
.claude/agents/
.claude/commands/

STEP 3 — BASE FILES
Crie com conteúdo mínimo funcional:
.claude/skills/project-context.md
.claude/skills/bootstrap-project.md
.claude/rules/efficiency.md
.claude/agents/architect.md
.claude/commands/init.md

STEP 4 — CODEBASE STRUCTURE
Se não existir estrutura, crie:
src/core/  src/api/  src/services/  jobs/  logs/

STEP 5 — BEHAVIOR ENFORCEMENT
- NUNCA scan completo do repositório
- SEMPRE leia CLAUDE.md primeiro
- Prefira editar existentes a criar novos
- Minimize uso de tokens

STEP 6 — FINALIZATION
Liste tudo que foi criado/validado e pergunte que tipo de projeto é este.
```

---

## Regras que este skill aplica
1. Leia CLAUDE.md antes de qualquer ação
2. Use Glob/Grep pontual em vez de scan completo
3. Nunca recrie arquivos que já existem com conteúdo válido
4. Documente o estado atual sempre que fizer alterações significativas
