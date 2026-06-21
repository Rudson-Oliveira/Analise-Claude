# 🧭 CHECKPOINT — 21/06/2026 (Sessão 7)

> **Para qualquer agente que retomar:** leia primeiro `CONTEXTO.json` (fonte da verdade) e
> depois este checkpoint. Resumo do que foi construído nesta sessão e o que falta.
> **Analisado por:** Claude Opus 4.8 · **Empresa:** HospitaLar Soluções em Saúde — **Pouso Alegre/MG**.

---

## 🎯 Objetivo da sessão
A partir de duas imagens (LOOP/Claude Code e **Firecrawl**), o CEO pediu para **verificar o ecossistema,
instalar o que faltava e implementar melhorias**. Isso evoluiu para um **sistema de inteligência de
concorrência + redes sociais**, com **painel visual** acessível no celular.

---

## ✅ O que foi realizado (descritivo completo)

### 1. Firecrawl (web → Markdown/JSON para LLM) — INSTALADO
- Adicionado ao **`.mcp.json`** (servidor `firecrawl` via `npx firecrawl-mcp`, chave por `${FIRECRAWL_API_KEY}`).
- **Chave validada** (`fc-9831b6...`) com testes reais: `example.com`, site da HospitaLar, ANVISA, buscas de concorrentes.
- Documentado em **`INTEGRACAO_FIRECRAWL_MCP.md`** (inclui uso da skill **`/loop`** do Claude Code).
- Complementa o **MarkItDown** (arquivos): Firecrawl cobre a **web**.

### 2. Metricool (redes sociais próprias) — CONECTADO
- MCP já tinha a marca **"HospitaLar Soluções em Saúde"** (brandId **6395876**), IG **@hospitalarsaude** + FB, tz America/Sao_Paulo.
- Puxados **dados reais (30 dias)**: ~5.030 seguidores, alcance ~4.374, ~125 curtidas, 82 compart., 21 salvos, **só 1 comentário** ⚠️, ~5% engajamento.
- **Melhor horário** (heatmap real): **17h–20h**, pico **sexta 20h**. Posts de **27–28/05** bombaram (142 interações, 56 compart.).

### 3. WhatsApp via Evolution API — TESTADO
- Instância **`rudson-pessoal`** (status **open**) descoberta via `fetchInstances`. Chave global confirmada.
- **Teste de envio real** retornou HTTP 201 (ressalva: enviar para o próprio número pode falhar — avaliar instância dedicada).

### 4. Tese de monitoramento (definida pelo CEO)
> O alvo **não** é o concorrente local "quieto". É detectar **home care DE FORA** (raio ~200 km, incl.
> São Paulo/DDD 11 e redes nacionais/estaduais) que estão **anunciando/atendendo Pouso Alegre**, além de **convênios**.
- **Raspagem real** confirmou entrantes "de fora": **Home Doctor** (SP, Alto), **Cuidar Saúde** (MG estadual),
  **Atend Home Care**, **Primordial Cuidados**, **AC Vida**. Locais: Vital Care, Medicina Integral PA.
- **Convênio:** **IPSEMG** lançou Programa de Atenção Domiciliar (oportunidade de credenciamento).

### 5. Workflows n8n (Cloud) — criados INATIVOS, isolados, prefixo `MONITOR-`
| Workflow | ID | Função |
|---|---|---|
| **MONITOR-Radar-Entrantes-PousoAlegre** | `Hql1HFXaV6Z9sF8o` | Schedule 24h → Firecrawl SEARCH → OpenRouter classifica "de fora" → IF → **alerta WhatsApp** |
| **MONITOR-Radar-API-Webhook** | `81RFduR2lx7HjRCJ` | Webhook GET `/webhook/radar-pa` → Firecrawl → OpenRouter → Code parse → **responde JSON** (CORS *) p/ o painel |
- **Arquivados:** `MONITOR-Concorrente` (KhvdfUhmwHyjHQng) e `WF-MONITOR-ANVISA` (lOWNpoAL4LM5j4AW) — abordagens superadas.
- **Confirmado:** n8n Cloud (plano pago) usa **`$vars`** (não `$env`).

### 6. Painel de Inteligência (frontend) — NO AR 🌐
- Arquivo **`dashboard/index.html`** (autossuficiente, pensado para **TDAH**).
- **URL pública (mobile):** **https://dashboard-pi-three-34.vercel.app** (deploy Vercel, `noindex`, só a pasta `dashboard/`).
- Funcionalidades: KPIs, abas (Radar / Redes / Melhor Horário / Convênios / **Tarefas**), **filtros**, busca,
  **incluir/ignorar**, **exportar WhatsApp/PDF**, **modo "Ao vivo"** (consome o webhook do n8n),
  **selo 🆕 Novo + 🔔 alerta de risco Alto**, checklist de ativação. Marcações/tarefas no `localStorage`.

---

## 🔑 Variáveis a cadastrar no n8n (Settings → Variables, `$vars`)
`FIRECRAWL_API_KEY` · `RADAR_QUERY` (= `home care atendimento domiciliar Pouso Alegre MG`) ·
`EVOLUTION_API_KEY` · `EVOLUTION_INSTANCE` (`rudson-pessoal`) · `ALERTA_NUMERO` (`5535998352323`) ·
`OPENROUTER_API_KEY` (já existe).

---

## ⏭️ Próximos passos (o que falta)
1. **CEO:** cadastrar as 6 Variables + **ativar** os 2 workflows `MONITOR-Radar-*`.
2. **Agente:** testar o webhook `/webhook/radar-pa` (deve responder `{data:[...]}`) e confirmar o painel "Ao vivo".
3. **Blindagem:** adicionar **token secreto** no webhook (link público expõe a URL → evitar gasto de créditos).
4. **Fase 2 (melhorias):** múltiplas buscas (cuidador de idosos / internação domiciliar / oxigenoterapia PA);
   **Data Table** para alertar só os **novos**; pilar **convênios** automatizado; auto-deploy do painel (git → Vercel).
5. **Fase 2 original (pendente):** `OPENAI_API_KEY` (Whisper) e teste do subfluxo de áudio WhatsApp.

---

## 🧠 Lições técnicas desta sessão (NÃO repetir erros)
- **n8n Cloud** não tem `$env` configurável → use **`$vars`** (recurso *Variables*, plano pago).
- **HTTP Request com body dinâmico:** `contentType: "raw"` + `specifyBody: "string"` + `rawContentType: application/json`
  (validador emite aviso cosmético, mas é o que funciona; embutir valores com `{{ JSON.stringify(...) }}`).
- **Evolution sendText:** `POST {base}/message/sendText/{instância}`, header `apikey`, body `{number, text}` (v2).
- **Workflows do Cloud só ficam legíveis via MCP** se tiverem **"Enable MCP access"** ligado no card.
- **Vercel deploy:** token precisa de **`--scope`** (time `rudson-oliveiras-projects`); desativar **ssoProtection**
  (Vercel Authentication) via API para o link ficar público.
- **Segredos no chat:** o CEO colou chaves (Firecrawl, Evolution, tokens Vercel) — **recomendar revogação/rotação**.
