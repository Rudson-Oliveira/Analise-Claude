# Integração — Claude Managed Agents (Anthropic)

> **Status:** 📋 Documentado / avaliado para uso futuro | **Data:** 21/06/2026
> **Decisão:** registrar no ecossistema como **camada opcional de runtime** para agentes
> autônomos de longa duração. **Não** substitui o n8n hoje — entra como "mãos" sob demanda.

## 🎯 O que é

[Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) é um
**serviço gerenciado (hosted) da Anthropic** que roda agentes Claude de longa duração *por você*.
Você deixa de construir o loop do agente, a execução de ferramentas e a infraestrutura de runtime —
tudo isso passa a ser responsabilidade da Anthropic.

A filosofia central é **["desacoplar o cérebro das mãos"](https://www.anthropic.com/engineering/managed-agents)**:
o modelo (o "cérebro") fica separado do ambiente seguro onde o agente executa ações (as "mãos").

- **Lançamento:** beta público em 08/04/2026.
- **Preço:** tarifa normal de tokens da API Claude **+ US$ 0,08 por hora de sessão**.

### Principais características
- Ambiente **sandbox seguro**: o agente lê arquivos, roda comandos, navega na web e executa código,
  com autenticação, execução de ferramentas e gestão de segredos cuidados pela Anthropic.
- Agentes rodam **autonomamente por horas**; sessões **sobrevivem a quedas de conexão**
  (tarefas multi-etapa não recomeçam do zero).
- Otimizações embutidas: **prompt caching**, **compactação de contexto** e afins, para saída
  de alta qualidade e eficiente.

## 🧩 Onde encaixa no nosso ecossistema (multicanal — "canivete suíço")

> **Princípio:** **não travar em um único canal.** O Managed Agents é um *runtime* de
> agente — um "cérebro + mãos" — que deve poder ser **acionado de qualquer canal** e
> **devolver o resultado em qualquer canal**. O n8n é só **um** dos orquestradores possíveis,
> não o dono exclusivo.

Hoje o Claude já entra como **cérebro** via **OpenRouter** dentro do n8n. O Managed Agents
amplia isso para um runtime que pode ser plugado em **vários pontos de entrada e saída**:

```
            CANAIS DE ENTRADA                  RUNTIME                 CANAIS DE SAÍDA
   ┌─────────────────────────────┐                            ┌─────────────────────────────┐
   │ WhatsApp (Evolution API)    │                            │ WhatsApp (Evolution API)    │
   │ Email (Outlook)             │   ┌────────────────────┐   │ Email (Outlook)             │
   │ Notion                      │──▶│  Claude Managed    │──▶│ Notion                      │
   │ Telegram                    │   │  Agents (cérebro   │   │ Google Sheets               │
   │ Google Sheets               │   │  + mãos / sandbox) │   │ Telegram                    │
   │ Webhook / API direta        │   └────────────────────┘   │ Webhook / app / API         │
   │ Claude Code / Desktop (MCP) │            ▲                │ Claude Code / Desktop (MCP) │
   └─────────────────────────────┘            │                └─────────────────────────────┘
                                   orquestração plugável:
                              n8n  •  chamada direta à API  •  MCP
```

### Três formas de acionar (escolher por caso, sem amarrar)
1. **Via n8n** — qualquer trigger n8n (cron, webhook WhatsApp, email, Notion) dispara o agente
   por HTTP Request e recebe o resultado de volta para distribuir nos canais. Bom para fluxos
   já existentes (COCKPIT-*).
2. **Chamada direta à API Claude** — um canal/serviço (app, webhook, microserviço Railway)
   aciona o Managed Agents **sem passar pelo n8n**, quando o n8n não precisa estar no caminho.
3. **Via MCP (Claude Code / Desktop)** — o agente Claude local usa o runtime sob demanda
   (ex.: combinado com o MarkItDown-MCP para análise de documentos).

### Casos no contexto da Hospitalar
- Atendente no **WhatsApp** pede uma análise demorada → agente roda por minutos/horas no runtime
  → resposta volta **no mesmo WhatsApp**, sem prender a sessão do n8n.
- Anexo chega por **Email/Notion** → MarkItDown converte → Managed Agents analisa em lote →
  resultado gravado no **Notion** e resumido no **WhatsApp**.
- Disparo manual via **Claude Code** para uma tarefa pontual de pesquisa longa.

> ⚠️ **Nota de arquitetura:** o Managed Agents é serviço **da Anthropic na nuvem**, acionado via
> **API Claude** (exige `ANTHROPIC_API_KEY`, não via OpenRouter). A camada de **canais**
> (WhatsApp/Email/Notion/Telegram/Sheets) continua sendo responsabilidade de quem orquestra
> (n8n, microserviço ou MCP) — o runtime é **agnóstico de canal** de propósito.

## 🆚 Como se compara com o que já temos

| Aspecto | n8n Cloud (atual) | Claude Managed Agents |
|---|---|---|
| Papel | Orquestração + "mãos" (nodes) | Runtime gerenciado (cérebro + mãos) |
| Melhor para | Fluxos curtos, integrações, cron, webhooks | Tarefas autônomas longas (horas) |
| Integrações WhatsApp/Notion/Sheets/Outlook | ✅ Nativas (nodes) | ❌ Não faz por si |
| Modelo Claude | Via OpenRouter | Via API Claude (direta) |
| Custo extra | — | + US$ 0,08/hora-sessão |

**Conclusão:** abordagens **complementares**, não concorrentes para o nosso caso. O n8n continua
sendo o orquestrador; o Managed Agents fica disponível como runtime sob demanda para jobs pesados.

## ⚙️ Pré-requisitos para ativar (quando/se decidirmos usar)

1. **`ANTHROPIC_API_KEY`** própria (conta Anthropic com acesso ao beta de Managed Agents).
2. Definir o(s) caso(s) de uso que justifiquem o custo por hora-sessão.
3. Escolher o(s) **ponto(s) de acionamento** (não precisa ser só um):
   - **n8n:** HTTP Request node (`specifyBody: "string"` quando houver expressões `{{ }}`)
     para iniciar a sessão e outro para coletar o resultado.
   - **Direto/microserviço:** um endpoint (ex.: Railway) que recebe do canal e chama a API.
   - **MCP:** uso pelo agente Claude (Code/Desktop).
4. Mapear quais ferramentas/sandbox o agente precisa (ex.: leitura de documentos do hospital).
5. Definir, por canal, **como o resultado volta** (WhatsApp, Email, Notion, Sheets, Telegram…).

## 🔒 Segurança

- A `ANTHROPIC_API_KEY` é credencial sensível — **nunca** commitar; usar variável de ambiente n8n.
- Dados enviados ao sandbox saem do nosso ambiente para a infraestrutura da Anthropic — avaliar
  sensibilidade dos dados de saúde (LGPD) antes de processar PII/PHI real.
- Custo por hora-sessão exige **timeouts/limites** claros para evitar sessões longas inadvertidas.

## 📋 Próximos passos

1. Manter como **avaliado/documentado** (sem ativação imediata — não há caso de uso que justifique hoje).
2. Reavaliar quando surgir uma tarefa autônoma longa (ex.: análise em lote de documentos via MarkItDown).
3. Se ativarmos: provisionar `ANTHROPIC_API_KEY` e prototipar o disparo a partir do n8n.

## 🔗 Fontes

- [Scaling Managed Agents: Decoupling the brain from the hands — Anthropic Engineering](https://www.anthropic.com/engineering/managed-agents)
- [Claude Managed Agents overview — Claude API Docs](https://platform.claude.com/docs/en/managed-agents/overview)
