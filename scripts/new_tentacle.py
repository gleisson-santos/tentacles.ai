"""
Cria um novo tentáculo no Clilink com tudo configurado automaticamente:
  - .octogent/tentacles/<nome>/ com CONTEXT.md + todo.md
  - .claude/skills/<nome>.md com comportamento skeleton
  - mcp_servers/<nome>/server.py + __init__.py (se --mcp)
  - Registra MCP em .claude/settings.local.json (se --mcp)
  - Adiciona card visual no deck.json do Octogent (cor + octopus)
  - Atualiza CLAUDE.md via sync_tentacles.py

Uso:
  python scripts/new_tentacle.py <nome> "<descricao>" [--mcp] [--color #RRGGBB]

Exemplos:
  python scripts/new_tentacle.py whatsapp-bot "Bot WhatsApp com respostas automaticas"
  python scripts/new_tentacle.py analytics "Relatorios de performance" --mcp --color #ff6d00
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

PYTHON_EXE = (
    "C:\\Users\\t034183\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe"
)

# Localização do deck.json (Detecta local ou global)
def get_deck_json():
    # 1. Prioridade: Local no Workspace
    local_deck = ROOT / ".octogent" / "state" / "deck.json"
    if local_deck.exists():
        return local_deck
    
    # 2. Fallback: Global (UUID fixo do projeto)
    global_deck = (
        Path.home()
        / ".octogent"
        / "projects"
        / "6db28e03-c46a-44da-8f55-7236cda76706"
        / "state"
        / "deck.json"
    )
    return global_deck

DECK_JSON = get_deck_json()

# Paleta de cores padrão em rotação para novos tentáculos
_DEFAULT_COLORS = [
    "#6c63ff", "#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff",
    "#ff6d00", "#2ca5e0", "#e040fb", "#00b894", "#fdcb6e",
]
_ANIMATIONS = ["sway", "swim-up", "sway", "swim-up"]
_EXPRESSIONS = ["happy", "surprised", "happy", "happy"]
_ACCESSORIES = ["none", "none", "mohawk", "none"]


# ── Templates ──────────────────────────────────────────────────────────────────

def _context_md(name: str, description: str, has_mcp: bool) -> str:
    mcp_section = ""
    if has_mcp:
        mcp_section = f"""
## MCP Server
- `mcp_servers/{name}/server.py` — servidor MCP FastMCP
- Registrado em `.claude/settings.local.json` como `{name}`

## Ferramentas MCP disponíveis
- `{name}_action(param)` — ação principal (personalizar)
"""
    return f"""# {name.replace("-", " ").title()}

## Scope
{description}

## Key Files
- `mcp_servers/{name}/server.py` — servidor MCP (se aplicável)
- `scripts/new_tentacle.py` — como este tentáculo foi criado
{mcp_section}
## Key Decisions
- TODO: documentar decisões de arquitetura

## Conventions
- TODO: documentar convenções deste agente

## Related Tentacles
- `orchestrator` — coordenador principal
"""


def _todo_md(name: str, description: str) -> str:
    return f"""# {name.replace("-", " ").title()} — Todo

## Backlog
- [ ] Definir ferramentas e responsabilidades deste agente
- [ ] Implementar lógica principal
- [ ] Integrar com orchestrator via canal clilink-events
- [ ] Adicionar testes
- [ ] Documentar no CONTEXT.md

## Concluído
- [x] Tentáculo criado via new_tentacle.py
- [x] Skill skeleton criada em .claude/skills/{name}.md
"""


def _skill_md(name: str, description: str, has_mcp: bool) -> str:
    tools_section = ""
    if has_mcp:
        tools_section = f"""
## Ferramentas disponíveis
- `{name}_action(param)` — ação principal (personalizar em `mcp_servers/{name}/server.py`)
"""
    return f"""# Skill: {name.replace("-", " ").title()}

## Papel
{description}

## Quando acionar
- Quando o usuário pedir algo relacionado a {name.replace("-", " ")}
- Delegado pelo orchestrator
{tools_section}
## Comportamento
1. Leia `.octogent/tentacles/{name}/CONTEXT.md` para contexto completo
2. Execute a tarefa solicitada
3. Registre a ação via `log_octogent("{name}", "acao", "detalhe")`
4. Retorne resultado claro ao usuário

## Regras
- Sempre confirmar antes de ações irreversíveis
- Registrar tudo em `logs/activity.log`
- Reportar erros detalhados para o orchestrator
"""


def _mcp_server_py(name: str, description: str) -> str:
    func_name = name.replace("-", "_")
    return f'''"""
{name.replace("-", " ").title()} MCP Server
{description}

Rode com: python mcp_servers/{name}/server.py
"""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__file__))))

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("{name}")


@mcp.tool()
def {func_name}_action(param: str) -> str:
    """Ação principal do agente {name}. Personalize conforme necessário."""
    # TODO: implementar lógica real
    return f"[{name}] Executado com: {{param}}"


@mcp.tool()
def {func_name}_status() -> str:
    """Retorna o status atual do agente {name}."""
    return f"[{name}] Agente ativo e operacional."


if __name__ == "__main__":
    mcp.run()
'''


# ── Deck visual ───────────────────────────────────────────────────────────────

def _add_to_deck(name: str, color: str, paths: list):
    """Adiciona o tentáculo ao deck.json para aparecer no Octogent Dashboard."""
    if not DECK_JSON.exists():
        return
    deck = json.loads(DECK_JSON.read_text(encoding="utf-8"))
    deck.setdefault("tentacles", {})

    # Escolhe variação visual baseada no índice do tentáculo
    idx = len(deck["tentacles"])
    deck["tentacles"][name] = {
        "color": color,
        "status": "idle",
        "octopus": {
            "animation": _ANIMATIONS[idx % len(_ANIMATIONS)],
            "expression": _EXPRESSIONS[idx % len(_EXPRESSIONS)],
            "accessory": _ACCESSORIES[idx % len(_ACCESSORIES)],
            "hairColor": color,
        },
        "scope": {"paths": paths, "tags": []},
        "label": name.replace("-", " ").title()
    }
    DECK_JSON.write_text(json.dumps(deck, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  [OK] Card visual adicionado ao Octogent Deck ({color})")


# ── Criação ────────────────────────────────────────────────────────────────────

def create_tentacle(name: str, description: str, has_mcp: bool, color: str = ""):
    name = name.lower().replace(" ", "-")

    # Escolhe cor automaticamente se não informada
    if not color:
        deck = json.loads(DECK_JSON.read_text(encoding="utf-8")) if DECK_JSON.exists() else {"tentacles": {}}
        idx = len(deck.get("tentacles", {}))
        color = _DEFAULT_COLORS[idx % len(_DEFAULT_COLORS)]

    print(f"\n  Criando tentaculo: {name}")
    print(f"  Descricao: {description}")
    print(f"  Cor: {color} | MCP: {'sim' if has_mcp else 'nao'}\n")

    # 1. Pasta do tentáculo
    tentacle_dir = ROOT / ".octogent" / "tentacles" / name
    tentacle_dir.mkdir(parents=True, exist_ok=True)
    (tentacle_dir / "CONTEXT.md").write_text(_context_md(name, description, has_mcp), encoding="utf-8")
    (tentacle_dir / "todo.md").write_text(_todo_md(name, description), encoding="utf-8")
    print(f"  [OK] .octogent/tentacles/{name}/ criado")

    # 2. Skill
    skills_dir = ROOT / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    (skills_dir / f"{name}.md").write_text(_skill_md(name, description, has_mcp), encoding="utf-8")
    print(f"  [OK] .claude/skills/{name}.md criado")

    # 3. MCP Server (opcional)
    if has_mcp:
        mcp_dir = ROOT / "mcp_servers" / name
        mcp_dir.mkdir(parents=True, exist_ok=True)
        (mcp_dir / "__init__.py").write_text("", encoding="utf-8")
        (mcp_dir / "server.py").write_text(_mcp_server_py(name, description), encoding="utf-8")
        print(f"  [OK] mcp_servers/{name}/server.py criado")

        # 4. Registrar no settings.local.json
        settings_path = ROOT / ".claude" / "settings.local.json"
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        settings.setdefault("mcpServers", {})[name] = {
            "type": "stdio",
            "command": PYTHON_EXE,
            "args": [str(ROOT / "mcp_servers" / name / "server.py")],
            "env": {},
        }
        settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  [OK] MCP '{name}' registrado em settings.local.json")

    # 5. Deck visual (sempre, com ou sem MCP)
    mcp_path = [f"mcp_servers/{name}"] if has_mcp else []
    _add_to_deck(name, color, mcp_path)

    # 6. Sync CLAUDE.md
    import importlib.util, sys as _sys
    _spec = importlib.util.spec_from_file_location("sync_tentacles", ROOT / "scripts" / "sync_tentacles.py")
    _mod  = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    _mod.sync()
    print(f"\n  Tentaculo '{name}' pronto! Reinicie o Claude Code para ativar o MCP.")


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    _name        = sys.argv[1]
    _description = sys.argv[2]
    _has_mcp     = "--mcp" in sys.argv

    _color = ""
    for i, arg in enumerate(sys.argv):
        if arg == "--color" and i + 1 < len(sys.argv):
            _color = sys.argv[i + 1]

    create_tentacle(_name, _description, _has_mcp, _color)
