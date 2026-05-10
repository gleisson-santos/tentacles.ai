# start_tentacles.ps1 - Launcher oficial do projeto Tentacles

$ROOT = Get-Location

Write-Host "========================================" -ForegroundColor Magenta
Write-Host "   TENTACLES.AI - INICIANDO PLATAFORMA" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta

# 0. Sincronização de Uso (Gemini + Outros)
$env:PATH = "C:\Program Files\GitHub CLI\;" + $env:PATH
Write-Host "[0/3] Sincronizando métricas de uso (Gemini)..." -ForegroundColor Yellow
python scripts/usage_aggregator.py

# 1. Dashboard Octogent
Write-Host "[1/3] Abrindo Dashboard na porta 8787..." -ForegroundColor Yellow
$ROOT_DYNAMIC = $PSScriptRoot
$env:OCTOGENT_PORT = "8787"
$env:OCTOGENT_WORKSPACE_CWD = $ROOT_DYNAMIC
# Mudança crucial: Iniciamos da RAIZ dinâmica, apontando para o binário na subpasta
Start-Process cmd -ArgumentList "/k", "title Octogent Dashboard && set PATH=C:\Program Files\GitHub CLI\;%PATH% && set OCTOGENT_PORT=8787 && set OCTOGENT_WORKSPACE_CWD=$ROOT_DYNAMIC && cd /d $ROOT_DYNAMIC && node octogent/bin/octogent"

# 2. Trends Intelligence (Monitor de Notícias)
Write-Host "[2/3] Iniciando Trends Monitor..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "title Trends Intelligence && cd /d $ROOT_DYNAMIC && python scripts/trends_monitor.py --loop"

# 3. Telegram Bot (Interface)
Write-Host "[3/3] Iniciando Telegram Bot (Modo Async)..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "title Telegram Bot && cd /d $ROOT_DYNAMIC && python bots/telegram_bot.py"

Write-Host "`n🚀 Tudo pronto! Acesse http://localhost:8787" -ForegroundColor Green
Write-Host "Pressione qualquer tecla para fechar este launcher (os serviços continuarão rodando)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
