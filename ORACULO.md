# 🔮 ORÁCULO — Base de Conhecimento Mestre

> **Documento único e canônico do projeto de automação da Hospitalar Soluções em Saúde.**
> Foi desenhado para ser o "cérebro" do projeto: qualquer agente (Claude ou outro) que ler este
> arquivo passa a ter **todo o contexto histórico, técnico e estratégico** e consegue continuar o
> trabalho sem refazer a base de conhecimento.
>
> **Versão do Oráculo:** 1.0 · **Consolidado em:** 23/06/2026 · **Cobre as sessões:** 1 a 6
> **Fonte da verdade legível por máquina:** [`CONTEXTO.json`](./CONTEXTO.json)

---

## 0. 🧭 PROTOCOLO DE ONBOARDING (leia primeiro — é para você, agente)

Se você é um agente acabando de "se conectar" a este projeto, siga esta ordem:

1. **Leia este `ORACULO.md` por inteiro** — ele é o consolidado de tudo.
2. Confira [`CONTEXTO.json`](./CONTEXTO.json) para o estado estruturado/máquina-legível mais recente.
3. Veja o último `CHECKPOINT_*.md` se precisar do detalhe cronológico de uma sessão específica.
4. **Respeite as regras** da seção [§11 Lições aprendidas](#11--lições-aprendidas-do-n8n-não-repetir-erros) e [§12 Segurança](#12--segurança).
5. Só então proponha/execute o próximo passo (seção [§16 Roadmap](#16--roadmap--pendências)).

### 🔑 Prompt de retomada (copie e cole numa nova conversa)

```
Você é o agente de automação da Hospitalar Soluções em Saúde.
Leia o ORACULO.md no repositório GitHub Rudson-Oliveira/Analise-Claude
(é a base de conhecimento mestre) e o CONTEXTO.json, e continue de onde paramos.
Responda em português (BR). Antes de agir no n8n, siga as lições aprendidas do Oráculo.
```

### ⚡ Resumo de 30 segundos (TL;DR)

- **Não há código de aplicação aqui.** Este repositório é a **memória/contexto** do projeto. O trabalho real acontece no **n8n Cloud**.
- **Stack:** n8n Cloud + OpenRouter + Evolution API (WhatsApp) + Notion + Google Sheets + Microsoft Outlook + Make.com.
- **Estado:** ~44 workflows ativos no n8n; migração HuggingFace→OpenRouter concluída; MCC (orquestrador multi-agente) funcionando.
- **Bloqueios principais:** faltam `OPENAI_API_KEY` (Whisper/áudio) e `EVOLUTION_API_KEY` (menu WhatsApp); Ollama local offline.
- **Ações de segurança pendentes:** revogar token Telegram exposto e mover segredos hardcoded para credenciais.

---

## 1. 🏥 Identidade do projeto

| Campo | Valor |
|---|---|
| **Empresa** | Hospitalar Soluções em Saúde |
| **Proprietário / CEO** | Rudson Antonio Ribeiro Oliveira |
| **WhatsApp** | +55 35 99835-2323 |
| **E-mail** | rud.pa@hotmail.com |
| **Idioma de trabalho** | Português (BR) |

### Plataformas e URLs

| Plataforma | URL / Identificador |
|---|---|
| n8n Cloud | https://rudsonoliveira2323.app.n8n.cloud |
| Repositório (este) | https://github.com/Rudson-Oliveira/Analise-Claude |
| OpenRouter | https://openrouter.ai |
| Evolution API | https://evolution-api-production-a1f9.up.railway.app |
| Frontend "HospitaLar Intel" | hospintel-y6rar4gv.manus.space |

---

## 2. 📦 O que é este repositório

Este repo é a **memória persistente** do projeto — checkpoints, estado estruturado e histórico de
decisões, para retomar qualquer sessão sem perder contexto. **Mapa de arquivos:**

| Arquivo | Papel |
|---|---|
| **`ORACULO.md`** | **Este arquivo — base de conhecimento mestre (começe por aqui).** |
| `CLAUDE.md` | Orientação curta lida automaticamente pelo Claude Code no início de cada sessão. |
| `CONTEXTO.json` | Estado estruturado/máquina-legível (versão atual = fonte da verdade). |
| `README.md` | Visão humana do estado atual. |
| `ANALISE_COMPLETA.md` | Análise inicial dos 39 workflows n8n + 11 cenários Make.com. |
| `CHECKPOINT_29052026_1..4.md` | Checkpoints datados da Fase 1 (sessões de 29/05). |
| `PROGRESSO_FASE1.md` | Progresso da Fase 1. |
| `INTEGRACAO_MARKITDOWN_MCP.md` | Integração do MarkItDown-MCP (Microsoft). |
| `SISTEMA_HOSPITALAR_INTEL_09-06-26.md` | Auditoria forense de frontend (21 telas). |
| `.mcp.json` | Config MCP do Claude Code (servidor `markitdown`). |
| `scripts/iniciar-claude.ps1` | Bootstrap PowerShell para abrir sessão Claude Code contextualizada. |

---

## 3. 🏗️ Arquitetura do ecossistema

```
┌─────────────────────────────────────────────────────┐
│                   ENTRADA DE DADOS                   │
├──────────────┬────────────────┬────────────────────┤
│ Telegram     │ Google Sheets  │ Webhooks           │
│ INEMA (24ch) │ PC-GERAL       │ Sistema Hospitalar │
│ @Bot API     │ PC-DATAS / MCC │ e63 Ticketing      │
└──────┬───────┴───────┬────────┴──────────┬─────────┘
       ▼               ▼                   ▼
┌──────────────────────────────────────────────────────┐
│                    N8N CLOUD (n8n@2.21.8)             │
│         (~69 workflows / ~44 ativos)                  │
│  INFRA · INT · CORE · OP · MAS(multi-agente) · INTEL  │
└───────────┬──────────────────────┬───────────────────┘
            ▼                      ▼
┌───────────────────┐   ┌──────────────────────────┐
│   N8N LOCAL       │   │      MAKE.COM             │
│   localhost:5678  │   │   11 cenários ativos      │
│ Docker:           │   │   Sheets→Placid→IG/FB/IN  │
│ - ollama:11434    │   │   (schedule 15min)        │
│ - postgres        │   └──────────────────────────┘
└───────────────────┘
            ▼
┌──────────────────────────────────────────────┐
│ ARMAZENAMENTO: Supabase (telegram_msgs) ·     │
│ Google Sheets (MCC/PC-GERAL) · GitHub (backup)│
└──────────────────────────────────────────────┘
```

**Camadas de IA:** OpenRouter (cloud, modelos Claude/Gemini) + Ollama (local, self-hosted, fallback).
O **MCC (Multi-Channel/Master Controller)** roteia requisições ao melhor agente via URL guardada no Google Sheets.

---

## 4. 🗂️ Registro de workflows n8n (com IDs)

> **Convenção:** sempre opere por **ID** (não por nome). Workflows marcados **INTEL — não alterar**
> pertencem ao projeto Intel em produção; não modificar sem autorização do Rudson.

### COCKPIT (triagem/briefing IA — núcleo operacional atual)

| Workflow | ID | Status | Modelo IA | Notas |
|---|---|---|---|---|
| COCKPIT-07 Inbox WhatsApp/Email/Notion (Master Triagem) | `acWQbkOkisdpzryy` | ✅ ativo (corrigido) | `google/gemini-2.5-flash-preview` | Node 7 (alerta URGENTE WhatsApp) depende de `EVOLUTION_API_KEY`. Fix sessão 4: `specifyBody` json→string. |
| COCKPIT-08 Briefing Diário (cron 07h) | `CoDTbFiy8g1ctkmO` | ✅ ativo | `anthropic/claude-haiku-4-5` | Teste #21415 SUCCESS. |
| COCKPIT-09 Detector/Helper Subworkflow | `ZQLHgsgDppId9qoe` | ⏭️ sem lógica IA | N/A | Apenas executeWorkflowTrigger + code (sem node HF). |
| COCKPIT-05 Polling Notion→WhatsApp | — | ✅ ativo | — | Citado como ativo no estado atual. |

### MCC / Multi-Agente (MAS)

| Workflow | ID | Status | Função |
|---|---|---|---|
| WF-MCC-GET-URL-GS | `2fuDZ6gYLsRxQM93` | ✅ funcionando | GET `/webhook/mcc/get-url?service_name=X` → lê URL no Sheets MCC_CONFIG (via HTTP API + OAuth2). |
| WF-MCC-SET-URL | `MIo8VUzGX77YJuSq` | ✅ funcionando | POST `/webhook/mcc/set-url` → grava URL no Sheets (Code→appendOrUpdate). |
| WF-ORQUESTRADOR-DINAMICO | `vZjIt5q0Nh9pRic4` | ✅ ativo | Roteia requisição → escolhe agente via MCC → fallback. 9 nodes. |
| WF-ORQUESTRADOR-MULTI-AGENTE | `RREL5BmuDu3HBqcR` | ✅ ativo | Versão multi-agente com fallback Ollama↔OpenAI. 17 nodes. |
| WF-HEALTH-CHECK-AGENTES | `9arDgUsepPgKE2K6` | ⚠️ ativo (falha) | Health check 5min; falha porque **Ollama local está offline** (não é bug de código — já corrigido o throw). |
| WF-GERENCIADOR-AGENTES | `exkT2c1GtIbNJmxr` | ✅ ativo | Gerencia agentes (lê/escreve MCC). |
| WF-INICIALIZADOR-AGENTES | `KGtAUkYFhH9UxLSt` | ✅ ativo | Inicializa agentes. |

### Infraestrutura

| Workflow | ID | Status |
|---|---|---|
| 17-INFRA-WF-Master (Orquestrador de Equipes) | `Gx6ak7bXif9Zh3Cn` | ✅ |
| 18-INFRA-Ollama-Gateway | `oB6o3r4iEMXULyAH` | ✅ (depende de túnel/Ollama) |
| 19-INFRA-WF0-Triggers (Central de Gatilhos) | `MgOrbuP6cWvNwNaE` | ✅ |
| 21-INFRA-Backup-GitHub | `QazJlHJIbIfaSfFI` | ✅ (revisão IA precisava de OpenRouter key) |
| 22-INFRA-AI-Code-Reviewer | `B7BBCjKDX5sGIfGU` | ✅ |
| WF-BACKUP-GITHUB | `Qbgwo4yCDqX7QAMy` | ✅ (nodes obsoletos corrigidos) |
| WF-RESTAURACAO-GITHUB | `WHSdG2ovJPyCnCXL` | ✅ (reconstruído; POST `/webhook/restaurar-workflow`) |
| WF-99-Observabilidade-Logs | `BCC5aExZklz2KHTZ` | ✅ (logs → Google Sheets) |
| 20-INFRA-WF1-Diagnostico | `blTLFKOWd4It5KMB` | ❌ inativo (DeepSeek + Memory) |

### Integrações (INT) e Core/Operações (CORE/OP)

| Workflow | ID | Status |
|---|---|---|
| 01-CORE-INEMA-AI-Criador-Universal | `5GQFEcl4PqYaPqXr` | ✅ |
| 02-CORE-Criador-Sites-Vitrine | `YRxqBEDiRd4j22yJ` | ✅ |
| 03-CORE-Vision-AI-Observacao-Web | `BRsMiqymKjnnomFr` | ✅ |
| 04-CORE-Auto-Import-Hospitalar (MySQL) | `LxuhS8681nX9NrB1` | ✅ |
| 05-INT-Webhook-Hospitalar-Bridge | `33xIKaVlBU1RTI8O` | ✅ |
| 06-INT-Telegram-Import | `mEw1hJz1cJMYMDNe` | ✅ |
| 07-INT-Telegram-Scraper | `NM89ewNy9WvjsPQ5` | ✅ |
| 08-INT-e63-Ticketing | `AITTSGpLcImXF3Nt` | ✅ |
| 09-INT-INEMA-Scraper | `uDHrit1TlBfWUxCh` | ✅ |
| 14-OP-Assistente-Virtual-Saude | `Esi1dNLQtzZGgECL` | ✅ |
| 📧 Triagem Email Outlook+IA | `i7f12WgSoAAHraWA` | ⚠️ ativo, mas Outlook com erro de autenticação |
| 📅 VAGA-LUME Calendário IA | `TEOEiAyVSlcyTa31Rgjb9` | ✅ |
| 📱 Triagem WhatsApp Evo+IA | `JiSB5D56uGUTRifp` | ✅ |
| WF-12-Captura-Formulario-Site | `1QDmhEjBoeYtCCP1` | ✅ |
| WF-COMET-01-ANALISADOR | `CHB6gdswY4UAQ9gT` | ✅ |
| 11-OP-Chatbot-Atendimento | `UZaFiDVTYEehjTmq` | ❌ só manualTrigger |
| 12-OP-Gestor-Agendamentos | `tHTuOdVtcsoDadTf` | ❌ Postgres + HuggingFace |
| 13-OP-Notificacoes-Pacientes | `QHdNijZ3JYY2nIK6` | ❌ Postgres |

### Funil de vendas (agentes 00–07) e Orçamentos

| Workflow | ID |
|---|---|
| WF-00-Orquestrador-Funil | `lVC4kyju9m0hPFo2` |
| WF-01-Agente-Prospeccao | `09c0hYoQw6T6KVm8` |
| WF-02-Agente-Qualificacao | `eQRTnUM9CDRnAcAy` |
| WF-03-Agente-Apresentacao | `AH57c4jXxxwV8ild` |
| WF-04-Agente-Maturacao | `km91d8MWMWqdljv7` |
| WF-05-Agente-Negociacao | `VFEiDVW51R9gNdQi` |
| WF-06-Agente-Encerramento | `gUqDltSpRoomJ6ge` |
| WF-07-Agente-Prospeccao-Mercados | `c4WmIUPjX0iH0ktY` |
| WF-Agente-Orcamentos-Completo | `vigd0lMGWAGZaSRB` |

### INTEL (produção — ⛔ não alterar sem autorização)

| Workflow | ID | Webhook |
|---|---|---|
| HospitaLar-Intel-Dispatcher | `UwmGLjOivexhtvV7` | POST `/webhook/hospitalarsaude-intel` |
| Intel-Proposta-Automatica | `CL2CJ91yjqRhPyI7` | POST `/webhook/intel-proposta` |
| Intel-Conteudo-IA | `LkLctxmxWtjbVE8F` | POST `/webhook/intel-conteudo-ia` |

---

## 5. 🔗 Webhooks / endpoints ativos

| Endpoint | Método | Workflow | Retorno |
|---|---|---|---|
| `/webhook/mcc/set-url` | POST | WF-MCC-SET-URL | `{success, service_name, url}` |
| `/webhook/mcc/get-url?service_name=X` | GET | WF-MCC-GET-URL-GS | `{success, url, description}` |
| `/webhook/mcc/orquestrador` | — | WF-ORQUESTRADOR-DINAMICO | roteamento |
| `/webhook/hospitalarsaude-intel` | POST | Intel-Dispatcher | `{ok}` |
| `/webhook/intel-proposta` | POST | Intel-Proposta | `{ok}` |
| `/webhook/intel-conteudo-ia` | POST | Intel-Conteudo | `{ok}` |
| `/webhook/restaurar-workflow` | POST | WF-RESTAURACAO-GITHUB | `{success, workflow_id}` |
| `/webhook/agente-local` | — | N8N Local (Ollama) | offline (aguardando túnel) |

**Exemplo — registrar um agente no MCC:**
```bash
curl -X POST https://rudsonoliveira2323.app.n8n.cloud/webhook/mcc/set-url \
  -H "Content-Type: application/json" \
  -d '{"service_name":"AGENTE_LOCAL","url":"http://host.docker.internal:5678/webhook/agente-local","description":"Agente N8N Local com Ollama (Llama3.2)","is_active":true}'
```

---

## 6. 🔐 Credenciais n8n (nomes + IDs — **sem segredos**)

| Credencial | ID | Uso |
|---|---|---|
| Google Sheets account | `iWwYR5lhrrUABiru` | Sheets MCC_CONFIG / logs |
| Header Auth account | `RKtcfFzRmcnJZBgu` | GitHub / N8N API |
| Evolution API Rudson | `XUO0KTV1AZe2pBXT` | WhatsApp |
| OpenAi account | `HKGFp46mQxWxySRb` | OpenAI |

> Há ~37 credenciais no total no n8n. Acima estão as que aparecem no histórico de trabalho.

### Variáveis de ambiente n8n (status)

| Variável | Status |
|---|---|
| `OPENROUTER_API_KEY` | ✅ Configurado (sessão 31/05/2026) |
| `OPENAI_API_KEY` | ❌ Pendente — necessário para Whisper (transcrição de áudio WhatsApp) |
| `EVOLUTION_API_KEY` | ❌ Pendente — necessário para menu WhatsApp (1=Manter/2=Dormir/3=Excluir) |

### Google Sheets MCC_CONFIG

- **ID da planilha:** `1-rRo3CAb2QunpNJfsAzqYm2lyqmRGsi_nyYnS_FqcDA`
- **Aba:** `MCC_CONFIG` (renomeada de "Folha1")
- **Colunas:** `service_name | url | description | is_active | updated_at`
- **Registros atuais:** `ORQUESTRADOR`, `AGENTE_LOCAL`

---

## 7. 🧰 Capacidades do agente (MCP / ferramentas)

> Antes de dizer "não tenho acesso", **procure a ferramenta** — muitos MCPs carregam sob demanda.

**Configurado no repo (`.mcp.json`):**
- **MarkItDown (MCP, Microsoft)** — `convert_to_markdown(uri)` converte PDF/Word/Excel/PPT/imagem/áudio/HTML → Markdown limpo para LLM. Roda local (STDIO/Docker); **não** conecta direto ao n8n Cloud.

**Disponíveis no ambiente Claude Code (web/CLI) quando conectados:**
- **n8n (MCP oficial)** — buscar/criar/editar/validar/ativar workflows. Fluxo: ler SDK → sugerir nodes → validar → criar.
- **GitHub (MCP)** — PRs, issues, CI, comentários no repo `Rudson-Oliveira/Analise-Claude`.
- **Microsoft Learn / Microsoft 365** — docs oficiais + busca Outlook/SharePoint/Calendar.
- **Notion**, **Google Drive**, **Supabase**, **Make** — leitura/escrita conforme conectado.
- **Web**: WebSearch / WebFetch / Exa / Context7 (docs de libs).

**Não temos hoje:** automação de **navegador real** (tipo `browser-harness`/Playwright/Puppeteer dirigindo Chrome).
Não é necessário no momento — todas as integrações são via API. Reavaliar só se surgir sistema sem API.

---

## 8. 🤖 Modelos de IA — política

- **Preferir sempre os modelos Claude mais recentes** via OpenRouter quando aplicável (ex.: `anthropic/claude-haiku-4-5`).
- Modelos em uso hoje: COCKPIT-07 → `google/gemini-2.5-flash-preview`; COCKPIT-08 → `anthropic/claude-haiku-4-5`.
- **Migração HuggingFace → OpenRouter: CONCLUÍDA** (31/05/2026).

---

## 9. 📎 Integrações avaliadas

### MarkItDown-MCP (Microsoft) — `INTEGRACAO_MARKITDOWN_MCP.md`
- **Função:** anexos (PDF/Word/Excel/imagem) → Markdown limpo → OpenRouter (Claude) → triagem/resposta.
- **Encaixe natural:** COCKPIT-07 (pré-processar anexos antes da IA).
- **Status:** documentado e pronto (`.mcp.json` com variante pip). Falta testar com arquivo real.
- **Ressalva de arquitetura:** roda local; para automação total dentro do n8n Cloud seria preciso um microserviço HTTP (ex.: Railway) chamado por HTTP Request node.

---

## 10. 🌐 Make.com — 11 cenários ativos

Pipeline de conteúdo social, independente do n8n:
```
Google Sheets (PC-GERAL / PC-DATAS) → Make (15min) → Google Drive → Placid (imagens) → Instagram / Facebook / LinkedIn
```
Cenários: Datas Comemorativas (postagem/revisão/reels), Transcrição (AssemblyAI), Geração Placid ($19/mês),
IG→LinkedIn, Review LinkedIn, Carrossel, Bobinas (geral e datas), Raspar.

---

## 11. ⚙️ Lições aprendidas do n8n (NÃO repetir erros)

| Tema | Regra |
|---|---|
| **Editar workflow** | Use **PATCH** em `/rest/workflows/:id`. **PUT retorna 404 (HTML).** |
| **Renomear node** | **Não renomeie** — mantenha o nome original e altere só os parâmetros (rename quebra conexões). |
| **Ativar workflow** | Busque o workflow, extraia o `versionId` e passe-o no body do `activate` (senão 400 "versionId required"). |
| **HTTP Request com expressões `{{ $json.x }}`** | Use `specifyBody: "string"`, **nunca `"json"`** (json valida como JSON puro e quebra — erro de sintaxe ex. "position 593"). |
| **Ler Google Sheets de forma robusta** | Em vez do node Sheets, use `httpRequest` (typeVersion 4) → `https://sheets.googleapis.com/v4/spreadsheets/{ID}/values/{ABA}!A:E`, `authentication: predefinedCredentialType`, `nodeCredentialType: googleSheetsOAuth2Api`. |
| **Respond to Webhook** | Defina `responseMode: responseNode` no Webhook para evitar "Unused Respond to Webhook". |
| **Nodes obsoletos** | `n8n-nodes-base.dataTables`, `.function`, `.start`, `.schedule` (antigo) podem não existir em `n8n@2.21.8` — substituir por equivalentes atuais (Code, Schedule Trigger v1+). |
| **API n8n** | `/rest/` usa **cookie de sessão**; `/api/v1/` exige **`X-N8N-API-KEY`**. |
| **Erro "graceful"** | Health checks não devem `throw` quando vazio — retorne status vazio (o throw do WF-HEALTH-CHECK gerou 9.345 falhas e estourou o limite de execuções). |
| **Modelos de IA** | Preferir Claude mais recente via OpenRouter. |

### Histórico de erros corrigidos
| Sessão | Erro | Fix |
|---|---|---|
| 1 | WF-HEALTH-CHECK `throw Error` (staticData vazio) → 100% falha, 9.345 execuções | Retornar gracefully sem throw |
| 2 | WF-MCC-SET-URL usava `dataTables` (node indisponível) | Code + Google Sheets appendOrUpdate |
| 2 | Limite de execução 2.500/2.500 (plano Free) | Upgrade p/ 10.000/mês (feito pelo usuário) |
| 3 | PUT `/rest/workflows` → 404 HTML | Usar PATCH |
| 3 | `activate` → 400 versionId required | Extrair versionId e passar no body |
| 3 | rename de node quebrava conexões | Manter nome original |
| 3 | Sheets node "Could not get parameter" | Trocar por httpRequest + OAuth2 |
| 4 | COCKPIT-07 JSON syntax error position 593 | `specifyBody` json→string |

---

## 12. 🛡️ Segurança

| Risco | Severidade | Ação |
|---|---|---|
| **Token Telegram exposto** em `ANALISE_COMPLETA.md` (repo telegram-scraper-inema-n8n) | 🔴 Alta | **Revogar no @BotFather e gerar novo.** Considerar limpar do histórico do Git. |
| **Supabase Service Role Key hardcoded** em code node (telegram-scraper-inema-n8n) | 🟠 Média | Mover para Credentials/variáveis do n8n. |
| **OpenRouter key parcial** registrada em `CONTEXTO.json` | 🟡 Baixa | Manter apenas como variável n8n; não versionar a chave. |
| MarkItDown em modo HTTP/SSE sem auth | 🟡 Baixa | Bind só em localhost; não expor a rede pública. |

> **Regra geral:** nunca commitar API keys/tokens reais. Usar placeholders e variáveis de ambiente.

---

## 13. 🖥️ Frontend "HospitaLar Intel" — resumo da auditoria (09/06/2026)

Sistema com 21 telas (Dashboard, CRM funil 7 níveis, OKR, NPS, Comm-Hub, Agentes IA, Planos Terapêuticos com OCR, etc.). **Nota geral: 3.2/5.**

**Críticos:** toast persistente sem auto-dismiss; máscara CPF incompleta na Proposta; spinners infinitos sem empty state (NPS/CRM/Funil); sidebar sem hamburger em mobile.
**Projeção:** com correções P1→~4.0, P2→~4.4, P3→~4.7. Detalhe completo em `SISTEMA_HOSPITALAR_INTEL_09-06-26.md`.

---

## 14. 📚 Repositórios GitHub relacionados

| Repo | Stack | Status |
|---|---|---|
| telegram-scraper | React + Node.js (v3.0, 24 canais, ROI ~R$170k/ano) | ✅ operacional (não usa n8n) |
| telegram-scraper-inema-n8n | n8n + Supabase + Telegram | ✅ produção (⚠️ segredos expostos) |
| n8n-workflows-pessoal-2026-01-08 | Code review com OpenRouter | precisa OpenRouter key |
| hospitalar-automation | Playwright + Python | local |
| MAKE-25-01-26 | Make.com (11 cenários) | ✅ independente |
| hospitalar-multi-agent-system | n8n + Ollama Docker (MCC) | ✅ sistema central |
| n8n-workflows | 35 workflows backup (v2.0) | backup |
| hospitalar-ia-evolutiva-projeto-completo | Doc do sistema IA autônoma | 9 workflows p/ Fase 2 |

---

## 15. 🕐 Linha do tempo das sessões

| # | Data | Marcos |
|---|---|---|
| 1 | 29/05/2026 | Repo criado; análise de 8 repos e ~68 workflows; WF-HEALTH-CHECK corrigido; WF-MCC-GET-URL-GS criado. |
| 2 | 29/05/2026 | Limite de execução estourado (2.500); MCC-SET corrigido (dataTables→Sheets); orquestrador mapeado. |
| 3 | 29/05/2026 | Upgrade para 10k exec; MCC SET+GET funcionando; multi-agente/triggers/observabilidade ativados. |
| 4 | 29/05/2026 | 44 workflows ativos (+6); Intel mapeado; backup/restauração corrigidos. |
| 5 (=v3/v4) | 31/05/2026 | `OPENROUTER_API_KEY` configurado; migração HF→OpenRouter; COCKPIT-07 corrigido (specifyBody). |
| 6 | 09–15/06/2026 | Auditoria de frontend; integração MarkItDown-MCP documentada; CLAUDE.md + bootstrap PowerShell. |
| — | 23/06/2026 | **Criação deste Oráculo** (consolidação de tudo) + análise do "browser-harness". |

---

## 16. 🎯 Roadmap / pendências

### 🔴 Alta prioridade — FASE 2
1. Configurar `OPENAI_API_KEY` (Whisper) e `EVOLUTION_API_KEY` (menu WhatsApp) no n8n.
2. Testar subfluxo de áudio WhatsApp: `áudio → Whisper → OpenRouter → resposta`.
3. Verificar node 7 do COCKPIT-07 (alerta URGENTE — depende de `EVOLUTION_API_KEY`).
4. Decidir sobre WF-HEALTH-CHECK-AGENTES: ligar N8N Local + Ollama **ou** desativar enquanto Ollama estiver offline.
5. **Segurança:** revogar token Telegram exposto; mover Supabase key para credenciais.

### 🟡 Média
6. Testar MarkItDown-MCP com PDF/Word real do hospital.
7. Corrigir autenticação Outlook (Triagem Email).
8. Implementar os 9 workflows do `hospitalar-ia-evolutiva` (IA autônoma).
9. Implementar correções P1 do frontend HospitaLar Intel.

### 🟢 Baixa
10. Túnel ngrok/IP fixo para N8N Local (teste end-to-end do agente local).
11. Tratamento de erros padronizado + dashboard de monitoramento.

---

## 17. 🔤 Glossário

- **MCC** — Multi-Channel/Master Controller: orquestração que descobre a URL do agente certo via Google Sheets.
- **COCKPIT-xx** — família de workflows operacionais (inbox/triagem/briefing).
- **INEMA** — fonte de mensagens (24 canais Telegram) que alimenta criação de conteúdo.
- **INTEL** — projeto/produto em produção (dispatcher + proposta + conteúdo); não alterar sem autorização.
- **AGENTE_LOCAL / AGENTE_EXTERNO** — Ollama local vs OpenAI/cloud (fallback).
- **Placid** — serviço de geração de imagens usado pelos cenários Make.

---

## 18. 🧱 Como manter o Oráculo saudável

- Ao concluir mudanças relevantes: **atualize esta `ORACULO.md`** (bump da versão no topo + entrada na §15) e o `CONTEXTO.json`.
- Registre um `CHECKPOINT_*.md` quando a sessão for grande.
- Idioma: **PT-BR**. Segredos: **nunca** versionar chaves reais.
- Git: desenvolver na branch de trabalho indicada; após push, abrir **PR em rascunho**.

---

## 19. 📒 Changelog do Oráculo

| Versão | Data | Mudança |
|---|---|---|
| 1.0 | 23/06/2026 | Criação do Oráculo: consolidação completa das sessões 1–6, registro de workflows/credenciais/webhooks, capacidades, lições, segurança, roadmap e protocolo de onboarding. |

---

*Oráculo mantido para a Hospitalar Soluções em Saúde. Comece sempre por aqui.*
