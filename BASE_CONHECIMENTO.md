# 🔮 BASE DE CONHECIMENTO (ORÁCULO) — Projeto Analise-Claude

> **Propósito deste arquivo:** ser a **fonte única e completa de contexto** do projeto.
> Qualquer agente Claude (em qualquer conversa, no PC do Rudson, na web, ou outro)
> que leia **este arquivo + `CONTEXTO.json`** deve entender 100% da situação e
> continuar o trabalho **sem precisar reexplicar nada**.
>
> **Como usar (prompt de retomada sugerido):**
> *"Leia BASE_CONHECIMENTO.md e CONTEXTO.json do repositório Analise-Claude e me dê
> o estado atual, pendências e próximo passo. Confirme se consegue acessar meu n8n
> via MCP."*
>
> **Última atualização:** 2026-06-16 · mantenha esta data e a versão do CONTEXTO.json sincronizadas.

---

## 1. Quem é o Rudson e qual o objetivo

- **Pessoa:** Rudson Antonio Ribeiro Oliveira — CEO da **Hospitalar Soluções em Saúde**.
- **Contato:** +55 35 99835-2323 · rud.pa@hotmail.com
- **Idioma:** responder **sempre em português do Brasil**, tom prático e acessível
  (o Rudson não é desenvolvedor; explicar passo a passo, sem jargão desnecessário).
- **Objetivo macro:** ter um ecossistema de automação com **n8n + IA** para a empresa,
  reduzindo custos e permitindo que o **Claude opere/construa workflows por conversa**.
- **Objetivo que disparou esta fase:** instalar **n8n local** para economizar (não gastar
  execuções do plano Cloud) **mantendo o plano básico Cloud**, e ainda assim interagir
  com o Claude. → **Viável: modelo híbrido.** (Confirmado e em execução.)

---

## 2. ⚠️ A barreira técnica MAIS IMPORTANTE (entenda antes de qualquer coisa)

**O Claude da sessão web/remota NÃO tem acesso ao computador do Rudson.**

- Esta instância roda num **contêiner Ubuntu Linux na nuvem da Anthropic** (provado:
  `uname` → Linux; `whoami` → root; máquina `vm`; `powershell.exe` não existe).
- Logo, **não dá para instalar nem rodar nada no Windows do Rudson a partir daqui.**
  Comandos de instalação têm que ser **colados por ele** no PowerShell dele.
- O MCP **`n8n-local`** aponta para `localhost:5678` — mas esse "localhost" é o do
  **servidor remoto**, não o PC dele (deu `SSRF: localhost blocked`). Ou seja, **a sessão
  web NÃO alcança o n8n local do Rudson.**
- O MCP **`n8n-cloud`** ✅ **funciona** (health check OK) — a sessão web **consegue**
  operar o n8n **Cloud** dele.

**Como um agente Claude consegue mexer no n8n LOCAL do Rudson:**
1. **Claude Code rodando no PC dele** (app/CLI local) — aí sim tem acesso ao PowerShell e ao `localhost`.
2. **OU** expor o PC via **Cloudflare Tunnel** e apontar o MCP `n8n-local` para a URL pública.

> Regra de ouro ao ajudar: **seja honesto sobre o que você alcança.** Se for tarefa no PC,
> guie o Rudson a colar comandos; não prometa "eu instalo aí".

---

## 3. Arquitetura (modelo híbrido)

| Camada | Onde | Papel |
|---|---|---|
| **N8N Cloud** (`https://rudsonoliveira2323.app.n8n.cloud`) | nuvem (plano básico) | Produção: webhooks sempre-online (COCKPIT-07, COCKPIT-08 cron 07h, COCKPIT-05 polling Notion→WhatsApp). **70 workflows.** |
| **N8N Local** | PC Windows do Rudson | Dev/testes e workflows pesados (Whisper, scraping) para não gastar execuções do Cloud. **4 workflows.** |
| **Roteamento** | — | `WF-ORQUESTRADOR-DINAMICO` (lê `AGENTE_LOCAL` no staticData) + `WF-MCC-SET-URL` (registra URL do túnel). |
| **Túnel (futuro)** | — | **Cloudflare Tunnel** (grátis, URL fixa) — decisão tomada. **ngrok pago foi descartado.** |
| **Stack** | — | n8n + OpenRouter + Evolution API + Notion + Google Sheets + Outlook + Supabase. |

---

## 4. Estado ATUAL do n8n LOCAL (no PC do Rudson) — junho/2026

- **Instalação:** **nativa, SEM Docker** (preferência explícita do Rudson). Feita com
  `npm install n8n` e iniciada com **`npx n8n`** no PowerShell. Node.js LTS instalado.
- **Acesso:** http://localhost:5678
- **Dado importante:** o `~/.n8n` do PC **já tinha um banco de dados de julho/2025** —
  por isso, ao subir, já apareceram workflows e uma conta de dono antiga (não era do zero).
- **Conta de dono:** foi feito **reset** (`npx n8n user-management:reset`) e recriada
  (login com rud.pa@hotmail.com). Workflows foram preservados.
- **Workflows locais (4, criados 18/07/2025):**
  - `My workflow`
  - **`Agente de Marketing`** (Published) — usa o nó community **`n8n-nodes-evolution-api`**
  - `Sistema Multiagentes`
- **Erro recorrente no terminal:** `Unrecognized node type: n8n-nodes-evolution-api.evolutionApi`
  → o nó community **ainda não está instalado** nesta instância. Por isso o "Agente de
  Marketing" fica em loop de retry de ativação. **Não é erro fatal** — o n8n roda normal.
- **Comportamento que confunde o Rudson:** rodando com `npx n8n`, **o n8n só fica no ar
  enquanto a janela do PowerShell estiver aberta**. Fechou/Ctrl+C → `ERR_CONNECTION_REFUSED`
  no navegador. Solução definitiva pendente: **PM2** para autostart (ver §7).

### Pendências imediatas do local
1. **Gerar API Key** (Settings → n8n API → Create an API key) — necessária para o n8n-mcp.
2. **Instalar o nó** `n8n-nodes-evolution-api` (Settings → Community Nodes → Install) → resolve o erro e ativa o "Agente de Marketing".
3. **Autostart com PM2** para não cair quando fechar a janela.

---

## 5. Estado ATUAL do n8n CLOUD — 🔴 ALERTA

- **70 workflows**, mas o painel mostra **Failure rate 100%** com **3.162 execuções
  falhando**. Isso indica que **a automação de produção está quebrada** — provavelmente
  o item mais urgente do projeto.
- A sessão web **consegue investigar isso agora** via MCP `n8n-cloud` (health check OK).
- **Próxima ação recomendada:** listar workflows do Cloud, abrir execuções com erro
  (`n8n_executions` action=list status=error) e diagnosticar a causa raiz.
- Workflows notáveis vistos no Cloud: `22-INFRA-LlamaIndex-Gateway - RAG e Orcamentos`,
  `HospitaLar-Intel-Dispatcher (Webhook: eventos do Intel)`, `intel-Hospitalar - Publicação Social com IA`.

---

## 6. Como o Claude se conecta ao n8n (n8n-mcp)

- Ferramenta: **n8n-mcp** (repo `czlonkowski/n8n-mcp`) — dá ao Claude conhecimento de
  1.800+ nós **e** conecta na API do n8n para **listar/criar/editar/validar/ativar** workflows.
- Config versionada em **`.mcp.json`** (na raiz do repo): dois servidores, `n8n-local` e
  `n8n-cloud`, via `npx n8n-mcp`, autenticando com `N8N_*_API_KEY` (variáveis de ambiente,
  expandidas com `${VAR}` — sem segredos no git).
- Script de conexão para Windows: **`scripts/Connect-N8nClaude.ps1`** (configura chaves,
  valida e imprime o prompt de retomada).
- Instalador nativo do n8n no Windows: **`scripts/Install-N8nNative.ps1`**.
- Quickstart Docker (caso um dia queira): **`n8n-local/docker-compose.yml`** (não usado agora).

---

## 7. Decisões já tomadas (NÃO reabrir sem motivo)

| Tema | Decisão | Motivo |
|---|---|---|
| Modelo | **Híbrido** (Cloud básico + Local) | Economia sem perder produção |
| Container | **SEM Docker** | Preferência do Rudson |
| Instalação local | **Nativa (npm/npx) no Windows** | Sem Docker |
| Túnel | **Cloudflare Tunnel** (grátis, URL fixa) | ngrok pago é custo recorrente desnecessário |
| ngrok pago | **Descartado** | Cloudflare faz o mesmo de graça; ngrok free só p/ debug |
| Docker Pro | **Não assinar** | Sem benefício para o caso |
| Ambiente local | **PC** (com VPS como destino futuro p/ 24/7) | Começar barato |
| Autostart | **PM2** (a implementar) | n8n via `npx` cai ao fechar a janela |

---

## 8. Pendências técnicas (visão completa)

| Item | Prioridade | Detalhe |
|---|---|---|
| 🔴 Cloud com **100% de falha** | **CRÍTICA** | Investigar execuções com erro no Cloud (MCP já alcança) |
| Instalar nó `n8n-nodes-evolution-api` no local | Alta | Resolve erro e ativa "Agente de Marketing" |
| Gerar API Key local + conectar n8n-mcp | Alta | Para o Claude operar o local |
| `OPENAI_API_KEY` (Whisper – áudio WhatsApp) | Alta | Pendente desde sessões anteriores |
| `EVOLUTION_API_KEY` (menu WhatsApp 1/2/3) | Alta | Pendente desde sessões anteriores |
| PM2 para manter o n8n local no ar | Média | Evita o `ERR_CONNECTION_REFUSED` ao fechar janela |
| Cloudflare Tunnel (URL fixa do local) | Média | Para webhooks externos e para o Claude alcançar o local |
| Teste e2e do subfluxo de áudio WhatsApp | Média | audio→Whisper→OpenRouter |
| Supabase com credenciais hardcoded | Baixa | telegram-scraper-inema |

---

## 9. Erros já resolvidos / armadilhas conhecidas (consulte antes de rediagnosticar)

- **PUT /rest/workflows → 404:** usar **PATCH**, não PUT.
- **activate → 400 versionId required:** buscar workflow, extrair `versionId`, passar no body.
- **PATCH com rename de node quebrava conexões:** manter o nome original do node.
- **JSON syntax error position 593 (COCKPIT-07):** `specifyBody: "json"` não aceita
  expressões n8n `{{ }}` → trocar para `"string"`.
- **`npm warn deprecated` na instalação:** são **avisos**, não erros. Ignorar.
- **`401 Wrong username or password` no login local:** a instância já tinha conta antiga;
  resolver com `npx n8n user-management:reset`.
- **`ERR_CONNECTION_REFUSED` em localhost:5678:** o n8n parou (janela fechada/Ctrl+C);
  religar com `npx n8n`.
- **`Unrecognized node type`:** falta instalar o nó community correspondente.

---

## 10. Convenções do projeto

- **Commits:** claros, em português, uma mudança lógica por commit.
- **Branch de trabalho:** `claude/n8n-local-install-xltfsv` (não fazer push em outras sem permissão).
- **Segredos:** **NUNCA** commitar API keys/senhas. Usar variáveis de ambiente; `.mcp.json`
  referencia `${VAR}`. **Nunca pedir/repetir senha no chat** (o Rudson já colou uma senha
  uma vez — orientá-lo a trocar e não repetir).
- **Ao terminar mudança relevante:** atualizar `CONTEXTO.json` (incrementar `meta.versao` e
  `meta.data_analise`) e **este arquivo** quando o estado mudar.
- **Documentos do repo:** `N8N_LOCAL_INSTALL.md` (guia híbrido + HA), `CLAUDE.md`
  (orientação curta auto-lida), `CONTEXTO.json` (estado estruturado), e este oráculo.

---

## 11. Próximo passo recomendado (quando retomar)

1. **Religar o n8n local** se estiver fora (`npx n8n`) e instalar o nó da Evolution API.
2. **Gerar a API Key local** e conectar o n8n-mcp (via Claude Code local).
3. **Investigar o Cloud falhando 100%** — provavelmente o de maior impacto; a sessão web
   já consegue fazer isso via MCP `n8n-cloud`.
4. Configurar **PM2** (autostart) e, depois, **Cloudflare Tunnel** (URL fixa).

> Sempre que ajudar o Rudson num passo no PC dele: instruções **curtas, numeradas,
> copiar-e-colar**, e peça o **print/saída** de volta para confirmar antes de seguir.
