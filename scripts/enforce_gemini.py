import json
import os
from pathlib import Path

def enforce_gemini():
    home = Path.home()
    octogent_dir = home / ".octogent"
    
    if not octogent_dir.exists():
        print("[-] Pasta .octogent não encontrada.")
        return

    print(f"[*] Escaneando projetos em {octogent_dir}...")
    
    # Busca todos os arquivos tentacles.json nos subprojetos
    for registry_path in octogent_dir.glob("projects/*/state/tentacles.json"):
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            changed = False
            
            # 1. Força o provedor preferido nas Settings para Gemini
            ui_state = data.get("uiState", {})
            if ui_state.get("preferredAgentProvider") != "gemini-cli":
                ui_state["preferredAgentProvider"] = "gemini-cli"
                changed = True
                print(f"[+] Setting atualizada para Gemini em: {registry_path.parent.parent.name}")

            # 2. LIMPEZA DE PRIMAVERA: Remove terminais antigos para começar do zero
            if "terminals" in data and len(data["terminals"]) > 0:
                # Mantemos apenas terminais que NÃO são tarefas temporárias (opcional)
                # Aqui vamos limpar TUDO para garantir o "Fresh Start" que você quer
                data["terminals"] = []
                changed = True
                print(f"[CLEANUP] Canvas limpo em: {registry_path.parent.parent.name}")

            if changed:
                with open(registry_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"[OK] {registry_path} atualizado com sucesso.")
                
        except Exception as e:
            print(f"[!] Erro ao processar {registry_path}: {e}")

if __name__ == "__main__":
    enforce_gemini()
