import subprocess
import json
import os

commands = [
    {
        "terminal-id": "files-assistant-swarm-0",
        "variables": {
            "tentacleName": "Files Assistant",
            "tentacleId": "files-assistant",
            "tentacleContextPath": r"C:\Users\t034183\Desktop\tentacles\.octogent\tentacles\files-assistant",
            "todoItemText": "Definir ferramentas e responsabilidades deste agente",
            "terminalId": "files-assistant-swarm-0",
            "apiPort": "8787",
            "workspaceContextIntro": "You are working on an isolated worktree branch, not the main branch.",
            "workspaceGuidelines": "- You are working in an isolated git worktree on branch `octogent/files-assistant-swarm-0`. Make changes freely without worrying about conflicts with other agents.",
            "commitGuidance": "- Commit your changes with a clear commit message describing what you did.",
            "definitionOfDoneCommitStep": "Changes are committed with a descriptive message.",
            "workspaceReminder": "Commit.",
            "parentTerminalId": "files-assistant-swarm-parent",
            "parentSection": "## Communication\n\nYour parent coordinator is at terminal `files-assistant-swarm-parent`.\nWhen you complete your task, report back:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"DONE: Definir ferramentas e responsabilidades deste agente\" --from files-assistant-swarm-0\n```\nIf you are blocked, ask for help:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"BLOCKED: <describe what you need>\" --from files-assistant-swarm-0\n```"
        },
        "context": "Definir ferramentas e responsabilidades deste agente"
    },
    {
        "terminal-id": "files-assistant-swarm-1",
        "variables": {
            "tentacleName": "Files Assistant",
            "tentacleId": "files-assistant",
            "tentacleContextPath": r"C:\Users\t034183\Desktop\tentacles\.octogent\tentacles\files-assistant",
            "todoItemText": "Implementar lógica principal",
            "terminalId": "files-assistant-swarm-1",
            "apiPort": "8787",
            "workspaceContextIntro": "You are working on an isolated worktree branch, not the main branch.",
            "workspaceGuidelines": "- You are working in an isolated git worktree on branch `octogent/files-assistant-swarm-1`. Make changes freely without worrying about conflicts with other agents.",
            "commitGuidance": "- Commit your changes with a clear commit message describing what you did.",
            "definitionOfDoneCommitStep": "Changes are committed with a descriptive message.",
            "workspaceReminder": "Commit.",
            "parentTerminalId": "files-assistant-swarm-parent",
            "parentSection": "## Communication\n\nYour parent coordinator is at terminal `files-assistant-swarm-parent`.\nWhen you complete your task, report back:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"DONE: Implementar lógica principal\" --from files-assistant-swarm-1\n```\nIf you are blocked, ask for help:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"BLOCKED: <describe what you need>\" --from files-assistant-swarm-1\n```"
        },
        "context": "Implementar lógica principal"
    },
    {
        "terminal-id": "files-assistant-swarm-2",
        "variables": {
            "tentacleName": "Files Assistant",
            "tentacleId": "files-assistant",
            "tentacleContextPath": r"C:\Users\t034183\Desktop\tentacles\.octogent\tentacles\files-assistant",
            "todoItemText": "Integrar com orchestrator via canal clilink-events",
            "terminalId": "files-assistant-swarm-2",
            "apiPort": "8787",
            "workspaceContextIntro": "You are working on an isolated worktree branch, not the main branch.",
            "workspaceGuidelines": "- You are working in an isolated git worktree on branch `octogent/files-assistant-swarm-2`. Make changes freely without worrying about conflicts with other agents.",
            "commitGuidance": "- Commit your changes with a clear commit message describing what you did.",
            "definitionOfDoneCommitStep": "Changes are committed with a descriptive message.",
            "workspaceReminder": "Commit.",
            "parentTerminalId": "files-assistant-swarm-parent",
            "parentSection": "## Communication\n\nYour parent coordinator is at terminal `files-assistant-swarm-parent`.\nWhen you complete your task, report back:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"DONE: Integrar com orchestrator via canal clilink-events\" --from files-assistant-swarm-2\n```\nIf you are blocked, ask for help:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"BLOCKED: <describe what you need>\" --from files-assistant-swarm-2\n```"
        },
        "context": "Integrar com orchestrator via canal clilink-events"
    },
    {
        "terminal-id": "files-assistant-swarm-3",
        "variables": {
            "tentacleName": "Files Assistant",
            "tentacleId": "files-assistant",
            "tentacleContextPath": r"C:\Users\t034183\Desktop\tentacles\.octogent\tentacles\files-assistant",
            "todoItemText": "Adicionar testes",
            "terminalId": "files-assistant-swarm-3",
            "apiPort": "8787",
            "workspaceContextIntro": "You are working on an isolated worktree branch, not the main branch.",
            "workspaceGuidelines": "- You are working in an isolated git worktree on branch `octogent/files-assistant-swarm-3`. Make changes freely without worrying about conflicts with other agents.",
            "commitGuidance": "- Commit your changes with a clear commit message describing what you did.",
            "definitionOfDoneCommitStep": "Changes are committed with a descriptive message.",
            "workspaceReminder": "Commit.",
            "parentTerminalId": "files-assistant-swarm-parent",
            "parentSection": "## Communication\n\nYour parent coordinator is at terminal `files-assistant-swarm-parent`.\nWhen you complete your task, report back:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"DONE: Adicionar testes\" --from files-assistant-swarm-3\n```\nIf you are blocked, ask for help:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"BLOCKED: <describe what you need>\" --from files-assistant-swarm-3\n```"
        },
        "context": "Adicionar testes"
    },
    {
        "terminal-id": "files-assistant-swarm-4",
        "variables": {
            "tentacleName": "Files Assistant",
            "tentacleId": "files-assistant",
            "tentacleContextPath": r"C:\Users\t034183\Desktop\tentacles\.octogent\tentacles\files-assistant",
            "todoItemText": "Documentar no CONTEXT.md",
            "terminalId": "files-assistant-swarm-4",
            "apiPort": "8787",
            "workspaceContextIntro": "You are working on an isolated worktree branch, not the main branch.",
            "workspaceGuidelines": "- You are working in an isolated git worktree on branch `octogent/files-assistant-swarm-4`. Make changes freely without worrying about conflicts with other agents.",
            "commitGuidance": "- Commit your changes with a clear commit message describing what you did.",
            "definitionOfDoneCommitStep": "Changes are committed with a descriptive message.",
            "workspaceReminder": "Commit.",
            "parentTerminalId": "files-assistant-swarm-parent",
            "parentSection": "## Communication\n\nYour parent coordinator is at terminal `files-assistant-swarm-parent`.\nWhen you complete your task, report back:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"DONE: Documentar no CONTEXT.md\" --from files-assistant-swarm-4\n```\nIf you are blocked, ask for help:\n```bash\nnode bin/octogent channel send files-assistant-swarm-parent \"BLOCKED: <describe what you need>\" --from files-assistant-swarm-4\n```"
        },
        "context": "Documentar no CONTEXT.md"
    }
]

octogent_dir = os.path.abspath("octogent")

for cmd in commands:
    args = [
        "node", "bin/octogent", "terminal", "create",
        "--terminal-id", cmd["terminal-id"],
        "--tentacle-id", "files-assistant",
        "--worktree-id", cmd["terminal-id"],
        "--parent-terminal-id", "files-assistant-swarm-parent",
        "--workspace-mode", "worktree",
        "--name", "Files Assistant",
        "--name-origin", "generated",
        "--auto-rename-prompt-context", cmd["context"],
        "--prompt-template", "swarm-worker",
        "--prompt-variables", json.dumps(cmd["variables"]),
        "--agent-provider", "gemini-cli"
    ]
    print(f"Creating terminal {cmd['terminal-id']}...")
    result = subprocess.run(args, cwd=octogent_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to create terminal {cmd['terminal-id']}")
        print(result.stdout)
        print(result.stderr)
    else:
        print(f"Successfully created terminal {cmd['terminal-id']}")
        print(result.stdout)
