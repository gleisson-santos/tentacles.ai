@echo off
TITLE Tentacles.ai Launcher
SETLOCAL EnableDelayedExpansion

echo ========================================
echo    TENTACLES.AI - Iniciando Agentes
echo ========================================

:: Pegar o caminho absoluto sem barra final e sem aspas
SET "ROOT_PATH=%~dp0"
if "%ROOT_PATH:~-1%"=="\" SET "ROOT_PATH=%ROOT_PATH:~0,-1%"

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

:: 2. Trends Monitor
echo [1/4] Iniciando Trends Monitor...
start "Trends Monitor" cmd /k "echo === Trends Monitor === && python scripts/trends_monitor.py"
timeout /t 2 /nobreak > nul

:: 3. LinkedIn Auto-Poster
echo [2/4] Iniciando LinkedIn Auto-Poster...
start "LinkedIn Poster" cmd /k "echo === LinkedIn Auto-Poster === && python scripts/linkedin_poster.py"
timeout /t 2 /nobreak > nul

:: 4. Octogent Dashboard
echo [3/4] Iniciando Octogent Dashboard...
:: Passando o CWD via CD temporário para garantir que o Node pegue o caminho correto
start "Octogent Dashboard" cmd /k "echo === Octogent Dashboard === && set "OCTOGENT_WORKSPACE_CWD=%ROOT_PATH%" && cd /d "%ROOT_PATH%\octogent" && pnpm dev"
timeout /t 5 /nobreak > nul

:: 5. Telegram Bot
if NOT "%TELEGRAM_BOT_TOKEN%"=="" (
    echo [4/4] Iniciando Telegram Bot...
    start "Telegram Bot" cmd /k "echo === Telegram Bot === && cd /d "%ROOT_PATH%" && python bots/telegram_bot.py"
)

echo.
echo ========================================
echo    Tudo iniciado com sucesso!
echo    Pasta: %ROOT_PATH%
echo    Dashboard: http://localhost:8787
echo ========================================
echo.
pause
