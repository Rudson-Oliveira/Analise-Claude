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
      2. Clona o repositorio (ou faz git fetch se ja existir).
      3. Faz checkout da branch de trabalho desejada e atualiza (pull ff-only).
      4. Configura a autenticacao (login interativo OU ANTHROPIC_API_KEY).
      5. Inicia o Claude Code dentro da pasta do projeto com um prompt inicial.
         (O .mcp.json do repo - servidor 'markitdown' - e carregado automaticamente.)

.PARAMETER ProjectPath
    Pasta local onde o repositorio fica/ficara. Padrao: %USERPROFILE%\Analise-Claude

.PARAMETER Branch
    Branch para checkout. Padrao: main. Use a branch de trabalho quando for
    continuar uma tarefa (ex.: claude/system-integration-check-kftmq2).

.PARAMETER ApiKey
    (Opcional) Chave da API Anthropic. Se omitida, usa a variavel de ambiente
    ANTHROPIC_API_KEY se existir; caso contrario, o Claude faz login interativo
    pelo navegador na primeira execucao.

.PARAMETER Model
    (Opcional) Modelo a usar (ex.: 'opus', 'sonnet', 'haiku'). Se omitido, usa a
    configuracao padrao do Claude Code. O projeto prefere os modelos Claude mais recentes.

.PARAMETER Headless
    (Opcional) Roda em modo nao-interativo (-p): o Claude le o contexto, responde
    uma vez e sai. Util para um agente automatizado coletar o resumo do projeto.

.PARAMETER OutFile
    (Opcional) Em modo Headless, salva o resumo do projeto neste arquivo (UTF-8),
    alem de exibi-lo na tela. Ideal para um agente capturar o estado do projeto.

.EXAMPLE
    .\iniciar-claude.ps1
    Modo interativo padrao (branch main).

.EXAMPLE
    .\iniciar-claude.ps1 -Branch claude/system-integration-check-kftmq2
    Continua o trabalho na branch de desenvolvimento.

.EXAMPLE
    .\iniciar-claude.ps1 -ApiKey "sk-ant-..." -Headless -OutFile contexto-atual.txt
    Um agente roda isto, recebe o resumo do projeto, salva em arquivo e encerra.
#>

[CmdletBinding()]
param(
    [string]$ProjectPath = (Join-Path $env:USERPROFILE 'Analise-Claude'),
    [string]$Branch = 'main',
    [string]$ApiKey,
    [string]$Model,
    [switch]$Headless,
    [string]$OutFile
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
    Write-Ok 'Repositorio ja existe. Buscando atualizacoes (git fetch)...'
    git -C $ProjectPath fetch origin --prune
} else {
    Write-Warn 'Repositorio nao encontrado. Clonando...'
    git clone $RepoUrl $ProjectPath
    Write-Ok 'Repositorio clonado.'
}

# --- 3. Checkout da branch de trabalho --------------------------------------
Write-Step "Selecionando a branch: $Branch"
git -C $ProjectPath checkout $Branch
# Atualiza a branch local com o remoto (fast-forward); ignora se nao houver upstream.
git -C $ProjectPath pull --ff-only 2>$null
Write-Ok "Na branch '$Branch'."

# --- 4. Autenticacao ---------------------------------------------------------
Write-Step 'Configurando autenticacao'
if ($ApiKey) {
    $env:ANTHROPIC_API_KEY = $ApiKey
    Write-Ok 'Usando a ANTHROPIC_API_KEY fornecida via parametro.'
} elseif ($env:ANTHROPIC_API_KEY) {
    Write-Ok 'Usando a ANTHROPIC_API_KEY ja presente no ambiente.'
} else {
    Write-Warn 'Sem API key: o Claude fara login interativo pelo navegador na primeira execucao.'
}

# --- 5. Inicia o Claude Code com o contexto ---------------------------------
Write-Step 'Iniciando o Claude Code'
Set-Location $ProjectPath

$promptInicial = @'
Voce esta no projeto Analise-Claude (memoria do sistema de automacao n8n da
Hospitalar Solucoes em Saude). Restaure o contexto na ordem:
  1. Leia BASE_CONHECIMENTO.md (o ORACULO: conhecimento completo do projeto).
  2. Leia CLAUDE.md (orientacao operacional) e cruze com CONTEXTO.json.
  3. Confira o checkpoint mais recente (CHECKPOINT_*.md), se houver.
Depois, me de um resumo curto (5-8 linhas) com: estado atual, workflows ativos,
pendencias de maior prioridade e o proximo passo recomendado da Fase 2.
'@

# Monta os argumentos do CLI dinamicamente.
$claudeArgs = @()
if ($Model) { $claudeArgs += @('--model', $Model) }

if ($Headless) {
    # Modo nao-interativo: o agente recebe o resumo e o processo encerra.
    if ($OutFile) {
        claude @claudeArgs -p $promptInicial | Tee-Object -FilePath $OutFile
        Write-Ok "Resumo salvo em: $OutFile"
    } else {
        claude @claudeArgs -p $promptInicial
    }
} else {
    # Modo interativo: abre a sessao ja com o prompt inicial.
    claude @claudeArgs $promptInicial
}
