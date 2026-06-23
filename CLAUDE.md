# CLAUDE.md — Orientação do Projeto Analise-Claude

> Este arquivo é lido automaticamente pelo Claude Code ao abrir o repositório.
> Objetivo: me dar todo o contexto para eu performar sem precisar reexplicar.

## Identidade do projeto

- **Empresa:** Hospitalar Soluções em Saúde
- **Proprietário:** Rudson Antonio Ribeiro Oliveira (CEO) — +55 35 99835-2323 — rud.pa@hotmail.com
- **Repositório:** memória/estado do projeto de automação (não é código de aplicação)
- **Idioma:** sempre responder em **português do Brasil**.

## Procedimento de retomada (FAÇA PRIMEIRO)

1. Leia **`BASE_CONHECIMENTO.md`** (o "oráculo" — contexto COMPLETO e autossuficiente).
2. Leia **`CONTEXTO.json`** (estado estruturado, máquina-legível).
3. Leia **`README.md`** (contexto humano) e este `CLAUDE.md`.
4. Resuma para o Rudson: estado atual, pendências e próximo passo. Confirme se consegue
   acessar o n8n via MCP (`n8n-cloud` ✅; `n8n-local` só se houver túnel/Claude local).
5. **Ao terminar qualquer mudança relevante, ATUALIZE `CONTEXTO.json` e `BASE_CONHECIMENTO.md`**
   (incremente `meta.versao` e `meta.data_analise`) e o README quando fizer sentido.

> ⚠️ **Barreira-chave (não esqueça):** o Claude da sessão web roda num servidor remoto e
> **não alcança o PC do Rudson** nem o n8n local (`localhost`). Alcança o **Cloud** via MCP.
> Para o local: Claude Code no PC dele OU Cloudflare Tunnel. Detalhes no oráculo.

## Arquitetura (modelo híbrido)

- **N8N Cloud** (`https://rudsonoliveira2323.app.n8n.cloud`) — produção: webhooks
  sempre-online (COCKPIT-07, COCKPIT-08 cron 07h, COCKPIT-05 polling Notion→WhatsApp).
- **N8N Local** (Docker, no **PC** do Rudson) — dev/testes e workflows pesados
  (Whisper, scraping), para não gastar execuções do Cloud. Guia: `N8N_LOCAL_INSTALL.md`.
- **Roteamento Cloud↔Local:** `WF-ORQUESTRADOR-DINAMICO` (lê `AGENTE_LOCAL` no
  staticData) + `WF-MCC-SET-URL` (registra a URL do túnel).
- **Túnel:** Cloudflare Tunnel (gratuito, URL fixa) com 2 réplicas para HA; ngrok
  como caminho DR/debug. ngrok pago **não** é necessário.
- **Stack:** N8N + OpenRouter + Evolution API + Notion + Google Sheets + Outlook.

## Como eu interajo com o n8n (n8n-mcp)

- Servidores MCP configurados em `.mcp.json`: **`n8n-local`** e **`n8n-cloud`**
  (ambos via `npx n8n-mcp`, autenticando com `N8N_*_API_KEY` do ambiente).
- Use-os para **listar, criar, editar, validar e ativar** workflows por conversa.
- Setup no Windows: rode `scripts\Connect-N8nClaude.ps1` (configura chaves, valida
  conexão e imprime o prompt de retomada).

## Pendências técnicas (ver detalhes no CONTEXTO.json)

| Item | Prioridade |
|---|---|
| `OPENAI_API_KEY` (Whisper — transcrição de áudio WhatsApp) | 🔴 Alta |
| `EVOLUTION_API_KEY` (menu WhatsApp 1=Manter/2=Dormir/3=Excluir) | 🔴 Alta |
| Teste end-to-end do subfluxo de áudio WhatsApp | 🟡 Média |
| Subir N8N local (Docker) + conectar n8n-mcp | 🟡 Média |
| Supabase com credenciais hardcoded (telegram-scraper-inema) | 🟢 Baixa |

## Convenções

- **Commits:** mensagens claras e descritivas em português; uma mudança lógica por commit.
- **Branch de trabalho:** `claude/n8n-local-install-xltfsv` (não fazer push em outras sem permissão).
- **Segredos:** nunca commitar API keys. Use variáveis de ambiente (`.env`/escopo do
  usuário); o `.mcp.json` referencia `${VAR}` e é seguro versionar.
- **Erros já resolvidos** estão catalogados em `CONTEXTO.json` (`erros_corrigidos_historico`) —
  consulte antes de rediagnosticar (ex.: usar PATCH e não PUT; `specifyBody` string vs json).

## Como me dar a melhor performance (orientação do Rudson)

- Quando pedir algo do n8n, eu já tenho contexto — não preciso reexplicar a empresa/stack.
- Diga o **objetivo** (o "para quê"), que eu escolho os nós/abordagem e valido com o n8n-mcp.
- Se algo for ambíguo ou arriscado (mexer em produção), eu pergunto antes de agir.
