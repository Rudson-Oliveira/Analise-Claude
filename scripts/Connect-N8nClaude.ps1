# ============================================================================
#  Connect-N8nClaude.ps1
#  Conecta o Claude Code ao seu n8n (local + cloud) via n8n-mcp e carrega o
#  contexto do projeto Analise-Claude.
#
#  Empresa: Hospitalar Solucoes em Saude
#  Uso tipico:
#    .\scripts\Connect-N8nClaude.ps1 -LocalApiKey "xxx" -CloudApiKey "yyy" -StartStack
#
#  Requisitos: Windows PowerShell 5.1+ (ou PowerShell 7+), Node.js (npx) e
#  Docker Desktop. Execute na RAIZ do repositorio Analise-Claude.
# ============================================================================

[CmdletBinding()]
param(
    # Chave de API do n8n LOCAL (Settings -> n8n API -> Create API Key)
    [string]$LocalApiKey,

    # Chave de API do n8n CLOUD
    [string]$CloudApiKey,

    # URLs (defaults ja preenchidos para o seu ambiente)
    [string]$LocalUrl = "http://localhost:5678",
    [string]$CloudUrl = "https://rudsonoliveira2323.app.n8n.cloud",

    # Sobe o stack docker (docker compose up -d) antes de testar
    [switch]$StartStack,

    # Caminho do docker-compose.yml (se -StartStack)
    [string]$ComposePath = ".\n8n-local\docker-compose.yml"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg)  { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)    { Write-Host "  [OK] $msg"   -ForegroundColor Green }
function Write-Warn2($msg) { Write-Host "  [!]  $msg"   -ForegroundColor Yellow }
function Test-Cmd($name)   { return [bool](Get-Command $name -ErrorAction SilentlyContinue) }

# ----------------------------------------------------------------------------
# 1. Pre-requisitos
# ----------------------------------------------------------------------------
Write-Step "Verificando pre-requisitos"
if (-not (Test-Cmd "node")) { throw "Node.js nao encontrado. Instale em https://nodejs.org (necessario para 'npx n8n-mcp')." }
Write-Ok ("Node.js: " + (node --version))
if (-not (Test-Cmd "npx"))  { throw "npx nao encontrado (vem com o Node.js)." }
Write-Ok "npx disponivel"
if (Test-Cmd "docker") { Write-Ok ("Docker: " + ((docker --version) -replace 'Docker version ','')) }
else { Write-Warn2 "Docker nao encontrado. Necessario apenas se for usar -StartStack." }

# ----------------------------------------------------------------------------
# 2. Coletar chaves (se nao vieram por parametro) — sem ecoar na tela
# ----------------------------------------------------------------------------
Write-Step "Configurando credenciais (armazenadas como variaveis de ambiente do usuario)"
if (-not $LocalApiKey) {
    $sec = Read-Host "Cole a API Key do n8n LOCAL (Enter para pular)" -AsSecureString
    $LocalApiKey = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
}
if (-not $CloudApiKey) {
    $sec = Read-Host "Cole a API Key do n8n CLOUD (Enter para pular)" -AsSecureString
    $CloudApiKey = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
}

# Persiste no escopo do USUARIO (sobrevive a reboot; nao vai pro git)
[Environment]::SetEnvironmentVariable("N8N_LOCAL_URL", $LocalUrl, "User")
[Environment]::SetEnvironmentVariable("N8N_CLOUD_URL", $CloudUrl, "User")
if ($LocalApiKey) { [Environment]::SetEnvironmentVariable("N8N_LOCAL_API_KEY", $LocalApiKey, "User"); Write-Ok "N8N_LOCAL_API_KEY definida" }
if ($CloudApiKey) { [Environment]::SetEnvironmentVariable("N8N_CLOUD_API_KEY", $CloudApiKey, "User"); Write-Ok "N8N_CLOUD_API_KEY definida" }
# Disponibiliza tambem na sessao atual
$env:N8N_LOCAL_URL = $LocalUrl; $env:N8N_CLOUD_URL = $CloudUrl
if ($LocalApiKey) { $env:N8N_LOCAL_API_KEY = $LocalApiKey }
if ($CloudApiKey) { $env:N8N_CLOUD_API_KEY = $CloudApiKey }

# ----------------------------------------------------------------------------
# 3. Garantir o .mcp.json (Claude Code expande ${VAR} a partir do ambiente)
# ----------------------------------------------------------------------------
Write-Step "Garantindo .mcp.json (config do Claude Code, sem segredos)"
if (-not (Test-Path ".\.mcp.json")) {
    Write-Warn2 ".mcp.json nao existe — sera criado a partir do template do repo."
    # O repo ja versiona um .mcp.json; este bloco e fallback.
    @'
{
  "mcpServers": {
    "n8n-local": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio", "LOG_LEVEL": "error", "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "${N8N_LOCAL_URL:-http://localhost:5678}",
        "N8N_API_KEY": "${N8N_LOCAL_API_KEY}"
      }
    },
    "n8n-cloud": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio", "LOG_LEVEL": "error", "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "${N8N_CLOUD_URL}",
        "N8N_API_KEY": "${N8N_CLOUD_API_KEY}"
      }
    }
  }
}
'@ | Set-Content -Path ".\.mcp.json" -Encoding UTF8
}
Write-Ok ".mcp.json pronto (servidores: n8n-local, n8n-cloud)"

# ----------------------------------------------------------------------------
# 4. (Opcional) Subir o stack docker
# ----------------------------------------------------------------------------
if ($StartStack) {
    Write-Step "Subindo o stack docker"
    if (-not (Test-Path $ComposePath)) { throw "docker-compose.yml nao encontrado em $ComposePath. Crie-o seguindo N8N_LOCAL_INSTALL.md." }
    docker compose -f $ComposePath up -d
    Write-Ok "docker compose up -d disparado"
}

# ----------------------------------------------------------------------------
# 5. Health check do n8n local
# ----------------------------------------------------------------------------
Write-Step "Testando o n8n local em $LocalUrl"
$healthy = $false
for ($i = 1; $i -le 10; $i++) {
    try {
        $r = Invoke-WebRequest -Uri "$LocalUrl/healthz" -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -eq 200) { $healthy = $true; break }
    } catch { Start-Sleep -Seconds 3 }
}
if ($healthy) { Write-Ok "/healthz respondeu 200" }
else { Write-Warn2 "n8n local nao respondeu. Suba o stack (-StartStack) ou verifique o Docker." }

# ----------------------------------------------------------------------------
# 6. Testar a API com a chave (valida a conexao que o n8n-mcp usara)
# ----------------------------------------------------------------------------
function Test-N8nApi($label, $url, $key) {
    if (-not $key) { Write-Warn2 "$label: sem API Key — pulando teste."; return }
    try {
        $resp = Invoke-RestMethod -Uri "$url/api/v1/workflows?limit=1" -Headers @{ "X-N8N-API-KEY" = $key } -TimeoutSec 10
        Write-Ok "$label: API autenticada com sucesso"
    } catch {
        Write-Warn2 "$label: falha ao autenticar na API ($url). Verifique a API Key. Detalhe: $($_.Exception.Message)"
    }
}
Write-Step "Validando as APIs do n8n (mesma conexao do n8n-mcp)"
Test-N8nApi "n8n-local" $LocalUrl $env:N8N_LOCAL_API_KEY
Test-N8nApi "n8n-cloud" $CloudUrl $env:N8N_CLOUD_API_KEY

# ----------------------------------------------------------------------------
# 7. Prompt de retomada — cole no Claude Code para eu carregar o contexto
# ----------------------------------------------------------------------------
Write-Step "Tudo pronto. Abra o Claude Code NESTA pasta e cole o prompt abaixo:"
$prompt = @"
Leia o CLAUDE.md e o CONTEXTO.json deste repositorio (Analise-Claude) e me de um
resumo do estado atual do projeto: arquitetura hibrida (n8n local PC + cloud),
workflows ativos, pendencias e proximos passos. Os servidores MCP 'n8n-local' e
'n8n-cloud' estao conectados — confirme que voce consegue listar meus workflows.
"@
Write-Host "`n----------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host $prompt -ForegroundColor White
Write-Host "----------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "`nDica: se voce acabou de definir as variaveis de ambiente, reinicie o" -ForegroundColor DarkGray
Write-Host "Claude Code para que ele enxergue N8N_LOCAL_API_KEY / N8N_CLOUD_API_KEY.`n" -ForegroundColor DarkGray
