<#
.SYNOPSIS
    Abre uma sessao do Claude Code ja conectada ao projeto Analise-Claude,
    com o contexto do projeto carregado automaticamente.

.DESCRIPTION
    Este script prepara o ambiente Windows e inicia o Claude Code apontado para
    o repositorio Analise-Claude. O Claude le automaticamente o arquivo CLAUDE.md
    (orientacao do projeto) e, no prompt inicial, e instruido a ler o CONTEXTO.json
    e continuar de onde paramos.

    O que ele faz, em ordem:
      1. Garante que o Claude Code CLI esta instalado (instala se faltar).
      2. Clona o repositorio (ou faz git pull se ja existir localmente).
      3. Configura a autenticacao (login interativo OU ANTHROPIC_API_KEY).
      4. Inicia o Claude Code dentro da pasta do projeto com um prompt inicial.

.PARAMETER ProjectPath
    Pasta local onde o repositorio fica/ficara. Padrao: %USERPROFILE%\Analise-Claude

.PARAMETER ApiKey
    (Opcional) Chave da API Anthropic. Se omitida, usa a variavel de ambiente
    ANTHROPIC_API_KEY se existir; caso contrario, o Claude faz login interativo
    pelo navegador na primeira execucao.

.PARAMETER Headless
    (Opcional) Roda em modo nao-interativo (-p): o Claude le o contexto, responde
    uma vez e sai. Util para um agente automatizado coletar o resumo do projeto.

.EXAMPLE
    .\iniciar-claude.ps1
    Modo interativo padrao.

.EXAMPLE
    .\iniciar-claude.ps1 -ApiKey "sk-ant-..." -Headless
    Um agente roda isto, recebe o resumo do projeto e encerra.
#>

[CmdletBinding()]
param(
    [string]$ProjectPath = (Join-Path $env:USERPROFILE 'Analise-Claude'),
    [string]$ApiKey,
    [switch]$Headless
)

$ErrorActionPreference = 'Stop'
$RepoUrl = 'https://github.com/Rudson-Oliveira/Analise-Claude.git'

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "    [ok] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "    [!] $msg"  -ForegroundColor Yellow }

# --- 1. Garante o Claude Code CLI -------------------------------------------
Write-Step 'Verificando o Claude Code CLI'
if (Get-Command claude -ErrorAction SilentlyContinue) {
    Write-Ok 'Claude Code ja esta instalado.'
} else {
    Write-Warn 'Claude Code nao encontrado. Instalando...'
    # Instalador oficial para Windows (binario nativo; nao usa npm).
    Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression
    # Recarrega o PATH da sessao atual para encontrar o 'claude' recem-instalado.
    $env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'User') + ';' +
                [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
    if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
        throw "Claude Code foi instalado, mas 'claude' nao esta no PATH. Feche e reabra o PowerShell e rode o script de novo."
    }
    Write-Ok 'Claude Code instalado.'
}

# --- 2. Garante o repositorio local -----------------------------------------
Write-Step "Preparando o repositorio em: $ProjectPath"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git nao encontrado. Instale o Git para Windows: https://git-scm.com/download/win"
}
if (Test-Path (Join-Path $ProjectPath '.git')) {
    Write-Ok 'Repositorio ja existe. Atualizando (git pull)...'
    git -C $ProjectPath pull --ff-only
} else {
    Write-Warn 'Repositorio nao encontrado. Clonando...'
    git clone $RepoUrl $ProjectPath
    Write-Ok 'Repositorio clonado.'
}

# --- 3. Autenticacao ---------------------------------------------------------
Write-Step 'Configurando autenticacao'
if ($ApiKey) {
    $env:ANTHROPIC_API_KEY = $ApiKey
    Write-Ok 'Usando a ANTHROPIC_API_KEY fornecida via parametro.'
} elseif ($env:ANTHROPIC_API_KEY) {
    Write-Ok 'Usando a ANTHROPIC_API_KEY ja presente no ambiente.'
} else {
    Write-Warn 'Sem API key: o Claude fara login interativo pelo navegador na primeira execucao.'
}

# --- 4. Inicia o Claude Code com o contexto ---------------------------------
Write-Step 'Iniciando o Claude Code'
Set-Location $ProjectPath

$promptInicial = @'
Voce esta no projeto Analise-Claude (memoria do sistema de automacao n8n da
Hospitalar Solucoes em Saude). Leia o arquivo CLAUDE.md e o CONTEXTO.json para
restaurar todo o contexto, depois me de um resumo curto do estado atual e do
proximo passo recomendado da Fase 2.
'@

if ($Headless) {
    # Modo nao-interativo: o agente recebe o resumo e o processo encerra.
    claude -p $promptInicial
} else {
    # Modo interativo: abre a sessao ja com o prompt inicial.
    claude $promptInicial
}
