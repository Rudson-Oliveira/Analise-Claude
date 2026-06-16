# CLAUDE.md — Orientação do Projeto

> Este arquivo é lido automaticamente pelo Claude Code no início de cada sessão
> (CLI e web). Mantenha-o curto, factual e atualizado. É a minha "orientação"
> para performar bem neste projeto.

## 🎯 O que é este repositório

Este repo **não tem código de aplicação** — ele é a **memória / contexto** do
projeto de automação da **Hospitalar Soluções em Saúde**. O trabalho real
acontece no **n8n Cloud**; aqui ficam os checkpoints, o estado estruturado e o
histórico de decisões para retomar qualquer sessão sem perder contexto.

- **Proprietário:** Rudson Antonio Ribeiro Oliveira (CEO)
- **Contato:** +55 35 99835-2323 | rud.pa@hotmail.com
- **n8n Cloud:** https://rudsonoliveira2323.app.n8n.cloud
- **Stack:** n8n Cloud + OpenRouter + Evolution API + Notion + Google Sheets + Microsoft Outlook

## 🔴 Primeira ação em toda sessão (restaurar contexto)

1. Leia **[CONTEXTO.json](./CONTEXTO.json)** — estado estruturado e máquina-legível (fonte da verdade).
2. Leia **[README.md](./README.md)** — visão humana do estado atual.
3. Confira o checkpoint mais recente (`CHECKPOINT_*.md`).
4. Só então proponha/execute o próximo passo.

## 📁 Mapa dos arquivos

| Arquivo | Papel |
|---|---|
| `CONTEXTO.json` | Estado estruturado da sessão (versão atual = fonte da verdade) |
| `README.md` | Contexto humano-legível |
| `ANALISE_COMPLETA.md` | Análise inicial dos 50+ workflows |
| `CHECKPOINT_*.md` | Checkpoints datados de sessões anteriores |
| `PROGRESSO_FASE1.md` | Progresso da Fase 1 |
| `INTEGRACAO_MARKITDOWN_MCP.md` | Integração do MarkItDown-MCP (Microsoft) — arquivos → Markdown para LLM |
| `.mcp.json` | Config MCP do Claude Code (servidor `markitdown` pronto para uso) |
| `scripts/iniciar-claude.ps1` | Bootstrap PowerShell para abrir uma sessão Claude Code já contextualizada |

## 🧰 Ferramentas / MCP disponíveis (use antes de pedir algo manual)

Quando a tarefa for **agir no sistema** (não só editar a memória), prefira as ferramentas:

- **n8n (MCP oficial)** — buscar/criar/editar/validar/ativar workflows direto no n8n Cloud
  (COCKPIT-* e WF-*). Siga o fluxo do MCP: ler SDK → sugerir nodes → validar → criar.
- **GitHub (MCP)** — PRs, issues, CI e comentários no repo `Rudson-Oliveira/Analise-Claude`.
- **MarkItDown (MCP, local)** — `convert_to_markdown(uri)` p/ PDF/Word/Excel/imagem → Markdown.
- **Microsoft Learn / docs** — documentação oficial Microsoft/Azure/Outlook quando necessário.

> Antes de dizer "não tenho acesso", **procure a ferramenta** — muitos MCPs carregam sob demanda.

## 🌿 Fluxo Git (branch + PR)

- **Desenvolva na branch de trabalho** indicada (ex.: `claude/system-integration-check-*`);
  não commite direto na `main` sem permissão.
- **Push:** `git push -u origin <branch>`; em falha de rede, retry com backoff (2s/4s/8s/16s).
- **Após o push, abra sempre um PR em rascunho (draft)** se ainda não existir.
- **Idioma/segredos:** mensagens claras em PT-BR; nunca credenciais/tokens no histórico.

## ⚙️ Convenções técnicas do n8n (lições já aprendidas — NÃO repetir erros)

- **Editar workflow:** use **PATCH** em `/rest/workflows/:id`. **PUT retorna 404** (HTML).
- **Renomear node:** **não renomeie** — manter o nome original do node, alterar só os parâmetros (rename quebra as conexões).
- **Ativar workflow:** buscar o workflow primeiro, extrair o `versionId` e passá-lo no body do `activate` (senão dá 400 "versionId required").
- **HTTP Request com expressões n8n `{{ $json.x }}`:** usar `specifyBody: "string"`, **nunca `"json"`** (json valida como JSON puro e quebra com erro de sintaxe).
- **Modelos de IA:** preferir sempre os modelos Claude mais recentes (ex.: `anthropic/claude-haiku-4-5`) via OpenRouter quando aplicável.

## 🔑 Variáveis n8n

| Variável | Status |
|---|---|
| `OPENROUTER_API_KEY` | ✅ Configurado |
| `OPENAI_API_KEY` | ❌ Pendente (Whisper — transcrição de áudio WhatsApp) |
| `EVOLUTION_API_KEY` | ❌ Pendente (menu WhatsApp 1=Manter/2=Dormir/3=Excluir) |

## 📋 Próximos passos (Fase 2)

1. Configurar `OPENAI_API_KEY` e `EVOLUTION_API_KEY`.
2. Testar o subfluxo de áudio WhatsApp: `áudio → Whisper → OpenRouter → resposta`.
3. Verificar o node 7 do COCKPIT-07 (alerta URGENTE WhatsApp depende de `EVOLUTION_API_KEY`).

## ✅ Como manter este projeto saudável

- **Ao terminar mudanças relevantes:** atualize `CONTEXTO.json` (bump de versão) e o `README.md`, e registre um checkpoint se a sessão foi grande.
- **Idioma:** responda em **português (BR)** — o proprietário escreve em PT-BR.
- **Segredos:** nunca commite API keys reais. Use placeholders e variáveis de ambiente.
- **Commits/PRs:** mensagens claras e objetivas; nada de credenciais ou tokens no histórico.
