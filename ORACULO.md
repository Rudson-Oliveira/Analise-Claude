# 🔮 ORÁCULO — Base de Conhecimento Mestre
## Hospitalar Soluções em Saúde | Sistema de Automação & Inteligência

> **Documento único de verdade (Single Source of Truth).**
> Versão: 5.0 | Última atualização: 23/06/2026 | Mantido por: Agentes Claude (Anthropic)
>
> **Propósito:** Qualquer agente de IA (Claude ou outro) deve conseguir ler ESTE
> documento e, sozinho, entender 100% do projeto — identidade, arquitetura,
> integrações, histórico, estado atual, pendências e convenções — sem precisar
> reconstruir contexto. É o "cérebro" portátil do projeto.

---

## 0. 🚀 BOOTSTRAP — Como um novo agente deve começar

Se você é um agente sendo conectado a este projeto pela primeira vez, faça nesta ordem:

1. **Leia este documento inteiro** (ORACULO.md). Ele é o índice e o resumo de tudo.
2. Leia [CONTEXTO.json](./CONTEXTO.json) para o estado estruturado (máquina-legível).
3. Consulte [SEGURANCA.md](./SEGURANCA.md) antes de tocar em qualquer credencial.
4. Só então aprofunde nos documentos específicos (ver índice na seção 10).

### Prompt pronto para colar (handoff entre conversas)

> "Você é um agente assistindo o projeto da **Hospitalar Soluções em Saúde**.
> Leia o repositório GitHub `Rudson-Oliveira/Analise-Claude`, começando por
> `ORACULO.md` (base de conhecimento mestre) e `CONTEXTO.json`. Eles contêm
> identidade, arquitetura, integrações, histórico de sessões, pendências e
> convenções. Após ler, confirme que entendeu o estado atual e continue de onde
> a última sessão parou. NUNCA exponha credenciais; siga `SEGURANCA.md`."

---

## 1. 🏥 Identidade & Missão

| Campo | Valor |
|---|---|
| **Empresa** | Hospitalar Soluções em Saúde |
| **Proprietário / CEO** | Rudson Antonio Ribeiro Oliveira |
| **Contato** | +55 35 99835-2323 · rud.pa@hotmail.com |
| **Repositório (memória)** | https://github.com/Rudson-Oliveira/Analise-Claude |
| **Domínio do negócio** | Soluções em saúde / hospitalar (B2B + atendimento) |

**Missão do sistema:** automatizar criação de conteúdo, atendimento, triagem,
agendamentos, orçamentos, CRM e inteligência operacional usando IA e workflows,
com a marca presente em redes sociais e canais (WhatsApp, e-mail, Telegram).

---

## 2. 🏗️ Arquitetura Geral

```
┌─────────────────── ENTRADA DE DADOS ───────────────────┐
│ Telegram (INEMA 24ch) · Google Sheets (PC-GERAL/DATAS)  │
│ Webhooks Sistema Hospitalar · e63 Ticketing · WhatsApp  │
└───────────────┬─────────────────────────────────────────┘
                ▼
┌──────────────── N8N CLOUD (núcleo) ─────────────────────┐
│ rudsonoliveira2323.app.n8n.cloud  (~39–68 workflows)    │
│ Categorias: INFRA · INT · CORE · OP · MAS (multi-agente) │
│ IA via OpenRouter (Gemini, Claude Haiku) + Ollama local │
└──────┬───────────────────────────────┬──────────────────┘
       ▼                               ▼
┌──────────────┐            ┌──────────────────────────────┐
│ N8N LOCAL    │            │ MAKE.COM (11 cenários)        │
│ localhost    │            │ Google Sheets/Drive → Placid  │
│ Ollama+PG+   │            │ → Instagram/Facebook/LinkedIn │
│ Mongo        │            └──────────────────────────────┘
└──────────────┘
       ▼
┌──────────── ARMAZENAMENTO ────────────┐
│ Supabase (telegram_msgs) · Google      │
│ Sheets (MCC/PC-GERAL) · GitHub (backup)│
└────────────────────────────────────────┘
```

**Camadas de IA / agentes (MAS):** orquestrador dinâmico que roteia entre
AGENTE_LOCAL (Ollama) e AGENTE_EXTERNO (OpenAI/OpenRouter), com health-check e
gerenciador de agentes via Google Sheets (MCC = memória central compartilhada).

---

## 3. 🔌 Inventário de Integrações

### 3.1 Plataformas de automação
| Plataforma | Papel | Status |
|---|---|---|
| **N8N Cloud** | Núcleo de workflows (IA, atendimento, triagem) | ✅ Ativo |
| **N8N Local** | Ollama self-hosted (sem custo de API) | 🟡 Depende de ngrok |
| **Make.com** | Publicação de conteúdo (datas comemorativas, reels) | ✅ 11 cenários |
| **OpenRouter** | Gateway de LLMs (Gemini, Claude Haiku) | ✅ Configurado |

### 3.2 Workflows N8N principais
| Workflow | ID | Função |
|---|---|---|
| COCKPIT-07 Master Triagem IA | acWQbkOkisdpzryy | Triagem WhatsApp/Email/Notion |
| COCKPIT-08 Briefing Diário | CoDTbFiy8g1ctkmO | Cron 07h resumo diário |
| WF-ORQUESTRADOR-DINAMICO | vZjIt5q0Nh9pRic4 | Roteia entre agentes |
| WF-MCC-SET-URL | MIo8VUzGX77YJuSq | Memória central (Google Sheets) |
| 21-INFRA-Backup-GitHub | QazJlHJIbIfaSfFI | Backup diário de workflows |

### 3.3 Ecossistema de ferramentas conectadas (MCPs / Claude)
> Disponibilidade pode variar por sessão; abaixo o que é relevante ao projeto.

| Categoria | Ferramenta | Uso no projeto | Status conhecido |
|---|---|---|---|
| Redes sociais | **Metricool** | Métricas + agendamento IG/FB | ✅ Conta `@hospitalarsaude` + Facebook conectados |
| Imagens | **Adobe Firefly / Canva** | Geração e edição de criativos | ✅ Disponível |
| Vídeo | **Descript** | Edição de Reels/vídeos por texto | ✅ Disponível |
| Automação | **Zapier / n8n / Make** | Workflows e e-mail | ✅ Disponível |
| E-mail | **Microsoft 365 / Outlook** | Leitura/triagem de e-mails | ✅ Disponível |
| Código | **GitHub** | Este repositório (memória) | ✅ Ativo |
| Dados/IA | **Hugging Face** | Modelos/datasets | ✅ Autenticado (RudsonOliveira) |
| Produto/Analytics | **PostHog** | Métricas de produto | ✅ Org "Rud" |

### 3.4 Canais de comunicação
WhatsApp (Evolution API) · Telegram (Bot + scraper INEMA) · E-mail (Outlook) ·
Instagram `@hospitalarsaude` · Facebook · LinkedIn.

### 3.5 Frontend
**HospitaLar Intel v2.0** (app em Manus) — 21 módulos: Dashboard, CRM 7 níveis,
OKR, NPS, Comm-Hub, Agentes IA, Planos Terapêuticos (OCR), Pipeline de conteúdo,
Calendário, E-mail, Ecossistema digital, etc.

---

## 4. ✅ Estado Atual (23/06/2026)

| Frente | Status |
|---|---|
| Migração HuggingFace → OpenRouter | ✅ Concluída (COCKPIT-07, 08) |
| Bugs críticos de frontend (auditoria 09/06) | ✅ **Corrigidos via MANUS** |
| API Keys (OPENAI / EVOLUTION) | ✅ **Disponíveis** (confirmar se já gravadas no N8N) |
| Token Telegram exposto | 🔴 Redigido no repo — **revogar na origem (@BotFather)** |
| Estratégia de redes sociais | ✅ Documentada (ESTRATEGIA_REDES_SOCIAIS.md) |
| Publicação automática em redes | ⏸️ Pausada por decisão — ativar em fase futura |

---

## 5. 📜 Histórico de Sessões (linha do tempo)

| Sessão | Data | Conquistas-chave |
|---|---|---|
| **1** | ~28/05/2026 | Análise de 50+ workflows; CONTEXTO.json v1.0; README inicial |
| **2** | ~29/05/2026 | AGENTE_LOCAL registrado; WF-MCC-SET-URL testado; orquestrador end-to-end OK (#21404) |
| **3** | 30/05/2026 | OPENROUTER_API_KEY global; COCKPIT-07/08 migrados; correções de API (PATCH vs PUT, versionId) |
| **4** | 31/05/2026 | Fix JSON syntax COCKPIT-07 (specifyBody json→string); exec #21422 SUCCESS |
| **Fase 1** | 29/05/2026 | WF-HEALTH-CHECK desativado (9.345 falhas/100%); diagnóstico raiz |
| **Auditoria FE** | 09/06/2026 | Auditoria forense de 21 módulos (nota 3.2/5) → **bugs depois corrigidos via Manus** |
| **5 (atual)** | 15–23/06/2026 | Orientação de ecossistema; playbook de redes (dados Metricool); correções de segurança; **criação deste ORÁCULO** |

---

## 6. 📋 Pendências Técnicas (atualizado)

| Item | Prioridade | Observação |
|---|---|---|
| Confirmar OPENAI/EVOLUTION keys gravadas no N8N | 🔴 ALTA | APIs já disponíveis; validar configuração + testar pipeline áudio WhatsApp |
| Revogar token Telegram + rotacionar OpenRouter | 🔴 ALTA | Ver SEGURANCA.md (segredo esteve no histórico do Git) |
| Supabase Service Role Key hardcoded | 🟡 MÉDIA | Mover para N8N Credentials |
| ngrok / túnel N8N Local | 🟢 BAIXA | Para teste end-to-end do agente local |
| Ativar publicação automática de redes | 🟢 FUTURO | Quando o proprietário liberar |

---

## 7. 🔐 Postura de Segurança (resumo)

- Credenciais nos documentos estão **mascaradas**; `.gitignore` previne novos vazamentos.
- **Regra de ouro:** nenhuma credencial em arquivos do repo — somente no N8N Credentials Manager.
- Detalhes e checklist completo em **[SEGURANCA.md](./SEGURANCA.md)**.

---

## 8. 📱 Estratégia de Conteúdo (resumo)

- Instagram `@hospitalarsaude`: melhor janela **17h–20h** (pico sexta 20h) + almoço 11h–12h.
- Facebook: melhor janela **10h–12h** (pico quarta 12h); fim de semana fraco.
- Regra: mesma peça, **FB de manhã / IG à noite**. Detalhes em **[ESTRATEGIA_REDES_SOCIAIS.md](./ESTRATEGIA_REDES_SOCIAIS.md)**.

---

## 9. 🤝 Convenções para Agentes (como manter o oráculo vivo)

1. **Este documento é a fonte de verdade.** Ao concluir trabalho relevante, atualize
   a seção 4 (Estado), 5 (Histórico) e 6 (Pendências) e suba a versão no topo.
2. **Sincronize** com `CONTEXTO.json` (versão `meta.versao` deve bater com a daqui).
3. **Nunca** escreva credenciais; mascare (prefixo + `***`) e registre em SEGURANCA.md.
4. **Datas reais:** use a data corrente; não invente. Marque suposições como tal.
5. **Commits** claros em português; **branch** de trabalho conforme orientação do projeto.
6. **Não refaça** o que já está feito — confira o histórico antes de agir.
7. Ao terminar, deixe um **"próximo passo"** explícito (seção 6 ou CONTEXTO.json).

---

## 10. 📁 Índice de Documentos do Repositório

| Arquivo | Conteúdo | Leitura |
|---|---|---|
| **ORACULO.md** | 🔮 Este — base de conhecimento mestre | **Sempre 1º** |
| CONTEXTO.json | Estado estruturado (máquina-legível) | 2º |
| SEGURANCA.md | Achados de segurança + checklist | Antes de credenciais |
| README.md | Contexto humano-legível (resumo) | Geral |
| ANALISE_COMPLETA.md | Análise dos 50+ workflows N8N + Make | Aprofundamento técnico |
| PROGRESSO_FASE1.md | Correções críticas da Fase 1 | Histórico |
| SISTEMA_HOSPITALAR_INTEL_09-06-26.md | Auditoria forense do frontend (21 módulos) | Frontend |
| ESTRATEGIA_REDES_SOCIAIS.md | Playbook de redes (horários, pilares, KPIs) | Conteúdo/marketing |
| CHECKPOINT_29052026_*.md | Checkpoints anteriores | Histórico |

---

*🔮 ORÁCULO mantido por agentes Claude. Se você é um agente e leu até aqui, você
já tem o conhecimento completo do projeto. Atualize este documento ao final do seu
trabalho para que o próximo agente continue de onde você parou.*
