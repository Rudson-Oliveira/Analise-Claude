<#
.SYNOPSIS
    Conecta o projeto Analise-Claude ao Claude Desktop via MCP.

.DESCRIPTION
    Instala os servidores MCP deste repositorio (memoria do projeto e, opcional,
    Metricool) e registra-os no claude_desktop_config.json automaticamente.
    Apos rodar, REINICIE o Claude Desktop: o agente passa a carregar o contexto
    do projeto e (se token informado) a operar o Metricool.

.PARAMETER RepoPath
    Caminho da pasta do repositorio Analise-Claude. Padrao: a pasta deste script.

.PARAMETER MetricoolToken
    (Opcional) Token de API do Metricool. Sem ele, apenas o MCP de contexto e
    registrado. Requer plano Advanced/Custom no Metricool.

.PARAMETER MetricoolUserId
    (Opcional) userId do Metricool. Padrao: 4927314.

.EXAMPLE
    .\connect-claude-desktop.ps1

.EXAMPLE
    .\connect-claude-desktop.ps1 -MetricoolToken "SEU_TOKEN" -MetricoolUserId 4927314
#>

[CmdletBinding()]
param(
    [string]$RepoPath = "",
    [string]$MetricoolToken = "",
    [string]$MetricoolUserId = "4927314"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn2($msg) { Write-Host "[!] $msg" -ForegroundColor Yellow }

# Resolve a raiz do repositorio de forma robusta (PS 5.1 nem sempre popula
# $PSScriptRoot no bloco param, entao resolvemos aqui no corpo).
if ([string]::IsNullOrWhiteSpace($RepoPath)) {
    $scriptDir = $PSScriptRoot
    if ([string]::IsNullOrWhiteSpace($scriptDir)) {
        $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    }
    if (-not [string]::IsNullOrWhiteSpace($scriptDir)) {
        $RepoPath = Split-Path -Parent $scriptDir
    }
    if ([string]::IsNullOrWhiteSpace($RepoPath)) { $RepoPath = (Get-Location).Path }
}

Write-Step "Projeto: $RepoPath"
if (-not (Test-Path (Join-Path $RepoPath "CONTEXTO.json"))) {
    throw "CONTEXTO.json nao encontrado em '$RepoPath'. Aponte -RepoPath para a raiz do repositorio Analise-Claude."
}

# 1) Localizar Python --------------------------------------------------------
Write-Step "Procurando Python 3.11+..."
$python = $null
foreach ($cmd in @("python", "py", "python3")) {
    $found = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($found) {
        $ver = & $found.Source -c "import sys; print('%d.%d' % sys.version_info[:2])" 2>$null
        if ($ver -and [version]$ver -ge [version]"3.11") { $python = $found.Source; break }
    }
}
if (-not $python) {
    Write-Warn2 "Python 3.11+ nao encontrado."
    Write-Host  "Instale com:  winget install -e --id Python.Python.3.12"
    Write-Host  "Depois rode este script novamente."
    throw "Python ausente."
}
Write-Ok "Python: $python ($ver)"

# 2) Instalar os pacotes MCP -------------------------------------------------
Write-Step "Instalando MCP de contexto (analise-context-mcp)..."
& $python -m pip install --upgrade pip --quiet
& $python -m pip install -e (Join-Path $RepoPath "context-mcp") --quiet
Write-Ok "analise-context-mcp instalado."

$installMetricool = -not [string]::IsNullOrWhiteSpace($MetricoolToken)
if ($installMetricool) {
    Write-Step "Instalando MCP do Metricool (metricool-mcp-swiss)..."
    & $python -m pip install -e (Join-Path $RepoPath "metricool-mcp") --quiet
    Write-Ok "metricool-mcp-swiss instalado."
} else {
    Write-Warn2 "Sem -MetricoolToken: registrando apenas o MCP de contexto (Metricool ignorado)."
}

# 3) Montar a configuracao do Claude Desktop --------------------------------
Write-Step "Atualizando claude_desktop_config.json..."
$configDir = Join-Path $env:APPDATA "Claude"
$configPath = Join-Path $configDir "claude_desktop_config.json"
New-Item -ItemType Directory -Force -Path $configDir | Out-Null

if (Test-Path $configPath) {
    Copy-Item $configPath "$configPath.bak" -Force
    Write-Ok "Backup criado: $configPath.bak"
    try { $config = Get-Content $configPath -Raw | ConvertFrom-Json } catch { $config = [pscustomobject]@{} }
} else {
    $config = [pscustomobject]@{}
}
if (-not ($config.PSObject.Properties.Name -contains "mcpServers")) {
    $config | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue ([pscustomobject]@{}) -Force
}

# Servidor de contexto
$contextServer = [pscustomobject]@{
    command = $python
    args    = @("-m", "analise_context_mcp")
    env     = [pscustomobject]@{ ANALISE_CLAUDE_ROOT = $RepoPath }
}
$config.mcpServers | Add-Member -NotePropertyName "analise-claude" -NotePropertyValue $contextServer -Force

# Servidor Metricool (opcional)
if ($installMetricool) {
    $metricoolServer = [pscustomobject]@{
        command = $python
        args    = @("-m", "metricool_mcp")
        env     = [pscustomobject]@{
            METRICOOL_USER_TOKEN = $MetricoolToken
            METRICOOL_USER_ID    = $MetricoolUserId
        }
    }
    $config.mcpServers | Add-Member -NotePropertyName "metricool" -NotePropertyValue $metricoolServer -Force
}

$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
Write-Ok "Config salvo: $configPath"

# 4) Final -------------------------------------------------------------------
Write-Host ""
Write-Step "Pronto! Servidores registrados:"
Write-Host  "   - analise-claude  (memoria do projeto)"
if ($installMetricool) { Write-Host "   - metricool       (Metricool API)" }
Write-Host ""
Write-Warn2 "REINICIE o Claude Desktop (feche pela bandeja e abra de novo)."
Write-Host  "Depois, no chat, peca: 'restaure o contexto do projeto Analise-Claude e continue'."
