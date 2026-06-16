# ============================================================================
#  Install-N8nNative.ps1
#  Instala e inicia o n8n no Windows SEM Docker (via Node.js/npm).
#  Empresa: Hospitalar Solucoes em Saude | Projeto Analise-Claude
#
#  Uso (cole no PowerShell):
#    irm https://raw.githubusercontent.com/Rudson-Oliveira/Analise-Claude/claude/n8n-local-install-xltfsv/scripts/Install-N8nNative.ps1 | iex
#  ou rode localmente:
#    .\scripts\Install-N8nNative.ps1
# ============================================================================

$ErrorActionPreference = "Stop"
function Write-Step($m) { Write-Host "`n==> $m" -ForegroundColor Cyan }
function Write-Ok($m)   { Write-Host "  [OK] $m" -ForegroundColor Green }

# ----------------------------------------------------------------------------
# 1. Node.js 20+
# ----------------------------------------------------------------------------
Write-Step "Verificando Node.js (n8n exige >= 20)"
$nodeOk = $false
try {
    $v = (node --version) 2>$null
    if ($v -match 'v(\d+)\.') { if ([int]$Matches[1] -ge 20) { $nodeOk = $true; Write-Ok "Node $v" } }
} catch {}

if (-not $nodeOk) {
    Write-Step "Node ausente ou antigo — instalando Node.js LTS via winget"
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "winget nao encontrado. Instale o Node LTS manualmente em https://nodejs.org e rode este script de novo."
    }
    winget install -e --id OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
    # Recarrega o PATH na sessao atual (winget nao atualiza sozinho)
    $env:Path = [Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [Environment]::GetEnvironmentVariable("Path","User")
    $v = node --version
    Write-Ok "Node instalado: $v"
}

# ----------------------------------------------------------------------------
# 2. Instalar n8n (global)
# ----------------------------------------------------------------------------
Write-Step "Instalando o n8n (npm install -g n8n) — pode levar 1-3 min"
npm install -g n8n
Write-Ok "n8n instalado: $(n8n --version 2>$null)"

# ----------------------------------------------------------------------------
# 3. Iniciar
# ----------------------------------------------------------------------------
Write-Step "Iniciando o n8n em http://localhost:5678"
$env:GENERIC_TIMEZONE = "America/Sao_Paulo"
$env:TZ = "America/Sao_Paulo"
Write-Host "`nDeixe esta janela ABERTA (e o n8n rodando)." -ForegroundColor Yellow
Write-Host "Abra http://localhost:5678 no navegador e crie sua conta.`n" -ForegroundColor Yellow
n8n start
