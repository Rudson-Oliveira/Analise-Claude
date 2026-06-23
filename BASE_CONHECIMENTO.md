# 🔮 BASE DE CONHECIMENTO — Projeto Hospitalar / Analise-Claude

> **Este é o "oráculo" do projeto.** Documento único, completo e autossuficiente.
> Qualquer agente (humano ou IA) que ler este arquivo do início ao fim passa a
> conhecer todo o contexto, histórico, arquitetura, IDs, convenções e pendências
> — sem precisar reconstruir a base de conhecimento nem reler todos os outros
> arquivos.
>
> **Fonte da verdade rápida (máquina):** [CONTEXTO.json](./CONTEXTO.json)
> **Orientação operacional do assistente:** [CLAUDE.md](./CLAUDE.md)
> **Última consolidação:** 2026-06-15 · Consolidado por Claude (Opus) · Cobre as sessões 1–5.

---

## 0. Protocolo do Oráculo — como um agente "se conecta" e usa este conhecimento

1. **Leia este arquivo inteiro** (`BASE_CONHECIMENTO.md`). Ele contém o estado consolidado.
2. Para dados estruturados/máquina, cruze com [`CONTEXTO.json`](./CONTEXTO.json).
3. Para detalhes históricos de uma sessão específica, vá ao `CHECKPOINT_*.md` correspondente.
4. **Antes de agir no n8n**, releia a seção **§7 Convenções técnicas (lições aprendidas)** para não repetir erros já resolvidos.
5. Ao terminar mudanças relevantes, **atualize este arquivo + `CONTEXTO.json`** (regra de manutenção — §11).
6. Idioma de resposta: **português (BR)**.

> Bootstrap automatizado: `scripts/iniciar-claude.ps1` abre uma sessão Claude Code
> já apontada para o repositório e instrui a leitura deste oráculo. Use
> `-Headless` para um agente coletar o resumo e seguir.

---

## 1. Identidade do projeto

| Campo | Valor |
|---|---|
| **Empresa** | Hospitalar Soluções em Saúde |
| **Proprietário** | Rudson Antonio Ribeiro Oliveira (CEO) |
| **Contato** | +55 35 99835-2323 · rud.pa@hotmail.com |
| **Repositório (este)** | https://github.com/Rudson-Oliveira/Analise-Claude |
| **Natureza do repo** | Memória/contexto do projeto. **Não tem código de aplicação** — o trabalho real roda no n8n Cloud, Make.com e apps externos. |

### Stack
n8n Cloud (orquestração) · OpenRouter (LLMs) · Evolution API (WhatsApp) · Notion · Google Sheets · Microsoft Outlook · Make.com (social media) · Supabase (Telegram msgs) · Ollama local (opcional) · GitHub (backup).

### Plataformas e URLs
| Plataforma | URL / Identificador |
|---|---|
| n8n Cloud | https://rudsonoliveira2323.app.n8n.cloud (versão n8n@2.21.8, TZ America/Sao_Paulo) |
| OpenRouter | https://openrouter.ai |
| Evolution API | https://evolution-api-production-a1f9.up.railway.app |
| Frontend "HospitaLar Intel" | https://hospintel-y6rar4gv.manus.space (auditado — §9) |
| Google Sheets MCC | ID `1-rRo3CAb2QunpNJfsAzqYm2lyqmRGsi_nyYnS_FqcDA`, aba `MCC_CONFIG` |

---

## 2. Plano n8n Cloud e limites

- **Plano atual:** 10.000 execuções/mês (upgrade feito pelo usuário; antes era Free 2.500/mês).
- **Histórico crítico:** em maio/2026 o limite Free (2.500) foi esgotado por 9.345 execuções em erro do `WF-HEALTH-CHECK-AGENTES` — isso travou TODOS os workflows ("Execution limit reached"). Resolvido com o fix do health-check + upgrade.
- **Contador reseta** no dia 1º de cada mês.

---

## 3. Arquitetura geral

```
ENTRADA            →    PROCESSAMENTO         →    SAÍDA / ARMAZENAMENTO
─────────────────       ──────────────────         ─────────────────────
Telegram INEMA (24ch)   n8n CLOUD (~69 wf)         WhatsApp (Evolution API)
Google Sheets           ├─ INFRA (triggers,        Email (Outlook)
 (PC-GERAL/PC-DATAS)    │   backup, orquestrador)  Notion
Webhooks                ├─ INT (scrapers/bridges)  Instagram/Facebook/LinkedIn
 (Sist. Hospitalar,     ├─ CORE (criação IA)        (via Make.com)
  e63 Ticketing)        ├─ OP (chatbot/agenda)     Supabase (telegram_msgs)
                        ├─ MAS (multi-agente)      Google Sheets (MCC/LOGS)
                        └─ COCKPIT (triagem IA)    GitHub (backup workflows)
                        +  n8n LOCAL (Ollama, opcional, via túnel)
                        +  Make.com (11 cenários social media, ciclo 15min)
```

Padrões-chave:
- **MCC (Multi-Channel/Master Control Config):** planilha Google Sheets central que mapeia `service_name → url`. Workflows leem/escrevem nela para descobrir endpoints de agentes dinamicamente.
- **Orquestrador dinâmico:** recebe requisição → consulta MCC → escolhe agente → fallback (local Ollama ↔ externo OpenAI/OpenRouter).
- **COCKPIT (mais recente):** pipeline de triagem/briefing com IA (WhatsApp/Email/Notion).

---

## 4. Inventário de workflows n8n (com IDs)

> Total ~69 workflows; ~44 ativos ao fim da sessão 4. IDs são a chave para operar via API.

### 4.1 MCC / Multi-Agente (núcleo de orquestração)
| Workflow | ID | Status | Observação |
|---|---|---|---|
| WF-ORQUESTRADOR-DINAMICO | `vZjIt5q0Nh9pRic4` | ✅ ATIVO | Orquestrador principal; usa MCC; AGENTE_LOCAL registrado no staticData |
| WF-ORQUESTRADOR-MULTI-AGENTE | `RREL5BmuDu3HBqcR` | ✅ ATIVO | 17 nós; Ollama LOCAL ↔ OpenAI EXTERNO + fallback |
| WF-MCC-GET-URL-GS | `2fuDZ6gYLsRxQM93` | ✅ FUNCIONA | `GET /webhook/mcc/get-url?service_name=X` (lê via HTTP Sheets API) |
| WF-MCC-SET-URL | `MIo8VUzGX77YJuSq` | ✅ FUNCIONA | `POST /webhook/mcc/set-url` (Code → Sheets appendOrUpdate) |
| WF-HEALTH-CHECK-AGENTES | `9arDgUsepPgKE2K6` | ⚠️ ATIVO | Código corrigido; ainda falha **se Ollama offline** (5min) |
| WF-GERENCIADOR-AGENTES | `exkT2c1GtIbNJmxr` | ✅ ATIVO | |
| WF-INICIALIZADOR-AGENTES | `KGtAUkYFhH9UxLSt` | ✅ ATIVO | |

### 4.2 COCKPIT — Triagem/Briefing IA (migração HuggingFace→OpenRouter, sessões 3–4)
| Workflow | ID | Status | Modelo | Teste |
|---|---|---|---|---|
| COCKPIT-07 (WhatsApp/Email/Obsidian→Notion Inbox) | `acWQbkOkisdpzryy` | ✅ MIGRADO+CORRIGIDO | google/gemini-2.5-flash-preview | exec #21422 SUCCESS |
| COCKPIT-08 (Cron 07h Briefing Diário) | `CoDTbFiy8g1ctkmO` | ✅ MIGRADO | anthropic/claude-haiku-4-5 | exec #21415 SUCCESS |
| COCKPIT-09 (Helper Texto Projeto+Confiança) | `ZQLHgsgDppId9qoe` | ⏭️ PULADO | N/A (sem node HF) | N/A |

### 4.3 Infraestrutura
| Workflow | ID |
|---|---|
| 21-INFRA-Backup-GitHub | `QazJlHJIbIfaSfFI` |
| WF-BACKUP-GITHUB (reconstruído) | `Qbgwo4yCDqX7QAMy` |
| WF-RESTAURACAO-GITHUB (reconstruído) | `WHSdG2ovJPyCnCXL` |
| 19-INFRA-WF0-Triggers (central de gatilhos) | `MgOrbuP6cWvNwNaE` |
| 18-INFRA-Ollama-Gateway | `oB6o3r4iEMXULyAH` |
| WF-99-Observabilidade-Logs (→ Google Sheets LOGS) | `BCC5aExZklz2KHTZ` |
| 22-INFRA-AI-Code-Reviewer | `B7BBCjKDX5sGIfGU` |
| 17-INFRA-WF-Master (orquestrador de equipes) | `Gx6ak7bXif9Zh3Cn` |

### 4.4 Integrações
| Workflow | ID |
|---|---|
| 04-CORE-Auto-Import (MySQL schedule) | `LxuhS8681nX9NrB1` |
| 06-INT-Telegram-Import | `mEw1hJz1cJMYMDNe` |
| 07-INT-Telegram-Scraper (produção) | `NM89ewNy9WvjsPQ5` |
| 08-INT-e63-Ticketing | `AITTSGpLcImXF3Nt` |
| 09-INT-INEMA-Scraper | `uDHrit1TlBfWUxCh` |
| 05-INT-Webhook-Hospitalar | `33xIKaVlBU1RTI8O` |
| 📧 Triagem Email Outlook+IA | `i7f12WgSoAAHraWA` (⚠️ erro auth Outlook) |
| 📅 VAGA-LUME Calendário IA | `TEOEiAyVSlcyTa31Rgjb9` |
| 📱 Triagem WhatsApp Evo+IA | `JiSB5D56uGUTRifp` |

### 4.5 CORE / Operações
| Workflow | ID |
|---|---|
| 01-CORE-INEMA-AI (criador automações via IA) | `5GQFEcl4PqYaPqXr` |
| 02-CORE-Criador-Sites | `YRxqBEDiRd4j22yJ` |
| 03-CORE-Vision-AI | `BRsMiqymKjnnomFr` |
| 14-OP-Assistente-Virtual | `Esi1dNLQtzZGgECL` |
| WF-12-Captura-Formulario-Site | `1QDmhEjBoeYtCCP1` |
| WF-COMET-01-ANALISADOR | `CHB6gdswY4UAQ9gT` |

### 4.6 Funil de Vendas (agentes)
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

### 4.7 Intel (PROJETO ATIVO — ⚠️ NÃO ALTERAR sem autorização de Rudson)
| Workflow | ID | Webhook |
|---|---|---|
| HospitaLar-Intel-Dispatcher | `UwmGLjOivexhtvV7` | `POST /webhook/hospitalarsaude-intel` |
| Intel-Proposta-Automatica | `CL2CJ91yjqRhPyI7` | `POST /webhook/intel-proposta` |
| Intel-Conteudo-IA | `LkLctxmxWtjbVE8F` | `POST /webhook/intel-conteudo-ia` |

### 4.8 Inativos relevantes (não ativáveis agora)
`11-OP-Chatbot-Atendimento` (`UZaFiDVTYEehjTmq`, só manualTrigger) · `12-OP-Gestor-Agendamentos` (`tHTuOdVtcsoDadTf`, Postgres+HF) · `13-OP-Notificacoes-Pacientes` (`QHdNijZ3JYY2nIK6`, Postgres) · `20-INFRA-WF1-Diagnostico` (`blTLFKOWd4It5KMB`, DeepSeek+Memory) · `WF-SIMULADOR-FRONTEND` (`8AXWxG4OYbCqsI1P`, nodes antigos).

---

## 5. Webhooks/endpoints funcionando

| Endpoint | Método | Workflow | Retorno |
|---|---|---|---|
| `/webhook/mcc/set-url` | POST | WF-MCC-SET-URL | `{success, service_name, url}` |
| `/webhook/mcc/get-url?service_name=X` | GET | WF-MCC-GET-URL-GS | `{success, url, description, is_active}` |
| `/webhook/mcc/orquestrador` | — | WF-ORQUESTRADOR-DINAMICO | roteia p/ agente |
| `/webhook/hospitalarsaude-intel` | POST | Intel-Dispatcher | `{ok}` |
| `/webhook/intel-proposta` | POST | Intel-Proposta | `{ok}` |
| `/webhook/intel-conteudo-ia` | POST | Intel-Conteudo | `{ok}` |
| `/webhook/restaurar-workflow` | POST | WF-RESTAURACAO-GITHUB | `{success, workflow_id}` |
| `/webhook/agente-local` | — | n8n Local (Ollama) | offline até túnel ativo |

Exemplo (registrar AGENTE_LOCAL no MCC):
```bash
curl -X POST https://rudsonoliveira2323.app.n8n.cloud/webhook/mcc/set-url \
  -H "Content-Type: application/json" \
  -d '{"service_name":"AGENTE_LOCAL","url":"http://host.docker.internal:5678/webhook/agente-local","description":"Agente N8N Local com Ollama (Llama3.2)","is_active":true}'
```

---

## 6. Credenciais e variáveis

### 6.1 Credenciais n8n (por nome/ID — **nunca os segredos**)
| Credencial | ID |
|---|---|
| Google Sheets account | `iWwYR5lhrrUABiru` |
| Header Auth account (GitHub/N8N API) | `RKtcfFzRmcnJZBgu` |
| Evolution API Rudson | `XUO0KTV1AZe2pBXT` |
| OpenAi account | `HKGFp46mQxWxySRb` |

### 6.2 Variáveis n8n
| Variável | Status | Para quê |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ Configurado | LLMs via OpenRouter |
| `OPENAI_API_KEY` | ❌ Pendente | Whisper (transcrição de áudio WhatsApp) |
| `EVOLUTION_API_KEY` | ❌ Pendente | Menu WhatsApp (1=Manter/2=Dormir/3=Excluir); alerta URGENTE do COCKPIT-07 node 7 |

### 6.3 Google Sheets MCC_CONFIG
- Planilha `1-rRo3CAb2QunpNJfsAzqYm2lyqmRGsi_nyYnS_FqcDA`, aba `MCC_CONFIG` (renomeada de "Folha1").
- Colunas: `service_name | url | description | is_active | updated_at`.
- Registros atuais: `ORQUESTRADOR`, `AGENTE_LOCAL`.

---

## 7. Convenções técnicas (LIÇÕES APRENDIDAS — não repetir erros)

| Tema | Regra |
|---|---|
| Editar workflow | Use **PATCH** `/rest/workflows/:id`. **PUT → 404 (HTML)**. |
| Ativar workflow | Buscar workflow (GET) → extrair `versionId` → passar no body do `/activate` (senão **400 "versionId required"**). |
| Renomear node | **Não renomeie** — manter o nome original, alterar só os parâmetros (rename quebra conexões). |
| HTTP Request com expressões `{{ $json.x }}` | Usar `specifyBody: "string"`, **nunca `"json"`** (json valida como JSON puro → "JSON syntax error"). |
| Ler Google Sheets de forma robusta | Em vez do node Sheets (dá "Could not get parameter"), usar `httpRequest` v4 + `predefinedCredentialType: googleSheetsOAuth2Api` na URL `https://sheets.googleapis.com/v4/spreadsheets/{ID}/values/{ABA}!A:E`. |
| Node `dataTables` | Não disponível em n8n@2.21.8 → substituir por Code + Google Sheets `appendOrUpdate`. |
| Health-check sem agentes | Não dar `throw Error` quando vazio → `return` graceful (senão gera milhares de execuções falhas e estoura o limite). |
| API n8n | `/rest/` usa cookie de sessão; `/api/v1/` exige header `X-N8N-API-KEY`. |
| Modelos de IA | Preferir Claude mais recente (ex.: `anthropic/claude-haiku-4-5`) via OpenRouter quando aplicável. |
| GitHub editor travando com arquivo grande | Usar `cmTile.view.dispatch()` (JS) para inserir conteúdo. |

### Endpoints REST n8n usados
`GET /rest/workflows?limit=100` · `GET /rest/workflows/{id}` · `PATCH /rest/workflows/{id}` · `POST /rest/workflows/{id}/activate` (body `{versionId}`) · `POST /rest/workflows/{id}/deactivate` (body `{versionId}`) · `GET /rest/executions?workflowId={id}&limit=5` · `GET /rest/credentials`.

---

## 8. Make.com — 11 cenários (social media, independente do n8n)
Fluxo: `Google Sheets (PC-GERAL/PC-DATAS) → Make (lê 15min) → Google Drive → Placid (gera imagens, $19/mês) → Instagram/Facebook/LinkedIn`.
Cenários: Datas Comemorativas (Postagem/Revisão/Reels), Transcrição (AssemblyAI PT-BR), Geração Placid, Instagram→LinkedIn, Review LinkedIn, Carrossel, Bobinas (Geral/Datas), Raspar.

---

## 9. Frontend "HospitaLar Intel" — auditoria 09/06/2026 (nota 3.2/5)
App: https://hospintel-y6rar4gv.manus.space (v2.0, 21 módulos: Dashboard, CRM 7 níveis, OKR, NPS, Comm-Hub, Tarefas, Agentes IA, Planos Terapêuticos c/ OCR, Pipeline, Calendário, Email, Ecossistema, Proposta, Contratos, etc.).
**Críticos a corrigir:** toast sem auto-dismiss; máscara CPF incompleta na Proposta; spinners infinitos sem empty-state (NPS/CRM/Funil); sidebar sem hamburger em mobile; acentuação "SOLUÇÕES EM SAÚDE". Projeção: corrigindo P1→~4.0, P2→~4.4, P3→~4.7.

---

## 10. Riscos e segurança (PENDÊNCIAS DE REMEDIAÇÃO)

| Risco | Ação |
|---|---|
| 🔴 **Token do bot Telegram exposto** no `ANALISE_COMPLETA.md` | **Revogar no @BotFather e gerar novo**; remover do histórico. (Não repetir o token aqui.) |
| 🔴 **Supabase Service Role Key hardcoded** em node Code (telegram-scraper-inema-n8n) | Mover para Credentials do n8n / variável de ambiente. |
| 🟡 n8n Local depende de Ngrok (URL muda a cada restart) | Ngrok pago ou IP fixo. |
| 🟢 Custos: Placid $19/mês, OpenRouter/OpenAI por token, Make por operação | Monitorar créditos / alerta de custo. |

---

## 11. Linha do tempo / histórico de sessões

- **Sessão 1 (29/05):** criado o repo Analise-Claude; análise de 8 repos GitHub + 39→68 workflows; diagnosticado o `WF-HEALTH-CHECK-AGENTES` causando 100% de falhas; primeiro fix + criação do `WF-MCC-GET-URL-GS`.
- **Sessão 2 (29/05):** estourou o limite Free (2.500); fixes do MCC-SET/GET; `ORQUESTRADOR-DINAMICO` validado; preparada Fase 2.
- **Sessão 3 (29–31/05):** **upgrade para 10.000 exec/mês**; MCC totalmente funcionando (aba renomeada p/ MCC_CONFIG); ativados MULTI-AGENTE, WF0-Triggers, Observabilidade-Logs; `OPENROUTER_API_KEY` cadastrado; iniciada migração COCKPIT HuggingFace→OpenRouter.
- **Sessão 4 (31/05):** 38→44 workflows ativos; reconstruídos BACKUP/RESTAURACAO-GITHUB; COCKPIT-07 corrigido (`specifyBody json→string`, exec #21422 SUCCESS); COCKPIT-08 migrado (exec #21415); CONTEXTO.json v4.0.
- **Sessão 5 (14–15/06):** organização da base de Claude Code na web — habilitado Dynamic Workflows (`.claude/settings.json`), criados `CLAUDE.md` (orientação automática) e `scripts/iniciar-claude.ps1` (bootstrap); criado este oráculo `BASE_CONHECIMENTO.md` (PR #1 mergeado).

---

## 12. Estado atual e próximos passos (Fase 2)

**Pendências priorizadas:**
1. 🔴 Configurar `OPENAI_API_KEY` (Whisper) e `EVOLUTION_API_KEY` (menu/alerta WhatsApp).
2. 🟡 Testar pipeline de áudio WhatsApp ponta a ponta: `áudio → Whisper → OpenRouter → resposta`.
3. 🟡 Decidir sobre `WF-HEALTH-CHECK-AGENTES`: ligar n8n Local+Ollama (túnel) ou desativar enquanto Ollama estiver offline (evita falhas a cada 5min).
4. 🟡 Corrigir auth do `📧 Triagem Email Outlook+IA`.
5. 🟢 Implementar Fase 2 do `hospitalar-ia-evolutiva` — 9 workflows: MONITOR, ANALYZER, DECISION, EXECUTOR, FEEDBACK, LEARNING, COORDINATOR, NOTIFIER, DASHBOARD.
6. 🟢 Remediar segredos expostos (§10).

**Repositórios relacionados (contexto):** telegram-scraper (v3.0, ROI R$170k/ano) · telegram-scraper-inema-n8n · n8n-workflows (35 backups) · hospitalar-multi-agent-system (sistema central) · hospitalar-ia-evolutiva-projeto-completo (fonte da Fase 2) · MAKE-25-01-26.

---

*Mantido como fonte única de verdade narrativa. Ao alterar o sistema, atualize este arquivo e o `CONTEXTO.json` (bump de versão) na mesma sessão.*
