# 🔮 ORÁCULO — Base de Conhecimento Completa

> **O que é este arquivo:** a **memória única e canônica** do projeto de automação da
> **Hospitalar Soluções em Saúde**. Foi escrito para ser o "cérebro" que qualquer agente
> (Claude ou outro) lê **uma vez** e passa a **saber de tudo** — estado, histórico, IDs,
> convenções e próximos passos — sem precisar reconstruir o contexto.
>
> **Mantido por:** sessões Claude Code (web/CLI). **Última consolidação:** 23/06/2026 · Sessão 7 · Claude Opus 4.8.
> **Fonte da verdade estruturada:** [`CONTEXTO.json`](./CONTEXTO.json). Em caso de divergência, o `CONTEXTO.json` (versão mais alta) vence; este oráculo é a leitura humana completa.

---

## 🧭 PROTOCOLO DE HANDOFF (como um agente "se conecta" a este conhecimento)

Para iniciar **qualquer** nova conversa já sabendo de tudo, cole este prompt:

```
Você está no projeto Analise-Claude (memória do sistema de automação n8n da
Hospitalar Soluções em Saúde). Leia, nesta ordem: ORACULO.md (base completa),
CONTEXTO.json (estado estruturado / fonte da verdade) e o CHECKPOINT_*.md mais
recente. Depois me dê um resumo de 6-8 linhas com: estado atual, workflows
ativos, pendências de maior prioridade e o próximo passo recomendado. Responda
em PT-BR. Não repita erros já documentados na seção "Convenções técnicas".
```

Ou, no terminal, rode o bootstrap: `scripts/iniciar-claude.ps1` (instala o Claude Code,
clona o repo e abre a sessão já contextualizada).

---

## ⚡ FATOS RÁPIDOS (quick facts)

| Campo | Valor |
|---|---|
| **Empresa** | Hospitalar Soluções em Saúde |
| **Proprietário / CEO** | Rudson Antonio Ribeiro Oliveira |
| **Contato** | +55 35 99835-2323 · rud.pa@hotmail.com |
| **n8n Cloud** | https://rudsonoliveira2323.app.n8n.cloud · versão `n8n@2.21.8` · TZ `America/Sao_Paulo` |
| **Plano n8n** | 10.000 execuções/mês (upgrade feito na Sessão 4; era Free 2.500) |
| **Repo (memória)** | https://github.com/Rudson-Oliveira/Analise-Claude |
| **Stack núcleo** | n8n Cloud + OpenRouter + Evolution API + Notion + Google Sheets + Microsoft Outlook |
| **Cérebro IA** | Modelos Claude (preferir os mais recentes) via **OpenRouter** |
| **Frontend** | HospitaLar Intel (Manus) · `frontend/index.html` neste repo · painel multicanal |
| **Filosofia** | "Canivete suíço" multicanal — **não travar em um único canal/orquestrador** |

---

## 🎯 MISSÃO E NATUREZA DO PROJETO

Este repositório **não tem código de aplicação**: é a **memória/contexto** do projeto. O trabalho
real acontece no **n8n Cloud** (e em sistemas satélites). Aqui ficam checkpoints, estado estruturado
e histórico de decisões para **retomar qualquer sessão sem perder contexto**.

O sistema da Hospitalar é um **ecossistema de automação multicanal** que cobre: captação e triagem de
mensagens (WhatsApp/Email/Telegram/Notion), criação de conteúdo com IA, funil de vendas (CRM 7 níveis),
orçamentos, briefings diários e um painel de inteligência (HospitaLar Intel).

**Princípio diretor ("canivete suíço"):** qualquer capacidade deve poder ser **acionada de qualquer
canal** e **devolver resultado em qualquer canal**. O n8n é **um** dos orquestradores possíveis — não o dono exclusivo.

---

## 🏗️ ARQUITETURA GERAL

```
┌──────────────────────── CANAIS DE ENTRADA ────────────────────────┐
│ WhatsApp (Evolution API) · Email (Outlook) · Telegram · Notion ·   │
│ Google Sheets · Webhooks · Sistema Hospitalar/e63 · Claude (MCP)   │
└───────────────┬────────────────────────────────────────────────────┘
                ▼
┌──────────────────────── ORQUESTRAÇÃO ──────────────────────────────┐
│  n8n CLOUD (rudsonoliveira2323)  ~69 workflows / ~44 ativos         │
│   • INFRA  (triggers, backup/restore, observabilidade, gateway)    │
│   • INT    (scrapers, bridges, imports, triagem email/whats)       │
│   • CORE   (criação de conteúdo, vision, sites)                    │
│   • OP     (assistente, captura, agentes)                          │
│   • MCC / MAS (orquestrador dinâmico multi-agente)                 │
│   • FUNIL  (00→07 agentes de vendas) + Orçamentos                  │
│   • INTEL  (Dispatcher / Proposta / Conteúdo) ⚠️ NÃO ALTERAR        │
│  Cérebro IA: Claude via OpenRouter                                 │
└──────┬───────────────────────────────────┬────────────────────────┘
       ▼                                    ▼
┌──────────────────┐              ┌──────────────────────────────────┐
│ n8n LOCAL (Ollama)│              │ MAKE.COM — 11 cenários (social)  │
│ Docker :5678/:11434│             │ Sheets/Drive → Placid → IG/FB/IN │
│ exige ngrok/túnel │              └──────────────────────────────────┘
└──────────────────┘
       ▼
┌──────────────────────── ARMAZENAMENTO / SAÍDA ─────────────────────┐
│ Supabase (telegram_msgs) · Google Sheets (MCC_CONFIG/PC-GERAL) ·    │
│ GitHub (backup workflows) · Notion · WhatsApp/Email/Telegram (out)  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 OS DOIS GRANDES SISTEMAS

### A) Backend de automação — **n8n Cloud** (núcleo operacional)
Onde vivem os workflows COCKPIT-*, WF-* e a orquestração multi-agente (MCC). É o foco da maioria das sessões.

### B) Frontend — **HospitaLar Intel** (painel de inteligência, feito na plataforma Manus)
- URL auditada: `hospintel-y6rar4gv.manus.space` · versão **v2.0** · **21 módulos**.
- Cópia/representação visual neste repo: **`frontend/index.html`** (HTML autocontido, "canivete suíço").
- Módulos: Dashboard, Auto-Conhecimento/Inteligência Estratégica, NPS, Comm-Hub, Tarefas, Agentes IA,
  Planos Terapêuticos (com OCR), Colaboradores, Setores, **CRM funil 7 níveis**, OKR, CRM-Leads,
  Saúde do Funil, Proposta Comercial, Contratos, Pipeline de Conteúdo, Calendário, Email, Ecossistema
  Digital (IG 5K / FB 10K / LinkedIn 4.3K), Pipeline Automático, Configurações.
- **Auditoria forense (09/06/2026, Sonnet 4.6):** nota geral **3.2/5**. Documento: `SISTEMA_HOSPITALAR_INTEL_09-06-26.md`.
  - Críticos: toast sem auto-dismiss; máscara CPF incompleta na Proposta; spinners infinitos sem empty state (NPS/CRM/Funil).
  - Altos: sidebar sem hamburger (inutilizável < 768px); títulos sem acentuação ("SOLUÇÕES EM SAÚDE"); empty states sem CTA.
  - Projeção com correções: 3.2 → ~4.7.
- **3 workflows n8n do projeto Intel são produção ATIVA — ⚠️ NÃO MODIFICAR sem autorização do Rudson** (ver inventário abaixo).

---

## 📋 INVENTÁRIO DE WORKFLOWS n8n (IDs canônicos)

> Estado consolidado até a Sessão 4 (69 workflows, 44 ativos) + migrações da Sessão 3/4. Os IDs são estáveis — use-os ao chamar a API/MCP.

### 🟦 COCKPIT (triagem/briefing — núcleo IA atual)
| Workflow | ID | Status | Modelo (via OpenRouter) |
|---|---|---|---|
| COCKPIT-07 — Inbox WhatsApp/Email/Notion (Master Triagem) | `acWQbkOkisdpzryy` | ✅ Ativo (corrigido S4) | `google/gemini-2.5-flash-preview` |
| COCKPIT-08 — Briefing Diário (cron 07h) | `CoDTbFiy8g1ctkmO` | ✅ Ativo | `anthropic/claude-haiku-4-5` |
| COCKPIT-09 — Helper Texto Projeto+Confiança | `ZQLHgsgDppId9qoe` | ⏭️ Sem lógica IA (pulado) | N/A |

### 🟩 MCC / Multi-Agente (orquestração)
| Workflow | ID | Webhook / Função |
|---|---|---|
| WF-MCC-SET-URL | `MIo8VUzGX77YJuSq` | `POST /webhook/mcc/set-url` — grava agente no Sheets |
| WF-MCC-GET-URL-GS | `2fuDZ6gYLsRxQM93` | `GET /webhook/mcc/get-url?service_name=X` — lê URL do agente |
| WF-ORQUESTRADOR-DINAMICO | `vZjIt5q0Nh9pRic4` | roteia requisição p/ melhor agente (depende do MCC) |
| WF-ORQUESTRADOR-MULTI-AGENTE | `RREL5BmuDu3HBqcR` | versão multi-agente com fallback |
| WF-HEALTH-CHECK-AGENTES | `9arDgUsepPgKE2K6` | health 5min (falha se Ollama offline) |
| WF-GERENCIADOR-AGENTES | `exkT2c1GtIbNJmxr` | registra agentes |
| WF-INICIALIZADOR-AGENTES | `KGtAUkYFhH9UxLSt` | inicializa agentes |

### 🟨 INFRA
| Workflow | ID |
|---|---|
| 21-INFRA-Backup-GitHub | `QazJlHJIbIfaSfFI` |
| WF-BACKUP-GITHUB (alternativo) | `Qbgwo4yCDqX7QAMy` |
| WF-RESTAURACAO-GITHUB | `WHSdG2ovJPyCnCXL` (`POST /webhook/restaurar-workflow`) |
| 19-INFRA-WF0-Triggers | `MgOrbuP6cWvNwNaE` |
| 18-INFRA-Ollama-Gateway | `oB6o3r4iEMXULyAH` |
| WF-99-Observabilidade-Logs | `BCC5aExZklz2KHTZ` |
| 22-INFRA-AI-Code-Reviewer | `B7BBCjKDX5sGIfGU` |
| 17-INFRA-WF-Master (Orquestrador Equipes) | `Gx6ak7bXif9Zh3Cn` |

### 🟧 INTEGRAÇÕES / OPERAÇÕES
| Workflow | ID |
|---|---|
| 04-CORE-Auto-Import (MySQL) | `LxuhS8681nX9NrB1` |
| 06-INT-Telegram-Import | `mEw1hJz1cJMYMDNe` |
| 07-INT-Telegram-Scraper | `NM89ewNy9WvjsPQ5` |
| 08-INT-e63-Ticketing | `AITTSGpLcImXF3Nt` |
| 09-INT-INEMA-Scraper | `uDHrit1TlBfWUxCh` |
| 05-INT-Webhook-Hospitalar | `33xIKaVlBU1RTI8O` |
| 📧 Triagem Email | `i7f12WgSoAAHraWA` |
| 📱 Triagem WhatsApp | `JiSB5D56uGUTRifp` |
| 01-CORE-INEMA-AI | `5GQFEcl4PqYaPqXr` |
| 02-CORE-Criador-Sites | `YRxqBEDiRd4j22yJ` |
| 03-CORE-Vision-AI | `BRsMiqymKjnnomFr` |
| 14-OP-Assistente-Virtual | `Esi1dNLQtzZGgECL` |
| WF-12-Captura-Formulario-Site | `1QDmhEjBoeYtCCP1` |
| WF-COMET-01-ANALISADOR | `CHB6gdswY4UAQ9gT` |

### 🟥 FUNIL DE VENDAS (00→07) + Orçamentos
`WF-00-Orquestrador-Funil` `lVC4kyju9m0hPFo2` · `WF-01-Prospeccao` `09c0hYoQw6T6KVm8` ·
`WF-02-Qualificacao` `eQRTnUM9CDRnAcAy` · `WF-03-Apresentacao` `AH57c4jXxxwV8ild` ·
`WF-04-Maturacao` `km91d8MWMWqdljv7` · `WF-05-Negociacao` `VFEiDVW51R9gNdQi` ·
`WF-06-Encerramento` `gUqDltSpRoomJ6ge` · `WF-07-Prospeccao-Mercados` `c4WmIUPjX0iH0ktY` ·
`WF-Agente-Orcamentos-Completo` `vigd0lMGWAGZaSRB`.

### ⚠️ INTEL (PROJETO ATIVO — **NÃO ALTERAR sem autorização**)
| Workflow | ID | Webhook |
|---|---|---|
| HospitaLar-Intel-Dispatcher | `UwmGLjOivexhtvV7` | `POST /webhook/hospitalarsaude-intel` |
| Intel-Proposta-Automatica | `CL2CJ91yjqRhPyI7` | `POST /webhook/intel-proposta` |
| Intel-Conteudo-IA | `LkLctxmxWtjbVE8F` | `POST /webhook/intel-conteudo-ia` |

### ❌ Inativos notáveis (motivo)
11-OP-Chatbot `UZaFiDVTYEehjTmq` (só manualTrigger) · 12-OP-Gestor-Agendamentos `tHTuOdVtcsoDadTf` (Postgres+HF) ·
13-OP-Notificacoes `QHdNijZ3JYY2nIK6` (Postgres) · 20-INFRA-WF1-Diagnostico `blTLFKOWd4It5KMB` (DeepSeek+Memory) ·
WF-SIMULADOR-FRONTEND `8AXWxG4OYbCqsI1P` (nodes antigos).

---

## 🔌 ENDPOINTS (webhooks) FUNCIONANDO

| Endpoint | Método | Workflow | Retorno |
|---|---|---|---|
| `/webhook/mcc/set-url` | POST | WF-MCC-SET-URL | `{success, service_name, url}` |
| `/webhook/mcc/get-url?service_name=X` | GET | WF-MCC-GET-URL-GS | `{success, url, description}` |
| `/webhook/restaurar-workflow` | POST | WF-RESTAURACAO-GITHUB | `{success, workflow_id}` |
| `/webhook/hospitalarsaude-intel` | POST | Intel-Dispatcher | `{ok}` |
| `/webhook/intel-proposta` | POST | Intel-Proposta | `{ok}` |
| `/webhook/intel-conteudo-ia` | POST | Intel-Conteudo | `{ok}` |

**MCC_CONFIG (Google Sheets):** planilha `1-rRo3CAb2QunpNJfsAzqYm2lyqmRGsi_nyYnS_FqcDA`, aba `MCC_CONFIG`,
colunas `service_name | url | description | is_active | updated_at`. Entradas atuais: `ORQUESTRADOR`, `AGENTE_LOCAL`.

---

## 🔑 CREDENCIAIS n8n (somente IDs — nunca os segredos)

| Credencial | ID |
|---|---|
| Google Sheets account | `iWwYR5lhrrUABiru` |
| Header Auth (GitHub / N8N API) | `RKtcfFzRmcnJZBgu` |
| Evolution API Rudson (WhatsApp) | `XUO0KTV1AZe2pBXT` |
| OpenAi account | `HKGFp46mQxWxySRb` |

### Variáveis de ambiente n8n
| Variável | Status | Para quê |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ Configurado | Cérebro IA (Claude/Gemini) dos COCKPIT |
| `OPENAI_API_KEY` | ❌ Pendente | Whisper — transcrição de áudio WhatsApp |
| `EVOLUTION_API_KEY` | ❌ Pendente | Menu WhatsApp (1=Manter / 2=Dormir / 3=Excluir) |

---

## ⚙️ CONVENÇÕES TÉCNICAS n8n (lições já aprendidas — **NÃO repetir erros**)

| Tema | Regra de ouro |
|---|---|
| Editar workflow | Use **PATCH** em `/rest/workflows/:id`. **PUT → 404 (HTML)**. |
| Renomear node | **Não renomeie** — mantenha o nome original e altere só os parâmetros (rename quebra conexões). |
| Ativar workflow | Busque o workflow → extraia `versionId` → passe no body do `activate` (senão 400 "versionId required"). |
| HTTP Request com `{{ $json.x }}` | Use `specifyBody: "string"`, **nunca `"json"`** (json puro quebra com erro de sintaxe — caso real: COCKPIT-07 "position 593"). |
| Node `dataTables` | Não disponível em `n8n@2.21.8` → substituir por **Code + Google Sheets (appendOrUpdate)**. |
| Ler Google Sheets em workflow | HTTP Request v4 → `https://sheets.googleapis.com/v4/spreadsheets/{ID}/values/{TAB}!A:E` com `googleSheetsOAuth2Api` (cred `iWwYR5lhrrUABiru`). |
| API n8n | `/rest/` usa cookie de sessão; `/api/v1/` exige `X-N8N-API-KEY`. Endpoints: GET/PATCH `/rest/workflows/:id`, POST `/activate`/`/deactivate`. |
| Health-check sem agentes | Não dê `throw Error` — retorne resultado vazio gracefully (causou 9.345 falhas/100% antes do fix). |
| Modelos de IA | Preferir sempre os Claude mais recentes (ex.: `anthropic/claude-haiku-4-5`) via OpenRouter. |

---

## 🔗 INTEGRAÇÕES AVALIADAS

### MarkItDown-MCP (Microsoft) — 📋 Documentado (`INTEGRACAO_MARKITDOWN_MCP.md`)
- Converte PDF/Word/Excel/PPT/imagem/áudio/HTML → **Markdown limpo p/ LLM**. Tool: `convert_to_markdown(uri)` (http/https/file/data).
- Modo escolhido: **servidor MCP** (uso pelo agente Claude). Pronto em **`.mcp.json`** (variante pip).
- Encaixe: COCKPIT-07 (pré-processar anexos antes do OpenRouter). Ressalva: roda local (STDIO/Docker), não conecta direto ao n8n Cloud — automação total exigiria microserviço HTTP (Railway).

### Claude Managed Agents (Anthropic) — 📋 Avaliado, sem ativação imediata (`INTEGRACAO_CLAUDE_MANAGED_AGENTS.md`)
- Runtime gerenciado p/ agentes Claude autônomos de **longa duração** ("desacopla cérebro das mãos"). Beta público 08/04/2026. Preço: tokens API + **US$ 0,08/hora-sessão**.
- Acesso via **API Claude direta** (exige `ANTHROPIC_API_KEY` própria, **não** via OpenRouter).
- **Complementar** ao n8n (não concorrente). Acionável de qualquer canal, por n8n / API direta / MCP. Avaliar **LGPD** antes de enviar PII/PHI ao sandbox.

---

## 🧰 FERRAMENTAS / MCP DISPONÍVEIS (use antes de pedir algo manual)

- **n8n (MCP oficial)** — buscar/criar/editar/validar/ativar workflows direto no Cloud. Fluxo: ler SDK → sugerir nodes → validar → criar.
- **GitHub (MCP)** — PRs, issues, CI, comentários no repo `Rudson-Oliveira/Analise-Claude`.
- **MarkItDown (MCP, local)** — `convert_to_markdown(uri)`.
- **Microsoft Learn / docs** — documentação oficial Microsoft/Azure/Outlook.

> Antes de dizer "não tenho acesso", **procure a ferramenta** — muitos MCPs carregam sob demanda.

---

## 🌐 ECOSSISTEMA DE REPOSITÓRIOS (8 repos satélites mapeados)

1. **telegram-scraper** (React+Node, v3.0) — 24 canais, ROI ~R$170k/ano. Operacional (não usa n8n).
2. **telegram-scraper-inema-n8n** — n8n + Supabase + Telegram Bot. Produção. ⚠️ credenciais Supabase hardcoded (mover).
3. **n8n-workflows-pessoal-2026-01-08** — code review com OpenRouter (precisa key).
4. **hospitalar-automation** — Playwright + Python (local).
5. **MAKE-25-01-26** — Make.com, 11 cenários sociais (independente do n8n).
6. **hospitalar-multi-agent-system** — n8n + Ollama Docker (MCC). Sistema central do orquestrador.
7. **n8n-workflows** — 35 workflows de backup (v2.0).
8. **hospitalar-ia-evolutiva-projeto-completo** — doc do sistema IA autônoma (9 workflows da FASE 2).

### Make.com — 11 cenários (social media)
`Sheets (PC-GERAL/PC-DATAS) → Make (15min) → Drive → Placid ($19/mês) → Instagram/Facebook/LinkedIn`.
Inclui datas comemorativas (post/revisão/reels), transcrição (AssemblyAI), carrossel, bobinas, raspar.

---

## 🚨 SEGURANÇA E RISCOS (itens abertos)

1. **Token Telegram exposto** no histórico do repo telegram-scraper-inema-n8n (`8517…CIK8`) — **REVOGAR no @BotFather e rotacionar**.
2. **Supabase Service Role Key hardcoded** em code node — mover para Credentials/env.
3. **n8n Local depende de ngrok** (URL muda a cada restart) — ngrok pago ou IP fixo.
4. **Custos de API** (OpenRouter/OpenAI por token, Placid $19/mês, Make por operação) — criar alertas de crédito.
5. **LGPD / dados de saúde (PII/PHI)** — avaliar antes de enviar a serviços externos (ex.: sandbox do Managed Agents).
6. Nunca commitar segredos; mensagens/PRs em PT-BR, sem tokens.

---

## 🗺️ ROADMAP — FASE 2

1. Configurar `OPENAI_API_KEY` (Whisper) e `EVOLUTION_API_KEY` (menu WhatsApp 1/2/3).
2. Testar subfluxo de áudio WhatsApp: `áudio → Whisper → OpenRouter → resposta`.
3. Verificar node 7 do COCKPIT-07 (alerta URGENTE WhatsApp, depende de `EVOLUTION_API_KEY`).
4. Decidir sobre WF-HEALTH-CHECK-AGENTES (Ollama offline) — ligar n8n Local ou manter desativado.
5. Implementar os **9 workflows IA-AUTÔNOMA** (Monitor, Analyzer, Decision, Executor, Feedback, Learning, Coordinator, Notifier, Dashboard).
6. Publicar `frontend/index.html` no GitHub Pages.
7. (Opcional) Configurar MarkItDown-MCP no cliente Claude e testar conversão de anexo real.

---

## 🕓 LINHA DO TEMPO DAS SESSÕES

| Sessão | Data | Marco principal |
|---|---|---|
| **1** | 29/05/2026 | Análise completa de 50+ workflows; `CONTEXTO.json` v1.0; `ANALISE_COMPLETA.md`. |
| **2** | 29/05/2026 | FASE 1: fix WF-HEALTH-CHECK (throw→graceful); criado WF-MCC-GET-URL-GS; fix WF-MCC-SET-URL (dataTables→Sheets). Limite 2.500/2.500 atingido. |
| **3** | 31/05/2026 | `OPENROUTER_API_KEY` global; COCKPIT-07/08 migrados HuggingFace→OpenRouter; Orquestrador testado (#21404). |
| **4** | 31/05/2026 | Fix COCKPIT-07 (`specifyBody json→string`, exec #21422 SUCCESS); upgrade plano 10k; 44 workflows ativos; mapeamento Intel. |
| **5** | 15/06/2026 | Integração **MarkItDown-MCP** documentada; `.mcp.json`; bootstrap PowerShell melhorado; CLAUDE.md reforçado. CONTEXTO v4.1. |
| **6** | 21/06/2026 | Avaliação **Claude Managed Agents**; `frontend/index.html` (painel multicanal). CONTEXTO v4.3. |
| **7** | 23/06/2026 | **Este `ORACULO.md`** — consolidação de toda a base de conhecimento. |

---

## 📁 MAPA DOS ARQUIVOS DO REPO

| Arquivo | Papel |
|---|---|
| **`ORACULO.md`** | **Esta base de conhecimento completa (ponto de partida do agente).** |
| `CONTEXTO.json` | Estado estruturado / fonte da verdade (maior versão vence). |
| `README.md` | Visão humana do estado atual. |
| `ANALISE_COMPLETA.md` | Mapa inicial de 39 workflows n8n + 11 cenários Make. |
| `CHECKPOINT_29052026_*.md` | Checkpoints datados (sessões 1–2 da Fase 1). |
| `PROGRESSO_FASE1.md` | Progresso da Fase 1. |
| `SISTEMA_HOSPITALAR_INTEL_09-06-26.md` | Auditoria forense do frontend Intel (21 módulos, nota 3.2/5). |
| `INTEGRACAO_MARKITDOWN_MCP.md` | Integração MarkItDown-MCP (Microsoft). |
| `INTEGRACAO_CLAUDE_MANAGED_AGENTS.md` | Avaliação Claude Managed Agents (Anthropic). |
| `.mcp.json` | Config MCP do Claude Code (servidor `markitdown`). |
| `frontend/index.html` | Painel visual do ecossistema (HTML autocontido). |
| `scripts/iniciar-claude.ps1` | Bootstrap PowerShell para abrir sessão Claude já contextualizada. |
| `CLAUDE.md` | Orientação curta lida automaticamente pelo Claude Code. |

---

## 📖 GLOSSÁRIO

- **COCKPIT-*** — workflows n8n de triagem/briefing com IA (inbox, briefing diário).
- **MCC (Multi-Channel Controller)** — registro central (Google Sheets) de URLs de agentes; SET grava, GET lê.
- **MAS** — Multi-Agent System (orquestrador dinâmico + agentes local/externo).
- **Orquestrador Dinâmico** — roteia cada requisição para o melhor agente disponível via MCC.
- **AGENTE_LOCAL** — agente n8n local com Ollama (Llama 3.2), depende de túnel ngrok.
- **INEMA** — fonte de mensagens (24 canais Telegram) para criação de conteúdo.
- **HospitaLar Intel** — frontend de inteligência (Manus), 21 módulos, CRM funil 7 níveis.
- **Canivete suíço** — princípio de não travar em um único canal/orquestrador.

---

## ✅ COMO MANTER O ORÁCULO SAUDÁVEL

- Ao terminar mudanças relevantes: **atualize `CONTEXTO.json` (bump de versão)**, este `ORACULO.md` e o `README.md`; registre checkpoint se a sessão foi grande.
- Idioma: **PT-BR**. Segredos: **nunca** commitar — apenas IDs e placeholders.
- Git: desenvolva em branch de trabalho; após push, abra **PR em rascunho (draft)**.
- Em conflito de informação: `CONTEXTO.json` (maior versão) é a fonte da verdade; ajuste o oráculo para refletir.

*Consolidado por Claude Opus 4.8 — Sessão 7 · 23/06/2026.*
