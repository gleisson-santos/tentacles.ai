@echo off
TITLE Tentacles.ai Launcher
SETLOCAL EnableDelayedExpansion

echo ========================================
echo    TENTACLES.AI - Iniciando Agentes
echo ========================================

:: 1. Carregar variaveis do .env
if exist ".env" (
    echo [OK] Carregando chaves do arquivo .env...
    for /f "usebackq tokens=*" %%a in (".env") do (
        set "line=%%a"
        if not "!line:~0,1!"=="#" (
            set "%%a"
        )
    )
)

:: 2. Trends Monitor (Serviço de Background - 2h loop)
echo [1/4] Iniciando Trends Monitor (Noticias/YouTube)...
start "Trends Monitor" cmd /k "python scripts/trends_monitor.py"
timeout /t 2 /nobreak > nul

:: 3. LinkedIn Auto-Poster
echo [2/4] Iniciando LinkedIn Auto-Poster...
start "LinkedIn Poster" cmd /k "echo === LinkedIn Auto-Poster === && python auto_poster.py"
timeout /t 2 /nobreak > nul

:: 4. Octogent Dashboard
echo [3/4] Iniciando Octogent Dashboard...
start "Octogent Dashboard" cmd /k "echo === Octogent Dashboard === && octogent"
timeout /t 3 /nobreak > nul

:: 5. Telegram Bot
if NOT "%TELEGRAM_BOT_TOKEN%"=="" (
    echo [4/4] Iniciando Telegram Bot...
    start "Telegram Bot" cmd /k "echo === Telegram Bot === && python bots/telegram_bot.py"
)

echo.
echo ========================================
echo    Tudo iniciado com sucesso!
echo    Dashboard: http://localhost:8787
echo ========================================
echo.
pause
