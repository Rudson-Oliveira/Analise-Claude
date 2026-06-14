# Instruções para o Claude — Projeto Análise-Claude

> Orientação para qualquer agente (Claude Desktop/Code/Web) que assuma este
> projeto. Conecte o MCP de contexto (`analise-context-mcp`) e siga este guia.
> Objetivo: **performar com consistência, sem repetir erros e sem reperguntar o
> que já está na memória.**

## 1. Quem é o cliente

- **Empresa:** Hospitalar Soluções em Saúde
- **CEO:** Rudson Antonio Ribeiro Oliveira — +55 35 99835-2323 · rud.pa@hotmail.com
- **n8n Cloud:** https://rudsonoliveira2323.app.n8n.cloud
- **Idioma:** responda sempre em **português (BR)**, tom direto e prático.

## 2. Stack do projeto

n8n Cloud · OpenRouter · Evolution API (WhatsApp) · Notion · Google Sheets ·
Microsoft Outlook. Workflows seguem o padrão **COCKPIT-XX**.

## 3. Como iniciar TODA sessão (ritual de contexto)

1. `restaurar_contexto` → carrega o `CONTEXTO.json` (estado atual).
2. `get_project_summary` → versão, próximo passo, pendências, plataformas.
3. `get_pending_tasks` → o que está aberto e a prioridade.
4. `search_context "<tema>"` → antes de mexer em algo, confira histórico.

Gatilho equivalente do usuário: *"leia o documento no GitHub Analise-Claude e
continue"*.

## 4. Regras de ouro para performar

- **Aja quando tiver contexto.** Não repergunte o que está na memória; seja
  conciso e proponha o próximo passo concreto.
- **Cheque antes de alterar.** Use `search_context` em "erros corrigidos" para
  não repetir armadilhas (ver §5).
- **Confirme ações de risco.** Antes de editar/excluir workflow, publicar post ou
  qualquer ação difícil de reverter, descreva o que vai mudar e peça confirmação.
- **Segredos são sagrados.** Nunca exponha tokens/chaves em commits, logs ou
  chat versionado. Use variáveis de ambiente.
- **Feche com checkpoint.** Ao terminar, proponha atualizar `CONTEXTO.json` +
  `README.md` no formato existente (nova versão, conquistas, pendências).

## 5. Erros já resolvidos — NÃO repita

| Sintoma | Causa | Correção |
|---|---|---|
| `PUT /rest/workflows` → 404 | endpoint errado | usar **PATCH** |
| rename de node quebra conexões | renomear node | **manter o nome original**, só mudar parâmetros |
| activate → 400 "versionId required" | falta versionId | buscar workflow, extrair `versionId`, enviar no body |
| `JSON syntax error position 593` (COCKPIT-07) | `specifyBody: json` com expressões `{{ }}` | trocar para `specifyBody: "string"` |

## 6. Pendências conhecidas (confirme em `get_pending_tasks`)

- 🔴 `OPENAI_API_KEY` — Whisper (transcrição de áudio do WhatsApp).
- 🔴 `EVOLUTION_API_KEY` — menu WhatsApp (1=Manter / 2=Dormir / 3=Excluir).
- 🟡 Teste do subfluxo de áudio ponta-a-ponta.
- 🟢 Supabase hardcoded em `telegram-scraper-inema-n8n`.
- 🟢 Túnel ngrok para o n8n local.

## 7. MCPs disponíveis neste repositório

- **`analise-context-mcp`** (`context-mcp/`) — esta memória. Grátis, offline.
- **`metricool-mcp-swiss`** (`metricool-mcp/`) — Metricool (requer token pago).
  Para uso **grátis** do Metricool, conecte o conector oficial
  `https://ai.metricool.com/mcp` no Claude Desktop (OAuth).

Instalação rápida no Windows: `scripts/connect-claude-desktop.ps1`.
