"""
Sincroniza o CLAUDE.md com os tentáculos existentes em .octogent/tentacles/.
Executado automaticamente via hook PostToolUse sempre que um arquivo for escrito.
Também pode ser rodado manualmente: python scripts/sync_tentacles.py
"""
import re
from pathlib import Path

ROOT       = Path(__file__).parent.parent
TENTACLES  = ROOT / ".octogent" / "tentacles"
CLAUDE_MD  = ROOT / "CLAUDE.md"


def _parse_context(context_path: Path) -> dict:
    text = context_path.read_text(encoding="utf-8")

    # Extrai primeira frase do ## Scope como responsabilidade
    scope_match = re.search(r"## Scope\s*\n(.+)", text)
    responsibility = scope_match.group(1).strip() if scope_match else "—"
    if len(responsibility) > 60:
        responsibility = responsibility[:57] + "..."

    # Extrai primeiro arquivo de ## Key Files (primeira linha de bullet)
    files_match = re.search(r"## Key Files\s*\n- `([^`]+)`", text)
    main_file = f"`{files_match.group(1)}`" if files_match else "—"

    return {"responsibility": responsibility, "main_file": main_file}


def _build_table(tentacles: list[dict]) -> str:
    header = (
        "| Agente | Arquivo Principal | Responsabilidade |\n"
        "|--------|-------------------|------------------|\n"
    )
    rows = ""
    for t in tentacles:
        rows += f"| {t['name']} | {t['main_file']} | {t['responsibility']} |\n"
    return header + rows


def sync():
    if not TENTACLES.exists():
        return

    tentacle_dirs = sorted([d for d in TENTACLES.iterdir() if d.is_dir()])
    if not tentacle_dirs:
        return

    tentacles = []
    for d in tentacle_dirs:
        ctx = d / "CONTEXT.md"
        if not ctx.exists():
            continue
        info = _parse_context(ctx)
        tentacles.append({"name": d.name, **info})

    new_table = _build_table(tentacles)

    claude_text = CLAUDE_MD.read_text(encoding="utf-8")

    # Remove TODAS as ocorrências de "## Mapa de Agentes" e reconstrói uma só
    # Padrão: heading + linha em branco opcional + tabela (linhas com |)
    pattern = r"## Mapa de Agentes[^\n]*\n(\n)?(\|[^\n]*\n)+"
    new_block = f"## Mapa de Agentes (Tentáculos Octogent)\n\n{new_table}"

    occurrences = list(re.finditer(pattern, claude_text))
    if occurrences:
        # Remove todas as ocorrências e insere uma só no lugar da primeira
        first_start = occurrences[0].start()
        # Remove todas da última para a primeira (para não deslocar índices)
        updated = claude_text
        for m in reversed(occurrences):
            updated = updated[:m.start()] + updated[m.end():]
        # Insere o bloco novo na posição original da primeira ocorrência
        updated = updated[:first_start] + new_block + "\n\n" + updated[first_start:]
    else:
        # Seção não existe ainda — adiciona antes de "## Credenciais"
        updated = claude_text.replace(
            "## Credenciais",
            f"{new_block}\n\n## Credenciais",
        )

    if updated != claude_text:
        CLAUDE_MD.write_text(updated, encoding="utf-8")
        print(f"  CLAUDE.md atualizado — {len(tentacles)} tentáculos sincronizados.")
    else:
        print(f"  CLAUDE.md já está em dia — {len(tentacles)} tentáculos.")


if __name__ == "__main__":
    sync()
