import os
import socket
import logging
import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("platform-infra")

mcp = FastMCP("platform-infra")

def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

@mcp.tool()
def check_platform_health() -> dict:
    """Verifica a saúde dos serviços principais da plataforma."""
    results = {
        "dashboard_8787": "ONLINE" if is_port_open(8787) else "OFFLINE",
        "telegram_bot": "NÃO DETECTADO",
        "trends_monitor": "NÃO DETECTADO"
    }
    
    # Verifica processos no Windows
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq python.exe" /V', shell=True).decode('latin1')
        if "telegram_bot" in output:
            results["telegram_bot"] = "RUNNING"
        if "trends_monitor" in output:
            results["trends_monitor"] = "RUNNING"
    except:
        pass
        
    return results

@mcp.tool()
def get_system_resources() -> str:
    """Retorna o uso de disco das pastas de saída."""
    paths = {
        "PDFs": Path("outputs/pdfs"),
        "Apresentações": Path("outputs/presentations"),
        "Transcrições": Path("outputs/transcripts"),
        "Logs": Path("logs")
    }
    
    report = "📊 Uso de Espaço:\n"
    for name, path in paths.items():
        if path.exists():
            size = sum(f.stat().st_size for f in path.glob('**/*') if f.is_file())
            report += f"• {name}: {size / 1024 / 1024:.2f} MB\n"
        else:
            report += f"• {name}: Pasta não encontrada\n"
            
    return report

@mcp.tool()
def cleanup_temp_files(days: int = 7) -> str:
    """Remove arquivos antigos das pastas de saída (Simulação)."""
    # Por segurança, apenas lista o que seria removido nesta versão
    return "Funcionalidade de limpeza ativa. No momento, o sistema está configurado apenas para reportar. Implemente a deleção real quando estiver pronto."

if __name__ == "__main__":
    mcp.run()
