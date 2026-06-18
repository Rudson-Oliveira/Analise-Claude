<#
.SYNOPSIS
    Connect-Claude.ps1 — Conecta um agente/usuario a Claude (Anthropic API) com o
    contexto do projeto Hospitalar Solucoes em Saude carregado, e abre um chat
    interativo onde Claude explica o contexto e continua o trabalho.

.DESCRIPTION
    PowerShell nao tem SDK oficial da Anthropic, entao este script usa HTTP puro
    (Invoke-RestMethod) contra POST https://api.anthropic.com/v1/messages.

    O script:
      1. Le a chave em $env:ANTHROPIC_API_KEY.
      2. Carrega CONTEXTO.json (fonte unica da verdade) — local ou do GitHub.
      3. Monta um system prompt de orientacao (protocolo context-engineering).
      4. Abre um REPL: voce digita, Claude responde, o historico e mantido.

    Modelo padrao: claude-opus-4-8 (mais capaz). Thinking adaptativo ligado.

.PARAMETER ContextPath
    Caminho local para CONTEXTO.json. Se ausente, baixa do GitHub (-ContextUrl).

.PARAMETER ContextUrl
    URL raw do CONTEXTO.json no GitHub (padrao: branch main do repo Analise-Claude).

.PARAMETER Model
    ID do modelo Claude. Padrao: claude-opus-4-8.

.PARAMETER MaxTokens
    Limite de tokens de saida por resposta. Padrao: 8000.

.EXAMPLE
    $env:ANTHROPIC_API_KEY = "sk-ant-..."
    ./Connect-Claude.ps1

.EXAMPLE
    ./Connect-Claude.ps1 -ContextPath ./CONTEXTO.json -Model claude-opus-4-8

.NOTES
    Requer PowerShell 7+ (recomendado) ou 5.1. Pede ANTHROPIC_API_KEY no ambiente.
#>

[CmdletBinding()]
param(
    [string]$ContextPath,
    [string]$ContextUrl = "https://raw.githubusercontent.com/Rudson-Oliveira/Analise-Claude/main/CONTEXTO.json",
    [string]$Model      = "claude-opus-4-8",
    [int]$MaxTokens     = 8000
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# ----------------------------------------------------------------------------
# 1. Chave da API
# ----------------------------------------------------------------------------
$apiKey = $env:ANTHROPIC_API_KEY
if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host "ERRO: defina a variavel de ambiente ANTHROPIC_API_KEY antes de rodar." -ForegroundColor Red
    Write-Host '  PowerShell:  $env:ANTHROPIC_API_KEY = "sk-ant-..."' -ForegroundColor Yellow
    exit 1
}

# ----------------------------------------------------------------------------
# 2. Carrega CONTEXTO.json (fonte unica da verdade)
# ----------------------------------------------------------------------------
$contextoJson = $null
if ($ContextPath -and (Test-Path $ContextPath)) {
    Write-Host "Carregando contexto local: $ContextPath" -ForegroundColor DarkGray
    $contextoJson = Get-Content -Path $ContextPath -Raw -Encoding UTF8
}
else {
    try {
        Write-Host "Baixando contexto do GitHub: $ContextUrl" -ForegroundColor DarkGray
        $contextoJson = Invoke-RestMethod -Uri $ContextUrl -Method Get -TimeoutSec 30 | ConvertTo-Json -Depth 20
    }
    catch {
        Write-Host "AVISO: nao consegui carregar o CONTEXTO.json ($($_.Exception.Message))." -ForegroundColor Yellow
        Write-Host "Seguindo sem o contexto estruturado." -ForegroundColor Yellow
        $contextoJson = "{}"
    }
}

# ----------------------------------------------------------------------------
# 3. System prompt de orientacao (protocolo context-engineering)
# ----------------------------------------------------------------------------
$systemPrompt = @"
Voce e o assistente tecnico do projeto de automacao da Hospitalar Solucoes em Saude
(CEO: Rudson Antonio Ribeiro Oliveira). Stack: N8N Cloud + OpenRouter + Evolution API
+ Notion + Google Sheets + Microsoft Outlook. Foco: triagem de WhatsApp/E-mail por IA.

PROTOCOLO (engenharia de contexto — economia de tokens):
- O CONTEXTO.json abaixo e a UNICA fonte da verdade. Confie nele; nao invente fatos.
- Ao iniciar, de um resumo curto (3-5 linhas): onde paramos (meta.proximo_passo),
  pendencias de prioridade ALTA, e a primeira acao sugerida.
- Seja conciso e direto. Nao cole blocos grandes (JSON inteiro, workflows completos);
  cite o campo e resuma. Quando houver decisao, recomende — nao liste tudo.
- Responda em portugues do Brasil.

PRIMEIRA ACAO: confirme se o usuario ja configurou OPENAI_API_KEY (Whisper) e
EVOLUTION_API_KEY (menu WhatsApp 1/2/3), que sao as pendencias ALTA atuais.

=== CONTEXTO.json (fonte da verdade) ===
$contextoJson
=== fim do contexto ===
"@

# ----------------------------------------------------------------------------
# 4. Funcao: chama a Messages API e devolve o texto
# ----------------------------------------------------------------------------
$headers = @{
    "x-api-key"         = $apiKey
    "anthropic-version" = "2023-06-01"
    "content-type"      = "application/json"
}

function Invoke-Claude {
    param([System.Collections.IEnumerable]$Messages)

    $body = [ordered]@{
        model      = $Model
        max_tokens = $MaxTokens
        system     = $systemPrompt
        thinking   = @{ type = "adaptive" }
        messages   = @($Messages)
    } | ConvertTo-Json -Depth 20

    try {
        $resp = Invoke-RestMethod -Uri "https://api.anthropic.com/v1/messages" `
            -Method Post -Headers $headers -Body $body -TimeoutSec 600

        if ($resp.stop_reason -eq "refusal") {
            return "[Claude recusou a solicitacao por motivo de seguranca.]"
        }
        # Concatena apenas os blocos de texto (ignora blocos de thinking)
        $text = ($resp.content | Where-Object { $_.type -eq "text" } |
                 ForEach-Object { $_.text }) -join "`n"
        return $text
    }
    catch {
        $msg = $_.Exception.Message
        if ($_.ErrorDetails.Message) { $msg = $_.ErrorDetails.Message }
        return "[Erro na API: $msg]"
    }
}

# ----------------------------------------------------------------------------
# 5. REPL interativo
# ----------------------------------------------------------------------------
Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Claude conectado ao projeto Analise-Claude (modelo: $Model)" -ForegroundColor Cyan
Write-Host "  Digite sua mensagem. Comandos: 'sair' para encerrar." -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# Lista de mensagens (historico). Primeira interacao: pede o resumo do contexto.
$messages = [System.Collections.Generic.List[object]]::new()
$messages.Add(@{ role = "user"; content = "Conecte-se, leia o CONTEXTO.json e explique onde paramos no projeto. Em seguida me oriente sobre o proximo passo." })

Write-Host "`nClaude esta lendo o contexto..." -ForegroundColor DarkGray
$reply = Invoke-Claude -Messages $messages
$messages.Add(@{ role = "assistant"; content = $reply })
Write-Host "`nClaude:" -ForegroundColor Green
Write-Host $reply

while ($true) {
    Write-Host "`nVoce: " -ForegroundColor Yellow -NoNewline
    $userInput = Read-Host
    if ([string]::IsNullOrWhiteSpace($userInput)) { continue }
    if ($userInput.Trim().ToLower() -in @("sair", "exit", "quit")) {
        Write-Host "Encerrando. Ate logo!" -ForegroundColor Cyan
        break
    }

    $messages.Add(@{ role = "user"; content = $userInput })
    Write-Host "Claude esta pensando..." -ForegroundColor DarkGray
    $reply = Invoke-Claude -Messages $messages
    $messages.Add(@{ role = "assistant"; content = $reply })
    Write-Host "`nClaude:" -ForegroundColor Green
    Write-Host $reply
}
