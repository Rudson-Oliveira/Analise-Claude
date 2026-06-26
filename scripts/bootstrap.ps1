<#
.SYNOPSIS
    Bootstrap completo: baixa/atualiza o projeto Analise-Claude e conecta os
    servidores MCP ao Claude Desktop num unico passo.

.DESCRIPTION
    Faz tudo sozinho:
      1. Garante Git e Python (instala via winget se faltarem e o winget existir).
      2. Clona o repositorio (ou da `git pull` se ja existir).
      3. Roda connect-claude-desktop.ps1 para instalar e registrar os MCPs.
    Pode ser executado de qualquer pasta, inclusive via:
      irm <url-raw>/scripts/bootstrap.ps1 | iex     (sem parametros)

.PARAMETER InstallDir
    Onde clonar o projeto. Padrao: a pasta Documentos do usuario.

.PARAMETER Branch
    Branch a clonar. Padrao: claude/metricool-mcp-server-pr6m40.

.PARAMETER MetricoolToken
    (Opcional) Token de API do Metricool. Se informado, registra tambem o MCP do
    Metricool. Sem ele, apenas o MCP de contexto e registrado.

.PARAMETER MetricoolUserId
    (Opcional) userId do Metricool. Padrao: 4927314.

.EXAMPLE
    .\bootstrap.ps1

.EXAMPLE
    .\bootstrap.ps1 -MetricoolToken "SEU_TOKEN"
#>

[CmdletBinding()]
param(
    [string]$InstallDir = (Join-Path $HOME "Documents"),
    [string]$Branch = "claude/metricool-mcp-server-pr6m40",
    [string]$MetricoolToken = "",
    [string]$MetricoolUserId = "4927314"
)

$ErrorActionPreference = "Stop"
$RepoUrl = "https://github.com/Rudson-Oliveira/Analise-Claude.git"

function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn2($msg) { Write-Host "[!] $msg" -ForegroundColor Yellow }

function Ensure-Tool($cmd, $wingetId, $label) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) { return $true }
    Write-Warn2 "$label nao encontrado."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Step "Instalando $label via winget..."
        winget install -e --id $wingetId --accept-source-agreements --accept-package-agreements
        # Atualiza o PATH do processo atual para enxergar o que foi instalado.
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                    [System.Environment]::GetEnvironmentVariable("Path", "User")
        if (Get-Command $cmd -ErrorAction SilentlyContinue) { Write-Ok "$label instalado."; return $true }
        Write-Warn2 "Instalei $label, mas pode ser preciso FECHAR e REABRIR o PowerShell. Rode o bootstrap de novo."
        return $false
    }
    Write-Warn2 "winget indisponivel. Instale $label manualmente e rode novamente."
    return $false
}

Write-Step "Bootstrap Analise-Claude"

# 1) Pre-requisitos ----------------------------------------------------------
if (-not (Ensure-Tool "git" "Git.Git" "Git")) { throw "Git ausente." }
if (-not (Ensure-Tool "python" "Python.Python.3.12" "Python")) { throw "Python ausente." }

# 2) Clonar ou atualizar -----------------------------------------------------
$repoPath = Join-Path $InstallDir "Analise-Claude"
if (Test-Path (Join-Path $repoPath ".git")) {
    Write-Step "Repositorio ja existe - atualizando ($Branch)..."
    git -C $repoPath fetch origin $Branch --quiet
    git -C $repoPath checkout $Branch --quiet
    git -C $repoPath pull origin $Branch --quiet
} else {
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    Write-Step "Clonando em $repoPath ..."
    git clone -b $Branch $RepoUrl $repoPath --quiet
}
Write-Ok "Codigo pronto: $repoPath"

# 3) Conectar ao Claude Desktop ---------------------------------------------
$connect = Join-Path $repoPath "scripts\connect-claude-desktop.ps1"
$connectArgs = @{ RepoPath = $repoPath; MetricoolUserId = $MetricoolUserId }
if (-not [string]::IsNullOrWhiteSpace($MetricoolToken)) { $connectArgs.MetricoolToken = $MetricoolToken }
& $connect @connectArgs

Write-Host ""
Write-Ok "Bootstrap concluido. Reinicie o Claude Desktop e diga:"
Write-Host "   'restaure o contexto do projeto Analise-Claude e continue'" -ForegroundColor White
