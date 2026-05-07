# start_clilink.ps1 — Inicia todos os agentes Clilink
# Uso: .\start_clilink.ps1
# Pressione Ctrl+C em cada janela para parar individualmente

$dir = $PSScriptRoot
$py  = "python" # Assume python está no PATH

# Carrega variáveis do .env se existir
if (Test-Path "$dir\.env") {
    Get-Content "$dir\.env" | ForEach-Object {
        if ($_ -match "^([^=]+)=(.+)$") {
            [System.Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], "Process")
        }
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   CLILINK — Iniciando agentes..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. LinkedIn Auto-Poster (2h loop)
Write-Host "`n[1/3] LinkedIn Auto-Poster..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command",
    "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new(); Set-Location '$dir'; Write-Host '=== LinkedIn Auto-Poster ===' -ForegroundColor Green; & '$py' auto_poster.py"

Start-Sleep -Seconds 2

# 2. Octogent Dashboard
Write-Host "[2/3] Octogent Dashboard..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command",
    "Set-Location '$dir'; Write-Host '=== Octogent Dashboard ===' -ForegroundColor Magenta; octogent"

Start-Sleep -Seconds 3

# 3. Telegram Bot (se token estiver configurado)
if ($env:TELEGRAM_BOT_TOKEN -and $env:TELEGRAM_BOT_TOKEN -ne "SEU_TOKEN_AQUI") {
    Write-Host "[3/3] Telegram Bot..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command",
        "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new(); Set-Location '$dir'; Write-Host '=== Telegram Bot ===' -ForegroundColor Blue; & '$py' bots/telegram_bot.py"
} else {
    Write-Host "[3/3] Telegram Bot PULADO (configure: `$env:TELEGRAM_BOT_TOKEN = 'token')" -ForegroundColor DarkGray
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Tudo iniciado!" -ForegroundColor Green
Write-Host "   Dashboard: http://localhost:8787" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nPara criar tentaculos no Octogent (apos ele iniciar):" -ForegroundColor White
Write-Host "  octogent tentacle create linkedin-poster" -ForegroundColor Gray
Write-Host "  octogent tentacle create google-assistant" -ForegroundColor Gray
Write-Host "  octogent tentacle create files-assistant" -ForegroundColor Gray
Write-Host "  octogent tentacle create telegram-bot" -ForegroundColor Gray
