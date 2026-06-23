<!--
  ╔══════════════════════════════════════════════════════════════════════╗
  ║  ORÁCULO — Base de Conhecimento Completa do Projeto                   ║
  ║  Hospitalar Soluções em Saúde · Automação multicanal                 ║
  ║  Leia este arquivo + CONTEXTO.json para ter contexto TOTAL.          ║
  ╚══════════════════════════════════════════════════════════════════════╝
-->

# 🔮 ORÁCULO — Base de Conhecimento Completa

> **Para qualquer agente (Claude ou outro) que abrir esta conversa/repositório:**
> este documento é um *handoff* completo. Lendo **só este arquivo + `CONTEXTO.json`**
> você passa a saber tudo sobre o projeto e pode continuar o trabalho sem que o
> proprietário precise reexplicar nada. Trate-o como a memória de longo prazo do projeto.

- **Versão do Oráculo:** 1.0 · **Última atualização:** 21/06/2026 · **Por:** Claude Opus 4.8
- **Fonte da verdade estruturada:** [`CONTEXTO.json`](./CONTEXTO.json) (v4.3) — em caso de divergência, o JSON vence para dados; este Oráculo vence para *narrativa/explicação*.

---

## 0. 🚀 Prompt de Bootstrap (copie e cole em qualquer agente novo)

> Use isto para iniciar uma conversa nova já contextualizada — em **qualquer** agente/canal:

```
Você é o agente de automação do projeto da Hospitalar Soluções em Saúde.
Antes de qualquer coisa, leia no repositório GitHub Rudson-Oliveira/Analise-Claude:
1) ORACULO.md (base de conhecimento completa)
2) CONTEXTO.json (estado estruturado, fonte da verdade)
3) O checkpoint mais recente (CHECKPOINT_*.md), se houver.
Depois, confirme em 3 linhas o estado atual (workflows ativos, pendências,
próximo passo) e só então proponha/execute a próxima ação.
Responda sempre em português (BR). Nunca exponha segredos/API keys.
Prefira agir pelas ferramentas (n8n MCP, GitHub MCP, MarkItDown MCP) antes de
pedir algo manual. Trabalhe em branch + PR em rascunho; nunca commite na main sem permissão.
```

---

## 1. 🪪 Identidade do projeto

| Campo | Valor |
|---|---|
| Empresa | **Hospitalar Soluções em Saúde** |
| Proprietário | Rudson Antonio Ribeiro Oliveira (CEO) |
| Contato | +55 35 99835-2323 · rud.pa@hotmail.com |
| Repositório | https://github.com/Rudson-Oliveira/Analise-Claude |
| n8n Cloud | https://rudsonoliveira2323.app.n8n.cloud |
| Evolution API | https://evolution-api-production-a1f9.up.railway.app |
| Idioma | **Português (BR)** sempre |

---

## 2. 🧭 O que é este repositório

Este repo **não contém código de aplicação**. Ele é a **memória / contexto** do projeto de
automação. O trabalho "real" (workflows) roda no **n8n Cloud**; aqui ficam os checkpoints,
o estado estruturado e o histórico de decisões para **retomar qualquer sessão sem perder contexto**.

**Hierarquia de leitura (ordem recomendada):**
1. `ORACULO.md` (este arquivo) — narrativa completa.
2. `CONTEXTO.json` — estado estruturado/máquina-legível (**fonte da verdade dos dados**).
3. `README.md` — visão humana resumida.
4. `CHECKPOINT_*.md` — fotos datadas de sessões.
5. Docs específicas: `INTEGRACAO_*.md`, `ANALISE_COMPLETA.md`, `PROGRESSO_FASE1.md`.

---

## 3. 🧠 Arquitetura do ecossistema — multicanal "canivete suíço"

**Princípio-mestre:** **não travar em um único canal.** Um cérebro de IA (Claude) acionável de
**qualquer canal** de entrada e que devolve resultado em **qualquer canal** de saída. O n8n é
**um** dos orquestradores — não o dono exclusivo.

```
        CANAIS DE ENTRADA              RUNTIME (cérebro+mãos)         CANAIS DE SAÍDA
   ┌───────────────────────┐                                   ┌───────────────────────┐
   │ WhatsApp (Evolution)  │      ┌────────────────────┐       │ WhatsApp (Evolution)  │
   │ Email (Outlook)       │      │  CLAUDE            │       │ Email (Outlook)       │
   │ Notion                │ ───▶ │  • via OpenRouter   │ ───▶ │ Notion                │
   │ Telegram              │      │    (dentro do n8n)  │       │ Google Sheets         │
   │ Google Sheets         │      │  • Managed Agents   │       │ Telegram              │
   │ Webhook / API direta  │      │    (tarefas longas) │       │ App / Webhook / API   │
   │ Claude Code (MCP)     │      └────────────────────┘       │ Claude Code (MCP)     │
   └───────────────────────┘                                   └───────────────────────┘
                        Orquestração plugável: n8n · API direta · MCP
```

**Três formas de acionar (escolher por caso, sem amarrar):**
1. **Via n8n** — triggers (cron, webhook, email, Notion) → HTTP Request → IA → distribui nos canais.
2. **API direta** — um canal/serviço (app, microserviço Railway) chama a IA sem passar pelo n8n.
3. **Via MCP** — agente Claude (Code/Desktop) usa o runtime sob demanda.

---

## 4. 🧱 Stack e contas

| Camada | Ferramenta | Papel |
|---|---|---|
| Orquestração | **n8n Cloud** | Workflows COCKPIT-* e WF-*; triggers, cron, webhooks, integrações |
| Modelos de IA | **Claude via OpenRouter** | Cérebro (ex.: `anthropic/claude-haiku-4-5`); preferir Claude mais recente |
| Mensageria | **Evolution API** | WhatsApp (envio/recebimento, menu 1/2/3) |
| Conhecimento | **Notion** | Base de cards/inbox |
| Planilhas | **Google Sheets** | Dados estruturados, set de URLs |
| Email | **Microsoft Outlook** | Triagem de email |
| Conversão | **MarkItDown-MCP** | Arquivos → Markdown limpo p/ LLM (avaliado) |
| Runtime longo | **Claude Managed Agents** | Agentes autônomos de horas (avaliado) |

---

## 5. ⚙️ Workflows (COCKPIT / WF) — estado atual

| Workflow | ID | Modelo | Status |
|---|---|---|---|
| COCKPIT-07 · Inbox WhatsApp/Email/Notion (triagem IA) | `acWQbkOkisdpzryy` | `google/gemini-2.5-flash-preview` | ✅ Ativo (corrigido sessão 4) |
| COCKPIT-08 · Briefing diário 07h (WhatsApp+Email) | `CoDTbFiy8g1ctkmO` | `anthropic/claude-haiku-4-5` | ✅ Ativo (cron) · exec #21415 SUCCESS |
| COCKPIT-09 · Helper texto projeto+confiança | `ZQLHgsgDppId9qoe` | N/A | ⏭️ Sem lógica IA (só trigger+code) |
| COCKPIT-05 · Polling Notion→WhatsApp | — | — | ✅ Ativo |
| WF-ORQUESTRADOR-DINÂMICO | — | — | ✅ Ativo · exec #21404 SUCCESS |
| WF-MCC-SET-URL | — | — | ✅ Ativo (testado via Sheets) |
| COCKPIT-07 · node 7 alerta URGENTE WhatsApp | — | — | ⚠️ Falta `EVOLUTION_API_KEY` |
| WF-TRIAGEM-EMAIL Outlook | — | — | ❌ Erro de autenticação |

---

## 6. 🔑 Variáveis e segredos (n8n)

| Variável | Status | Para quê |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ Configurado | Modelos Claude via OpenRouter |
| `OPENAI_API_KEY` | ❌ Pendente | Whisper — transcrição de áudio WhatsApp |
| `EVOLUTION_API_KEY` | ❌ Pendente | Menu WhatsApp (1=Manter / 2=Dormir / 3=Excluir) |
| `ANTHROPIC_API_KEY` | 🔵 Futuro | Necessária para ativar o Managed Agents (API direta) |

> 🔒 **Nunca** commitar valores reais. Usar placeholders e variáveis de ambiente n8n.

---

## 7. 🧩 Integrações avaliadas

### MarkItDown-MCP (Microsoft, open-source) — 📋 Documentado
Converte PDF/Word/Excel/PPT/imagem/áudio/HTML → Markdown limpo. Ferramenta MCP:
`convert_to_markdown(uri)`. Roda **local** (STDIO/Docker), serve ao agente Claude — não conecta
direto ao n8n Cloud. Encaixe: pré-processar anexos no COCKPIT-07 antes da IA. Doc: `INTEGRACAO_MARKITDOWN_MCP.md`. Já existe `.mcp.json` na raiz com o servidor `markitdown`.

### Claude Managed Agents (Anthropic) — 📋 Avaliado (sem ativação imediata)
Runtime gerenciado da Anthropic para agentes autônomos de longa duração ("desacoplar o cérebro
das mãos"). Beta público 08/04/2026. Preço: tokens + **US$ 0,08/hora-sessão**. Acesso via **API
Claude** (exige `ANTHROPIC_API_KEY`, **não** via OpenRouter). Posicionado como **runtime
multicanal** (ver seção 3). Doc: `INTEGRACAO_CLAUDE_MANAGED_AGENTS.md`.

---

## 8. 🖥️ Frontend (painel visual)

- Arquivo: `frontend/index.html` — HTML autocontido, sem dependências.
- Mostra: hero, stats, **diagrama multicanal interativo**, integrações, tabela de workflows, status das variáveis.
- Publicação: GitHub Actions (`.github/workflows/deploy-pages.yml`) publica `frontend/` no GitHub Pages a cada push na `main`. Ligar uma vez em **Settings → Pages → Source: GitHub Actions**.
- URL futura: `https://rudson-oliveira.github.io/Analise-Claude/`.

---

## 9. ⚠️ Armadilhas a NÃO repetir (lições n8n já aprendidas)

| Erro | Causa | ✅ Fix |
|---|---|---|
| `PUT /rest/workflows` → 404 (HTML) | Endpoint errado | Usar **PATCH** em `/rest/workflows/:id` |
| Rename de node quebra conexões | n8n liga nodes por nome | **Não renomear** node — mudar só os parâmetros |
| `activate` → 400 "versionId required" | Falta versionId | Buscar o workflow, extrair `versionId`, passar no body do activate |
| HTTP Request: JSON syntax error (pos. 593) | `specifyBody: "json"` não aceita `{{ $json.x }}` | Usar **`specifyBody: "string"`** quando houver expressões n8n |
| Modelo de IA desatualizado | — | Preferir Claude mais recente (ex.: `anthropic/claude-haiku-4-5`) via OpenRouter |

---

## 10. 🧰 Ferramentas / MCP disponíveis (use antes de pedir algo manual)

- **n8n (MCP oficial):** buscar/criar/editar/validar/ativar workflows no n8n Cloud. Fluxo: ler SDK → sugerir nodes → validar node a node → validar workflow → criar.
- **GitHub (MCP):** PRs, issues, CI, comentários no repo `Rudson-Oliveira/Analise-Claude`.
- **MarkItDown (MCP, local):** `convert_to_markdown(uri)`.
- **Microsoft Learn / docs:** documentação oficial Microsoft/Azure/Outlook.

> Antes de dizer "não tenho acesso", **procure a ferramenta** — muitos MCPs carregam sob demanda.

---

## 11. 🗓️ Histórico de sessões (linha do tempo)

| Sessão | Data | Conquistas-chave |
|---|---|---|
| **1** | — | Análise de 50+ workflows; mapeamento de integrações; `CONTEXTO.json` v1.0 + README inicial |
| **2** | — | `AGENTE_LOCAL` registrado no WF-ORQUESTRADOR-DINAMICO; WF-MCC-SET-URL testado via Sheets; orquestrador end-to-end (exec #21404 SUCCESS) |
| **3** | 31/05/2026 | `OPENROUTER_API_KEY` global; COCKPIT-07 e COCKPIT-08 migrados HuggingFace→OpenRouter; lições PATCH/rename/versionId |
| **4** | 31/05/2026 | Corrigido JSON syntax COCKPIT-07 (`specifyBody` json→string); reativado e testado (exec #21422 SUCCESS); identificado node 7 dependente de `EVOLUTION_API_KEY` |
| **5** | 15/06/2026 | Integração **MarkItDown-MCP** documentada; `.mcp.json` criado; CONTEXTO v4.1 |
| **6** | 21/06/2026 | **Claude Managed Agents** avaliado e posicionado como **runtime multicanal**; **frontend visual** criado; deploy GitHub Pages; **ORÁCULO** (este doc); CONTEXTO v4.3 |

---

## 12. 📋 Pendências e próximos passos (roadmap — Fase 2)

1. 🔴 Configurar `OPENAI_API_KEY` (Whisper — transcrição de áudio WhatsApp).
2. 🔴 Configurar `EVOLUTION_API_KEY` (menu WhatsApp 1/2/3; destrava node 7 do COCKPIT-07).
3. 🟡 Testar subfluxo de áudio WhatsApp: `áudio → Whisper → OpenRouter → resposta`.
4. 🟡 Configurar MarkItDown-MCP no cliente Claude e testar conversão de anexo real.
5. 🟢 Corrigir auth do WF-TRIAGEM-EMAIL (Outlook).
6. 🟢 Supabase: remover credenciais hardcoded do `telegram-scraper-inema-n8n`.
7. 🔵 (Futuro) Ativar Managed Agents quando houver tarefa autônoma longa — provisionar `ANTHROPIC_API_KEY`.
8. 🔵 (Melhoria) Tornar o frontend **dinâmico** (ler `CONTEXTO.json` via `fetch()`).

---

## 13. 📐 Convenções

- **Idioma:** PT-BR em respostas, commits e PRs.
- **Git:** desenvolver em branch de trabalho; **nunca** commitar na `main` sem permissão; push `git push -u origin <branch>` com retry/backoff (2s/4s/8s/16s); após push, **abrir PR em rascunho**.
- **Segredos:** jamais no histórico — placeholders + variáveis de ambiente.
- **Saúde do projeto:** ao terminar mudanças relevantes, **bump** do `CONTEXTO.json`, atualizar `README.md` e este `ORACULO.md`, e registrar checkpoint se a sessão foi grande.

---

## 14. 📖 Glossário

- **COCKPIT-*** — workflows n8n "de produção" (inbox, briefing, polling).
- **WF-*** — workflows utilitários/orquestração.
- **Canivete suíço** — filosofia multicanal: uma capacidade plugável em qualquer canal, sem travar.
- **Runtime** — onde o agente executa (n8n nodes, ou o sandbox do Managed Agents).
- **MCP** — Model Context Protocol; servidores que dão ferramentas ao agente (n8n, GitHub, MarkItDown).
- **OpenRouter** — gateway para chamar modelos (Claude etc.) de forma unificada.

---

## 15. 🗂️ Snapshot JSON (para agentes não-Claude / parsing rápido)

```json
{
  "projeto": "Hospitalar Soluções em Saúde - automação multicanal",
  "proprietario": "Rudson Antonio Ribeiro Oliveira",
  "repo": "Rudson-Oliveira/Analise-Claude",
  "n8n": "https://rudsonoliveira2323.app.n8n.cloud",
  "principio": "multicanal canivete suico - nao travar em um canal",
  "ia": {"cerebro": "Claude via OpenRouter", "runtime_longo": "Claude Managed Agents (avaliado)"},
  "canais": ["WhatsApp","Email/Outlook","Notion","Telegram","Google Sheets","Webhook/API","MCP"],
  "workflows_ativos": ["COCKPIT-07","COCKPIT-08","COCKPIT-05","WF-ORQUESTRADOR-DINAMICO","WF-MCC-SET-URL"],
  "variaveis": {"OPENROUTER_API_KEY":"ok","OPENAI_API_KEY":"pendente","EVOLUTION_API_KEY":"pendente","ANTHROPIC_API_KEY":"futuro"},
  "fonte_da_verdade": "CONTEXTO.json (v4.3)",
  "frontend": "frontend/index.html (GitHub Pages)",
  "proximo_passo": "Configurar OPENAI_API_KEY e EVOLUTION_API_KEY (Fase 2)"
}
```

---

> **Fim do Oráculo.** Mantenha-o vivo: ao concluir mudanças relevantes, atualize a seção 11
> (histórico), 12 (roadmap) e o cabeçalho (versão/data). Um oráculo desatualizado engana o próximo agente.
