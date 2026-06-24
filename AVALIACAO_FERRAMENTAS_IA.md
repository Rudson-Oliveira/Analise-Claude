# Avaliação de Ferramentas de IA — Hospitalar Soluções em Saúde

> Análises solicitadas por Rudson Oliveira (CEO) | Avaliado por Claude
> Contexto do projeto: automação via **N8N Cloud + OpenRouter + Evolution API + Notion + Google Sheets + Outlook**
> Escala de interesse/viabilidade: **0 (irrelevante) a 5 (essencial)**

---

## 1. Open Design — Nota: **2 / 5**

**O que é:** plataforma **open source** (licença Apache-2.0), *local-first*, posicionada como alternativa ao **Claude Design**. Não é um editor tipo Figma do zero — é uma **camada de controle** que transforma agentes de código que você já usa (Claude Code, Codex, Cursor, Gemini, Qwen, OpenCode) no "motor" de design, gerando sites, dashboards, apresentações e design systems a partir de prompts. Roda localmente ou como web app.

| Critério | Avaliação |
|---|---|
| É open source de verdade? | ✅ Sim (Apache-2.0) |
| Alinhamento com o stack atual | 🔴 Baixo — foco do projeto é automação/orquestração, não front-end |
| Privacidade (saúde/LGPD) | 🟢 Ponto forte — local-first ajuda com dados sensíveis |
| Utilidade imediata | 🟡 Só se for criar painel/portal visual para o sistema hospitalar |

**Recomendação:** guardar como referência futura para a camada de interface (subiria para 3-4 se houver um cockpit/portal visual). Não é prioridade frente às pendências reais (OPENAI_API_KEY, EVOLUTION_API_KEY, teste de áudio WhatsApp).

**Fontes:**
- https://open-design.ai/
- https://penpot.app/ (alternativa open-source)
- https://opensourcedesign.net/

---

## 2. Polsia — Nota de viabilidade: **2 / 5**

**O que é:** plataforma de IA **autônoma** (polsia.com) que promete planejar, programar, fazer marketing e operar empresas inteiras 24/7. Um "AI CEO" (rodando sobre Claude/Anthropic) executa tarefas sozinho e envia resumos diários. Legítima — fundador com credenciais reais, captação de US$30M a US$250M de valuation.

**Sinais de alerta sérios:**
- **Trustpilot 2.1/5** (70% das avaliações com 1 estrela).
- Tarefas marcadas como "concluídas" que nunca sobem; **créditos queimados em falhas, sem reembolso**.
- Suporte ignorado por semanas.
- **Código fica inacessível se a assinatura vencer** (lock-in pesado).
- **Não valida demanda** — executa qualquer ideia, mesmo sem mercado.
- Custo: **US$49/mês + take-rate de 20%** sobre receita gerada e gasto com anúncios.

| Critério | Avaliação |
|---|---|
| Maturidade/confiabilidade | 🔴 Baixa (reviews ruins, falhas de deploy) |
| Encaixe com o projeto | 🔴 Baixo — já existe orquestração própria (N8N + OpenRouter + Evolution) |
| Risco de lock-in | 🔴 Alto (perde o código sem assinatura) |
| Adequação saúde/LGPD | 🔴 Preocupante — dados sensíveis em plataforma autônoma de terceiros |

**Recomendação:** **não vale a pena** para o core da Hospitalar Soluções — exige controle, auditoria e conformidade, o oposto de uma "caixa-preta" autônoma. O stack atual (onde você detém o código e os workflows) é mais adequado. Talvez 3/5 apenas para testar uma ideia paralela e descartável.

**Fontes:**
- https://polsia.com/
- https://preuve.ai/blog/polsia-review
- https://www.producthunt.com/products/polsia
- https://www.contextstudios.ai/blog/polsia-how-a-solo-founder-hit-1m-arr-in-30-days-with-ai-agents
