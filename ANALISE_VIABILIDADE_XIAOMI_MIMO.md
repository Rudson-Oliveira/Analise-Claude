# Análise de Viabilidade — Xiaomi MiMo

> **Data:** 15/06/2026 | **Decisão:** Adotar como ferramenta **auxiliar**, sempre sob régua de custo-benefício
> **Solicitado por:** Rudson Oliveira (CEO) | **Contexto:** complementar o pipeline de IA do n8n Cloud

---

## 🎯 Resumo da decisão

O **Xiaomi MiMo** entra como **mais um auxílio** ao nosso ecossistema de automação —
**não** como substituto dos modelos atuais em produção. A adoção fica condicionada a
**custo-benefício comprovado** em cada caso de uso, via **OpenRouter** (sem
infraestrutura nova).

---

## 1. O que é o Xiaomi MiMo

Família de LLMs **open-source** da Xiaomi, focada em raciocínio, código e fluxos agênticos.
Variantes relevantes (jun/2026):

| Modelo | Params (total / ativos) | Perfil | Observação |
|---|---|---|---|
| MiMo-7B | 7B / 7B | Pequeno, denso | Roda em GPU consumer (~6-8 GB VRAM em 4-bit) |
| MiMo-VL-7B | 7B / 7B | Multimodal (visão) | Exige um pouco mais de recurso |
| **MiMo-V2-Flash** | 309B / 15B (MoE) | Código / agente | **Disponível na OpenRouter** — top open-source em SWE-bench, ~3,5% do custo do Sonnet 4.5 |
| MiMo-V2.5 | 310B / 15B (MoE) | Multimodal (texto/img/vídeo/áudio) | — |
| MiMo-V2.5-Pro | 1,02T / 42B (MoE) | Flagship, 1M de contexto | Próximo de GPT-5.2 / Opus 4.6 |

## 2. Caminhos de adoção

### ❌ Self-hosting (servidor próprio com GPU)
- MiMo-7B roda em GPU consumer, mas é o modelo **mais fraco** da família (abaixo do que já usamos).
- Variantes V2-Flash/V2.5/Pro exigem **clusters multi-GPU de data center** — inviável.
- Não temos infra de GPU (tudo roda em **n8n Cloud**) e o volume não paga o custo fixo.
- **Veredito:** descartado.

### ✅ Via OpenRouter (caminho escolhido)
- **MiMo-V2-Flash já está na OpenRouter** (`xiaomi/mimo-v2-flash`).
- "Instalar" = **trocar a string do modelo** num node HTTP Request (mesmo padrão da migração HuggingFace→OpenRouter).
- Usa a `OPENROUTER_API_KEY` já configurada. **Zero infraestrutura nova.**
- **Veredito:** viável e barato de testar.

## 3. Onde aplicar (e onde NÃO aplicar)

| Caso de uso | Recomendação |
|---|---|
| COCKPIT-07 (triagem inbox, Gemini 2.5 Flash) | 🔒 **Manter** — já cobre bem, baixo custo/latência |
| COCKPIT-08 (briefing diário, Claude Haiku 4.5) | 🔒 **Manter** — idem |
| Workflows de **código/agente** (ex.: orquestrador dinâmico) | 🧪 **POC com `xiaomi/mimo-v2-flash`** — comparar custo×qualidade vs. Haiku 4.5 |
| Qualquer fluxo com **dados clínicos sensíveis** | ⚠️ **Avaliar LGPD/política de dados** do provedor ANTES de enviar conteúdo |

## 4. Regras de adoção (custo-benefício)

1. MiMo é **auxiliar**: só entra onde provar **custo×qualidade** melhor que a opção atual.
2. **Prioridade do projeto continua sendo os modelos Claude mais recentes** via OpenRouter.
3. Testar sempre em **workflow novo e não-sensível** antes de cogitar produção.
4. Nunca apontar dados clínicos a um modelo de terceiros sem checagem de conformidade.

## 5. Próximo passo sugerido

POC isolado: apontar **um** node de um workflow de teste para `xiaomi/mimo-v2-flash`,
medir custo por execução e qualidade, e comparar com o Haiku 4.5. **Não** tocar nos
COCKPIT-07/08 de produção.

---

## 📚 Fontes

- [GitHub — XiaomiMiMo/MiMo](https://github.com/xiaomimimo/mimo)
- [Xiaomi MiMo — Wikipedia](https://en.wikipedia.org/wiki/Xiaomi_MiMo)
- [MiMo-V2-Flash — API & Benchmarks (OpenRouter)](https://openrouter.ai/xiaomi/mimo-v2-flash)
- [VentureBeat — MiMo-V2-Pro](https://venturebeat.com/technology/xiaomi-stuns-with-new-mimo-v2-pro-llm-nearing-gpt-5-2-opus-4-6-performance)
- [Gizmochina — Xiaomi AI/LLMs](https://www.gizmochina.com/2026/06/12/xiaomi-ai-llm-mimo-miclaw-omnivoice-explained/)
- [Requisitos de VRAM para LLMs locais (Plugable)](https://plugable.com/blogs/news/gpu-vram-requirements-for-local-llms-plugable-guide)
