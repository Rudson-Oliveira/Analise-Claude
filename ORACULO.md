# 🔮 ORÁCULO — Base de Conhecimento Completa do Projeto Análise-Claude

> **Para qualquer agente Claude que ler isto:** este é o conhecimento COMPLETO do
> projeto. Lendo este documento (ou chamando a ferramenta `oraculo` do MCP de
> contexto) você assume o projeto inteiro — empresa, stack, histórico, decisões,
> erros já resolvidos e estado atual — sem precisar reconstruir nada. Responda em
> **português (BR)**, de forma direta e acionável.
>
> **Versão:** 6.0 · **Atualizado:** 26/06/2026 · **Sessões:** 6 (memória unificada com as sessões paralelas)

---

## 1. Identidade do projeto

| Campo | Valor |
|---|---|
| Empresa | **Hospitalar Soluções em Saúde** |
| CEO / dono | Rudson Antonio Ribeiro Oliveira |
| Contato | +55 35 99835-2323 · rud.pa@hotmail.com |
| Repositório | https://github.com/Rudson-Oliveira/Analise-Claude |
| n8n Cloud | https://rudsonoliveira2323.app.n8n.cloud |

**O que é o projeto:** um sistema de **automação de atendimento e produtividade**
construído em **n8n Cloud**, com IA via **OpenRouter**, mensageria **WhatsApp
(Evolution API)**, e integrações com **Notion, Google Sheets e Microsoft
Outlook**. Os fluxos seguem o padrão de nomenclatura **COCKPIT-XX** e **WF-XXX**.

Este repositório (`Analise-Claude`) é a **memória** do projeto: guarda o estado,
os checkpoints e o conhecimento para que cada nova conversa continue de onde a
anterior parou.

---

## 2. Stack e plataformas

- **n8n Cloud** — orquestração dos workflows (50+ mapeados).
- **OpenRouter** — gateway de modelos de IA (substituiu o HuggingFace).
  - `OPENROUTER_API_KEY` ✅ configurada.
- **Evolution API** — WhatsApp (envio/recebimento). `EVOLUTION_API_KEY` ❌ pendente.
- **OpenAI Whisper** — transcrição de áudio. `OPENAI_API_KEY` ❌ pendente.
- **Notion, Google Sheets, Microsoft Outlook** — dados e e-mail.
- **Metricool** — social media analytics/agendamento (conectado na sessão 5).

---

## 3. Linha do tempo (sessão a sessão)

### Sessão 1 — Diagnóstico
Análise completa de 50+ workflows do n8n. Mapeamento de integrações ativas e
pendentes. Criação do `CONTEXTO.json` v1.0 e do README.

### Sessão 2 — Orquestração
`WF-ORQUESTRADOR-DINAMICO` testado end-to-end (exec #21404 SUCCESS).
`AGENTE_LOCAL` registrado via staticData e webhook. `WF-MCC-SET-URL` publicado.

### Sessão 3 — Migração HuggingFace → OpenRouter
`OPENROUTER_API_KEY` cadastrada. COCKPIT-07 migrado para `google/gemini-2.5-flash-preview`;
COCKPIT-08 para `anthropic/claude-haiku-4-5` (exec #21415 SUCCESS); COCKPIT-09 pulado.

### Sessão 4 — Correção COCKPIT-07
Erro `JSON syntax error position 593` diagnosticado e corrigido (`specifyBody`
json→string). COCKPIT-07 reativado e testado (exec #21422 SUCCESS).

### Sessão 5 — Infraestrutura MCP + Metricool (esta)
- Criados **dois servidores MCP** (ver §5) na branch `claude/metricool-mcp-server-pr6m40` (**PR #4**).
- Criados **scripts PowerShell** para instalar/conectar no Claude Desktop.
- **Metricool conectado** via MCP; marca validada (ver §6).
- Criados `INSTRUCOES_CLAUDE.md` e este `ORACULO.md`.

---

## 4. Workflows-chave (n8n)

| Workflow | ID | Estado |
|---|---|---|
| COCKPIT-07 (Inbox WhatsApp/Email/Notion) | `acWQbkOkisdpzryy` | ✅ ativo, corrigido · modelo gemini-2.5-flash-preview |
| COCKPIT-08 (Briefing diário, cron 07h) | `CoDTbFiy8g1ctkmO` | ✅ ativo · modelo claude-haiku-4-5 |
| COCKPIT-09 (Helper) | `ZQLHgsgDppId9qoe` | ⏭️ sem lógica IA |
| WF-ORQUESTRADOR-DINAMICO | — | ✅ ativo |
| WF-MCC-SET-URL | — | ✅ ativo |
| COCKPIT-05-POLLING (Notion→WhatsApp) | — | ✅ ativo |

---

## 5. Infraestrutura MCP criada (branch `claude/metricool-mcp-server-pr6m40`, PR #4)

### 5.1 `analise-context-mcp` — a memória/oráculo (pasta `context-mcp/`)
Servidor MCP que entrega ESTE conhecimento a qualquer agente. **Grátis e offline**
(lê os arquivos do repositório).

Ferramentas: `oraculo` (conhecimento completo numa chamada), `restaurar_contexto`,
`get_project_summary`, `list_documents`, `read_document`, `search_context`,
`get_pending_tasks`. Resources: `analise://contexto`, `analise://resumo`.
Prompt: `continuar_projeto`.

### 5.2 `metricool-mcp-swiss` — canivete suíço do Metricool (pasta `metricool-mcp/`)
Superset do MCP oficial (`metricool/mcp-metricool`) com 30 ferramentas, cliente
resiliente (retry/backoff, erros estruturados), `normalize_media_url`,
`find_brand`, `metricool_request` (qualquer endpoint). **Requer token de API
(plano Advanced).** Alternativa grátis: conector OAuth `https://ai.metricool.com/mcp`.

### 5.3 Scripts (pasta `scripts/`)
- `bootstrap.ps1` — one-shot: clona/atualiza + instala + registra no Claude Desktop.
- `connect-claude-desktop.ps1` — registra os MCPs no `claude_desktop_config.json`.

**Instalar no Windows:**
```powershell
cd $HOME\Documents\Analise-Claude; git pull
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```
Depois **reiniciar o Claude Desktop**.

---

## 6. Conexão Metricool (sessão 5)

| Campo | Valor |
|---|---|
| userId | `4927314` |
| Marca | **HospitaLar Soluções em Saúde** |
| blogId / brandId | `6395876` |
| Timezone | `America/Sao_Paulo` |
| Criada em | 13/06/2026 |
| Rede conectada | Facebook (page) |
| Status métricas | Sync pendente (conta nova) — 1ª leitura 19/06 deu tudo 0 |

**Importante:** o MCP **oficial remoto** (`ai.metricool.com/mcp`) funciona por
**OAuth/login em qualquer plano (inclusive free)** — não precisa do token pago. O
token só é necessário para o servidor self-hosted (`metricool-mcp-swiss`).

---

## 6.1 Ecossistema do projeto (outras sessões paralelas — já na `main`)

Além dos nossos MCPs, sessões paralelas adicionaram (estão na `main`, integrados no v6.0):

- **MarkItDown-MCP** (Microsoft, open-source) — converte PDF/Word/Excel/PPT/imagem/áudio/HTML para Markdown limpo para LLM (`convert_to_markdown(uri)`). Encaixe: pré-processar anexos no COCKPIT-07 antes do OpenRouter. Status: documentado (`INTEGRACAO_MARKITDOWN_MCP.md`), aguardando configuração no cliente. Roda local (STDIO/Docker) — não conecta direto ao n8n Cloud.
- **Claude Managed Agents** (Anthropic, hosted) — runtime gerenciado para agentes autônomos de longa duração (sandbox: arquivos, comandos, web, código). Beta público 08/04/2026. Exige `ANTHROPIC_API_KEY` própria (não via OpenRouter). Status: documentado/avaliado (`INTEGRACAO_CLAUDE_MANAGED_AGENTS.md`), sem ativação imediata.
- **Frontend visual** — `frontend/index.html` (HTML autocontido), painel multicanal do ecossistema. Publicável no GitHub Pages. Workflow de deploy em `.github/workflows/deploy-pages.yml`.
- **`CLAUDE.md`** — orientação do projeto para Claude Code (Dynamic Workflows).

---

## 7. ⚠️ Erros já resolvidos — NÃO repita

| Erro | Causa | Correção |
|---|---|---|
| `PUT /rest/workflows` → 404 | endpoint errado | usar **PATCH** |
| rename de node quebra conexões | renomear node | **manter nome original**, só mudar params |
| activate → 400 "versionId required" | falta versionId | buscar workflow, extrair `versionId`, enviar no body |
| `JSON syntax error position 593` (COCKPIT-07) | `specifyBody: json` com `{{ }}` | trocar para `specifyBody: "string"` |
| PS 5.1 `Split-Path: string vazia` | `$PSScriptRoot` vazio no param default | resolver RepoPath no corpo do script |

---

## 8. Pendências atuais (prioridade)

- 🔴 **`OPENAI_API_KEY`** — Whisper (transcrição de áudio WhatsApp).
- 🔴 **`EVOLUTION_API_KEY`** — menu WhatsApp (1=Manter / 2=Dormir / 3=Excluir).
- 🟡 **Sync Metricool** — revalidar métricas da marca 6395876 após 24–48h.
- 🟡 **Teste subfluxo de áudio** ponta-a-ponta.
- 🟡 **Merge do PR #4** (MCPs + scripts).
- 🟢 Supabase hardcoded em `telegram-scraper-inema-n8n`.
- 🟢 Túnel ngrok para o n8n local.

**Próximo passo macro:** FASE 2 — configurar `OPENAI_API_KEY` + `EVOLUTION_API_KEY`
para ativar o subfluxo de áudio do WhatsApp.

---

## 9. Como um novo agente assume o projeto

1. **Conecte** o `analise-context-mcp` (via `scripts/bootstrap.ps1` no Desktop).
2. Chame **`oraculo`** → recebe tudo isto em uma resposta estruturada.
3. Apresente o resumo (empresa, próximo passo, pendências 🔴) e pergunte por onde seguir.
4. Antes de alterar qualquer workflow, use **`search_context`** no histórico de erros (§7).
5. Ao fechar a sessão, **proponha atualizar** `CONTEXTO.json` + `ORACULO.md` (novo checkpoint).

> Gatilho equivalente do usuário: *"leia o documento no GitHub Analise-Claude e continue"*.

---

## 10. Regras de ouro

- **Aja quando tiver contexto.** Não repergunte o que está na memória.
- **Confirme ações de risco** (editar/excluir workflow, publicar post) antes de executar.
- **Segredos são sagrados** — nunca exponha tokens/chaves em commits, logs ou chat versionado.
- **Feche com checkpoint** — deixe a memória sempre atualizada para o próximo agente.
