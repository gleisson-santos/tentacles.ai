# setup.ps1 - Automação de Configuração do Tentacles

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   TENTACLES.AI - SETUP AUTOMÁTICO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Instalar dependências Python
Write-Host "`n[1/4] Instalando dependências Python..." -ForegroundColor Yellow
python -m pip install -r requirements.txt

# 2. Configurar Octogent (Node.js)
Write-Host "`n[2/4] Instalando dependências e compilando Dashboard..." -ForegroundColor Yellow
Set-Location octogent
pnpm install
pnpm build

# 3. Criar link profissional do comando 'octogent'
Write-Host "`n[3/4] Configurando comando CLI global..." -ForegroundColor Yellow
npm link
Set-Location ..

# 4. Verificar arquivo .env
if (-not (Test-Path .env)) {
    Write-Host "`n[4/4] Criando template de .env..." -ForegroundColor Yellow
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
    } else {
        # Cria um dummy se não houver example
        "GROQ_API_KEY=your_key_here`nSTABILITY_KEY=your_key_here`nTELEGRAM_BOT_TOKEN=your_token_here`nALLOWED_USER_ID=0" | Out-File .env -Encoding utf8
    }
    Write-Host "⚠️  ATENÇÃO: Arquivo .env criado. Adicione suas chaves de API nele." -ForegroundColor Red
} else {
    Write-Host "`n[4/4] Arquivo .env já existe. Pulando..." -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   SETUP CONCLUÍDO COM SUCESSO!" -ForegroundColor Cyan
Write-Host "   Agora você pode usar o comando 'octogent' em qualquer lugar." -ForegroundColor Cyan
Write-Host "   Para iniciar tudo, use: ./start_tentacles.ps1" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
