# Integração — Scrapling (D4Vinci)

> **Status:** 📋 Documentado / pronto para configurar | **Data:** 27/06/2026
> **Decisão:** conectar via **servidor MCP nativo do Scrapling** (`scrapling mcp`) — o agente Claude
> dirige tudo; **ninguém precisa escrever Python**.

## 🎯 O que é

[Scrapling](https://github.com/D4Vinci/Scrapling) é uma biblioteca **open-source (BSD-3, Python)** de
**web scraping adaptativo**. O grande diferencial: passa por sistemas **anti-bot** (Cloudflare Turnstile)
"sem ninguém perceber", e **não quebra quando o site muda de layout** — ele reencontra o elemento.

> 🔑 **Por que Python não é impeditivo aqui:** o Scrapling já vem com um **servidor MCP nativo**. A gente
> registra ele no `.mcp.json` (igual ao `markitdown`) e o **agente Claude opera as ferramentas** — o
> proprietário não toca em código. "Juntar e resolver", não "travar por causa da linguagem".

### Os 3 modos de busca (fetchers)
| Modo | Para quê |
|---|---|
| **get** | HTTP rápido, imitando fingerprint TLS de browser real |
| **fetch** | Browser completo (Chromium) — sites que dependem de JavaScript |
| **stealthy_fetch** | O "stealth": resolve Cloudflare Turnstile/Interstitial e anti-bots |

## 🧩 Ferramentas expostas pelo MCP (10)

```
get               → HTTP rápido (1 URL)         bulk_get            → vários URLs em paralelo
fetch             → browser dinâmico (1 URL)    bulk_fetch          → vários URLs (browser)
stealthy_fetch    → anti-bot/Cloudflare (1 URL) bulk_stealthy_fetch → vários URLs (stealth)
screenshot        → print PNG/JPEG da página
open_session / close_session / list_sessions    → sessões de browser persistentes
```

**Extração inteligente embutida** — converte a página para **Markdown / HTML / texto limpo** e aceita
**seletores CSS** para pegar só o trecho que interessa (reduz tokens enviados à IA).
Parâmetro `main_content_only` (padrão `true`) filtra menus/anúncios **e ativa proteção contra
prompt-injection** — relevante por segurança.

## 🧩 Onde encaixa no nosso ecossistema

```
Site sem API (ex.: tabela de preços de fornecedor) → Scrapling (stealthy_fetch) →
Markdown limpo → OpenRouter (Claude) → triagem/decisão → Notion/Sheets/WhatsApp
```

Casos naturais de uso na Hospitalar:
- **Monitorar preços/disponibilidade** de fornecedores que não têm API.
- **Coletar dados públicos** de portais (licitações, ANVISA, editais) para o briefing diário (COCKPIT-08).
- **Pré-coleta** antes do MarkItDown/OpenRouter quando a fonte é um site protegido, não um arquivo.

> ⚠️ **Nota de arquitetura:** o `scrapling mcp` roda **localmente** (STDIO) e serve ao **agente Claude**.
> Ele **não** se conecta diretamente ao n8n **Cloud**. Para um pipeline 100% automático dentro do n8n
> Cloud, o caminho é um **microserviço HTTP** (ex.: Railway/Docker `pyd4vinci/scrapling`) chamado por um
> **HTTP Request node** — mesmo padrão já previsto para o MarkItDown. Avaliar quando houver caso real.

## ⚙️ Como configurar (Claude Code / Desktop)

### 1) Instalar (uma vez, na máquina onde roda o Claude)

```bash
pip install "scrapling[ai]"
scrapling install   # baixa o browser (Chromium) usado por fetch/stealthy_fetch
```

> Requer **Python 3.10+**. O `scrapling[ai]` traz o servidor MCP. O `scrapling install` é obrigatório
> para os modos com browser (`fetch`, `stealthy_fetch`, `screenshot`).

### 2) Bloco de configuração MCP

> ✅ **Pronto no repo:** o **`.mcp.json`** da raiz já inclui o bloco abaixo — basta instalar o pacote
> (passo 1) e abrir o Claude Code neste diretório.

```json
{
  "mcpServers": {
    "scrapling": {
      "command": "scrapling",
      "args": ["mcp"]
    }
  }
}
```

**Dica (caminho absoluto):** se o `scrapling` não estiver no PATH, use o caminho completo do executável
(ex.: `.../.venv/bin/scrapling` no Linux/Mac ou `...\\Scripts\\scrapling.exe` no Windows) no campo
`command`. Para registrar via CLI: `claude mcp add scrapling "<caminho>/scrapling" mcp`.

**Modo HTTP (opcional, ≥ v0.3.6):** `scrapling mcp --http` expõe transporte "Streamable HTTP" para testes.

Depois de configurar, **feche e reabra** o cliente Claude.

## 🔒 Segurança e conformidade (LEIA — negócio de saúde)

- **Respeitar Termos de Uso e `robots.txt`** dos sites-alvo. O próprio projeto declara uso
  educacional/pesquisa; o uso é de responsabilidade de quem opera.
- **LGPD:** não coletar dados pessoais/sensíveis de terceiros sem base legal. Preferir **dados públicos**
  (preços, editais, bulas) — nunca PII/PHI sem necessidade e amparo.
- **APIs oficiais têm prioridade:** scraping é o **plano B**, só quando a fonte não oferece integração.
- `main_content_only=true` mantém a **proteção contra prompt-injection** ligada — não desligar sem motivo.

## 📋 Próximos passos

1. Instalar `scrapling[ai]` + `scrapling install` na máquina do Claude (via `scripts/bootstrap.ps1` no Windows).
2. Testar um `stealthy_fetch` em um portal real de fornecedor → Markdown → resumo pela IA.
3. Se um caso justificar automação total no n8n Cloud, subir o microserviço HTTP (Railway) e plugar via HTTP Request.

## 🔗 Fontes

- Repositório: <https://github.com/D4Vinci/Scrapling>
- Guia do MCP Server: <https://scrapling.readthedocs.io/en/latest/ai/mcp-server.html>
- Documentação: <https://scrapling.readthedocs.io/en/latest/>
