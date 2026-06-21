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

## 🧩 Onde encaixa no nosso ecossistema

Hoje nosso "loop" de agente é o **n8n Cloud**, e o Claude entra como **cérebro** chamado via
**OpenRouter** (ex.: `anthropic/claude-haiku-4-5` no COCKPIT-08). O Managed Agents seria uma
**alternativa de runtime** para um perfil de tarefa que o n8n não atende bem: trabalho autônomo,
longo e exploratório.

```
n8n Cloud (gatilho/orquestração) → dispara job → Claude Managed Agents (cérebro + mãos, por horas)
        → resultado volta ao n8n → Notion / WhatsApp / Sheets / Outlook
```

Casos onde valeria a pena no contexto da Hospitalar:
- Varredura/análise de uma **base grande de documentos** por horas (ex.: combinar com o
  MarkItDown-MCP para pré-processar anexos).
- Pesquisa **multi-etapa autônoma** que ultrapassa o tempo/limite confortável de um workflow n8n.

> ⚠️ **Nota de arquitetura:** o Managed Agents é um serviço **da Anthropic na nuvem**, acionado via
> **API Claude** — não via OpenRouter. Para usá-lo a partir do n8n Cloud seria preciso uma
> `ANTHROPIC_API_KEY` própria e um HTTP Request node chamando a API de Managed Agents. Isso difere
> do nosso padrão atual (Claude via OpenRouter) e adiciona uma segunda relação de billing.

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
3. No n8n: um HTTP Request node (`specifyBody: "string"` quando houver expressões `{{ }}`)
   para iniciar a sessão e outro para coletar o resultado.
4. Mapear quais ferramentas/sandbox o agente precisa (ex.: leitura de documentos do hospital).

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
