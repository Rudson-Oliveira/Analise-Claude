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
- **GitHub:** https://github.com/Rudson-Oliveira/Analise-Claude
- **Stack:** n8n Cloud + OpenRouter + Evolution API + Notion + Google Sheets + Microsoft Outlook

## 🔴 Primeira ação em toda sessão (restaurar contexto)

1. Leia **[CONTEXTO.json](./CONTEXTO.json)** — estado estruturado e máquina-legível (**fonte da verdade**, versão atual = v4.2).
2. Leia **[README.md](./README.md)** — visão humana do estado atual.
3. Confira o checkpoint mais recente (`CHECKPOINT_*.md`).
4. Só então proponha/execute o próximo passo. **Não altere nada antes de restaurar o contexto.**

## 🔌 Como me conectar (bootstrap)

O dono (ou um agente) abre uma sessão já contextualizada com o script PowerShell:

```powershell
# Interativo (branch main):
.\scripts\iniciar-claude.ps1

# Na branch de trabalho atual:
.\scripts\iniciar-claude.ps1 -Branch claude/installation-feasibility-k0q8lx

# Headless (agente coleta o resumo e encerra):
.\scripts\iniciar-claude.ps1 -ApiKey "sk-ant-..." -Headless

# Retomar a última conversa:
.\scripts\iniciar-claude.ps1 -Resume
```

O script instala o CLI se faltar, sincroniza o repo na branch certa, cuida da
autenticação e me abre já com um prompt que manda restaurar o contexto.

## 📁 Mapa dos arquivos

| Arquivo | Papel |
|---|---|
| `CONTEXTO.json` | Estado estruturado da sessão (versão atual = fonte da verdade) |
| `README.md` | Contexto humano-legível |
| `ANALISE_COMPLETA.md` | Análise inicial dos 50+ workflows |
| `ANALISE_VIABILIDADE_XIAOMI_MIMO.md` | Decisão: MiMo como auxiliar via OpenRouter |
| `CHECKPOINT_*.md` | Checkpoints datados de sessões anteriores |
| `PROGRESSO_FASE1.md` | Progresso da Fase 1 |
| `scripts/iniciar-claude.ps1` | Bootstrap PowerShell para abrir uma sessão Claude Code já contextualizada |
| `.claude/skills/` + `.agents/skills/` | Skills Claude Code versionadas (ver seção Skills) |

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

## 🧩 Skills do Claude Code (versionadas no repo)

Instaladas via CLI `skills` em `.agents/skills/` (arquivos) + `.claude/skills/`
(symlinks), rastreadas em `skills-lock.json`. Todas avaliadas como **Safe** pelo scanner.

| Skill | Fonte | Uso |
|---|---|---|
| `brainstorming` | obra/superpowers | Refinar ideias/design antes de executar |
| `ai-seo` | coreyhaines31/marketingskills | SEO para buscas de IA / divulgação |
| `ads` | agricidaniel/claude-ads | Auditoria de campanhas de anúncios |
| `landing-page-design` | inferen-sh/skills | Design de landing pages |

> As 3 últimas são de marketing — usar só quando o assunto for divulgação da
> Hospitalar, não no pipeline clínico.

## 🧭 Decisões estratégicas

- **Xiaomi MiMo (15/06/2026):** adotado apenas como **auxiliar**, sob custo-benefício,
  via OpenRouter (`xiaomi/mimo-v2-flash`). **Sem self-hosting.** Não substitui os
  modelos em produção. Detalhes em `ANALISE_VIABILIDADE_XIAOMI_MIMO.md`.

## 🌿 Fluxo de Git / commits

- **Branch de trabalho atual:** `claude/installation-feasibility-k0q8lx` (PR #7).
- **Nunca** commitar direto na `main` sem permissão explícita.
- `git push -u origin <branch>`; após push, garantir que existe um **PR (draft)**.
- Mensagens de commit claras; **nunca** incluir API keys/tokens no histórico.

## ⚠️ Dados sensíveis (saúde / LGPD)

Lidamos com dados clínicos. Antes de enviar qualquer conteúdo sensível a modelos
de terceiros, avaliar **conformidade LGPD** e a política de dados do provedor.

## ✅ Como manter este projeto saudável

- **Ao terminar mudanças relevantes:** atualize `CONTEXTO.json` (bump de versão) e o `README.md`, e registre um checkpoint se a sessão foi grande.
- **Idioma:** responda em **português (BR)** — o proprietário escreve em PT-BR.
- **Segredos:** nunca commite API keys reais. Use placeholders e variáveis de ambiente.
- **Tom:** seja objetivo e proativo; quando concluir algo verificável, afirme com clareza (sem rodeios).
