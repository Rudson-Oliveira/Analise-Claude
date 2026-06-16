<#
.SYNOPSIS
    Abre uma sessao do Claude Code ja conectada ao projeto Analise-Claude,
    com todo o contexto do projeto carregado automaticamente.

.DESCRIPTION
    Este script prepara o ambiente Windows e inicia o Claude Code apontado para
    o repositorio Analise-Claude. O Claude le automaticamente o CLAUDE.md
    (orientacao do projeto) e, no prompt inicial, e instruido a ler o CONTEXTO.json,
    o checkpoint mais recente, e continuar de onde paramos.

    O que ele faz, em ordem:
      1. Garante que o Claude Code CLI esta instalado (instala se faltar).
      2. Clona o repositorio (ou faz git pull/checkout se ja existir localmente).
      3. Configura a autenticacao (login interativo OU ANTHROPIC_API_KEY).
      4. Inicia o Claude Code dentro da pasta do projeto com um prompt de contexto.

    Um "agente" (humano ou automatizado) roda este script e cai numa sessao do
    Claude que ja sabe explicar o estado do projeto e o proximo passo.

.PARAMETER ProjectPath
    Pasta local onde o repositorio fica/ficara. Padrao: %USERPROFILE%\Analise-Claude

.PARAMETER Branch
    (Opcional) Branch a usar. Padrao: main.

.PARAMETER ApiKey
    (Opcional) Chave da API Anthropic. Se omitida, usa a variavel de ambiente
    ANTHROPIC_API_KEY se existir; caso contrario, login interativo no navegador.

.PARAMETER Resume
    (Opcional) Retoma a ultima sessao do Claude neste projeto (claude --continue)
    em vez de iniciar uma nova.

.PARAMETER Headless
    (Opcional) Modo nao-interativo (-p): o Claude le o contexto, responde uma vez
    e sai. Util para um agente automatizado coletar o resumo do projeto.

.EXAMPLE
    .\iniciar-claude.ps1
    Modo interativo padrao (branch main).

.EXAMPLE
    .\iniciar-claude.ps1 -Branch claude/installation-feasibility-k0q8lx
    Abre a sessao ja na branch de trabalho atual.

.EXAMPLE
    .\iniciar-claude.ps1 -ApiKey "sk-ant-..." -Headless
    Um agente roda isto, recebe o resumo do projeto e encerra.

.EXAMPLE
    .\iniciar-claude.ps1 -Resume
    Retoma a conversa anterior de onde parou.
#>

[CmdletBinding()]
param(
    [string]$ProjectPath = (Join-Path $env:USERPROFILE 'Analise-Claude'),
    [string]$Branch = 'main',
    [string]$ApiKey,
    [switch]$Resume,
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

# --- 2. Garante o repositorio local na branch certa -------------------------
Write-Step "Preparando o repositorio em: $ProjectPath (branch: $Branch)"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git nao encontrado. Instale o Git para Windows: https://git-scm.com/download/win"
}
if (Test-Path (Join-Path $ProjectPath '.git')) {
    Write-Ok 'Repositorio ja existe. Sincronizando...'
    git -C $ProjectPath fetch origin
    git -C $ProjectPath checkout $Branch
    git -C $ProjectPath pull --ff-only origin $Branch
} else {
    Write-Warn 'Repositorio nao encontrado. Clonando...'
    git clone --branch $Branch $RepoUrl $ProjectPath
    Write-Ok 'Repositorio clonado.'
}

# Confirma que o contexto essencial existe.
foreach ($f in @('CLAUDE.md', 'CONTEXTO.json', 'README.md')) {
    if (-not (Test-Path (Join-Path $ProjectPath $f))) {
        Write-Warn "Arquivo de contexto ausente: $f (a sessao ainda funciona, mas o contexto pode estar incompleto)."
    }
}
if (Test-Path (Join-Path $ProjectPath '.claude\skills')) {
    Write-Ok 'Skills do Claude Code detectadas (.claude\skills).'
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

if ($Resume) {
    Write-Ok 'Retomando a ultima sessao (claude --continue).'
    claude --continue
    return
}

$promptInicial = @'
Voce esta no projeto Analise-Claude: a memoria do sistema de automacao n8n da
Hospitalar Solucoes em Saude (proprietario: Rudson Oliveira, CEO).

Para restaurar o contexto, NESTA ORDEM:
  1. Leia CLAUDE.md (sua orientacao - regras e convencoes do projeto).
  2. Leia CONTEXTO.json (estado estruturado = fonte da verdade).
  3. Leia o README.md e o CHECKPOINT_*.md mais recente.

Depois, me responda em portugues (BR), de forma curta:
  - Resumo do estado atual (workflows ativos, pendencias).
  - O proximo passo recomendado (Fase 2).
  - Pergunte se ja tenho OPENAI_API_KEY e EVOLUTION_API_KEY para configurar.

Nao altere nada ainda - so restaure o contexto e proponha o proximo passo.
'@

if ($Headless) {
    # Modo nao-interativo: o agente recebe o resumo e o processo encerra.
    claude -p $promptInicial
} else {
    # Modo interativo: abre a sessao ja com o prompt de contexto.
    claude $promptInicial
}
