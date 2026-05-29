# 🧠 Análise Claude - Contexto e Memória do Projeto
## Hospitalar Soluções em Saúde | Sistema de Automação Completo

> **REPOSITÓRIO DE RESTAURAÇÃO DE CONTEXTO PARA CLAUDE AI**
> Data: 29/05/2026 | Analisado por: Claude Sonnet 4.6

---

## 📋 PARA RESTAURAR CONTEXTO - LEIA PRIMEIRO

Este repositório contém a memória completa do projeto. Ao iniciar nova sessão:
1. Leia este README para contexto geral
2. Leia CONTEXTO.json para dados estruturados (máquina-legível)
3. Leia ANALISE_COMPLETA.md para análise técnica detalhada
4. Próxima ação: ver campo "proximo_passo" no CONTEXTO.json

**PRÓXIMA AÇÃO:** Importar WF-MCC-GET/SET-URL-GS no N8N Local

---

## 🏥 Sobre o Projeto

**Empresa:** Hospitalar Soluções em Saúde
**Proprietário:** Rudson Antonio Ribeiro Oliveira
**WhatsApp:** +55 35 99835-2323

Sistema completo de automação para gestão hospitalar, scraping de conteúdo, IA multi-agente, e publicação em redes sociais.

---

## 📁 Repositórios Analisados (8 repos)

| # | Repositório | Stack | Status |
|---|-------------|-------|--------|
| 1 | [telegram-scraper](https://github.com/Rudson-Oliveira/telegram-scraper) | React+Node.js | ✅ v3.0 |
| 2 | [telegram-scraper-inema-n8n](https://github.com/Rudson-Oliveira/telegram-scraper-inema-n8n) | N8N+Supabase | ✅ Produção |
| 3 | [n8n-workflows-pessoal-2026-01-08](https://github.com/Rudson-Oliveira/n8n-workflows-pessoal-2026-01-08) | N8N+OpenRouter | ⚠️ Sem API Key |
| 4 | [hospitalar-automation](https://github.com/Rudson-Oliveira/hospitalar-automation) | Playwright+Python | 🔄 Estrutura |
| 5 | [MAKE-25-01-26](https://github.com/Rudson-Oliveira/MAKE-25-01-26) | Make.com | ✅ 11 cenários |
| 6 | [hospitalar-multi-agent-system](https://github.com/Rudson-Oliveira/hospitalar-multi-agent-system) | N8N+Ollama | ❌ MCC ausente |
| 7 | [n8n-workflows](https://github.com/Rudson-Oliveira/n8n-workflows) | N8N 35wfs backup | ✅ OK |
| 8 | [hospitalar-ia-evolutiva-projeto-completo](https://github.com/Rudson-Oliveira/hospitalar-ia-evolutiva-projeto-completo) | N8N+LLM | 🔄 Só docs |

---

## ⚠️ Problemas Críticos (Resolver Primeiro)

### 🔴 CRÍTICO 1: Sistema Multi-Agente Quebrado
**Repo:** hospitalar-multi-agent-system
**Problema:** WF-MCC-GET-URL-GS e WF-MCC-SET-URL-GS não foram importados no N8N Local
**Impacto:** O Orquestrador Dinâmico falha ao tentar buscar URL do Ollama
**Solução:**
1. Baixar os JSON dos workflows do repo
2. Importar no N8N Local (localhost:5678)
3. Configurar credenciais do Google Sheets
4. Testar: POST http://localhost:5678/webhook/orquestrador-dinamico

### 🔴 CRÍTICO 2: Revisão IA Inativa
**Repo:** n8n-workflows-pessoal-2026-01-08
**Problema:** API Key do OpenRouter não configurada
**Solução:**
1. Criar conta em openrouter.ai
2. Gerar API Key (sk-or-v1-XXXXX)
3. Abrir workflow 21-INFRA-Backup-GitHub no N8N
4. Editar node HTTP Request → Authorization → inserir a key

### 🔴 CRÍTICO 3: Credenciais Hardcoded
**Repo:** telegram-scraper-inema-n8n
**Problema:** Supabase URL e Service Role Key hardcoded no node Code
**Risco:** Exposição de credenciais no código
**Solução:** Mover para N8N Credentials ou variáveis de ambiente

---

## 📊 Infraestrutura Atual

```
N8N Cloud (rudsonoliveira2323.app.n8n.cloud)
  39 workflows ativos
  Categorias: CORE, INFRA, INT, OP, MAS, ORCAMENTOS

N8N Local (Docker - localhost:5678)
  Serviços: n8n, ollama:11434, postgres, mongo-express
  Problema: 2 workflows MCC ausentes

Make.com (us2.make.com - Org 440797)
  11 cenários - Schedule 15min
  Integrações: Google, Placid, OpenAI, AssemblyAI, Meta

Supabase
  Tabela principal: telegram_messages
  Campos: id, chat_id, text, category, sentiment, extracted_*

GitHub (Rudson-Oliveira)
  Backup automático: 03:00 Brasília
  Endpoint: /webhook/backup-github
```

---

## 🗺️ Mapa de Workflows N8N Cloud (39 total)

**CORE (4):** Criador Universal, Sites Vitrine, Vision AI, Auto-Import
**INFRA (5):** Master Orquestrador, Ollama Gateway, Triggers Central, Diagnóstico, Backup GitHub
**INT (5):** Webhook Bridge, Telegram Import, Telegram Scraper, e63 Ticketing, INEMA Scraper
**OP (4):** Chatbot Atendimento, Gestor Agendamentos, Notificações Pacientes, Assistente Virtual
**MAS (7):** Gerenciador, Health-Check, Inicializador, Orquestrador Dinâmico, Multi-Agente, Ollama, OpenAI
**ORCAMENTOS (4):** Completo, Local, Básico
**OUTROS:** ~10 workflows diversos

---

## 📅 Plano de Ação Completo

### FASE 1 - AGORA (Crítico)
- [ ] Importar WF-MCC-GET-URL-GS no N8N Local
- [ ] Importar WF-MCC-SET-URL-GS no N8N Local
- [ ] Configurar Google Sheets credentials no N8N Local
- [ ] Testar WF-ORQUESTRADOR-DINAMICO end-to-end
- [ ] Inserir API Key OpenRouter no 21-INFRA-Backup-GitHub
- [ ] Mover credenciais Supabase para env vars N8N

### FASE 2 - Implementações
- [ ] Criar 9 workflows N8N para hospitalar-ia-evolutiva
- [ ] Configurar Ngrok para N8N Local
- [ ] Teste completo: Ngrok → Cloud → Local → Ollama
- [ ] Implementar fallback Ollama → OpenAI

### FASE 3 - Robustez
- [ ] HEALTH-CHECK a cada 5 minutos
- [ ] Tratamento de erros centralizado Make.com
- [ ] Dashboard monitoramento unificado
- [ ] Revogar token Telegram exposto no README

### FASE 4 - Autonomia Total
- [ ] Conectar sistema vendas via API
- [ ] Ativar feedback loop LLM
- [ ] Atingir Nível 3 de autonomia
- [ ] ROI alvo: R$ 170.000/ano

---

## 🔗 Links Importantes

| Recurso | URL |
|---------|-----|
| N8N Cloud | https://rudsonoliveira2323.app.n8n.cloud |
| WhatsApp Evolution | https://rudsonoliveira2323.app.n8n.cloud/webhook/whatsapp-evolution |
| Backup Webhook | https://rudsonoliveira2323.app.n8n.cloud/webhook/backup-github |
| Restauração Webhook | https://rudsonoliveira2323.app.n8n.cloud/webhook/restaurar-workflow |
| Backup Workflows | https://github.com/Rudson-Oliveira/n8n-workflows |
| Multi-Agent System | https://github.com/Rudson-Oliveira/hospitalar-multi-agent-system |
| IA Evolutiva | https://github.com/Rudson-Oliveira/hospitalar-ia-evolutiva-projeto-completo |
| Make.com | https://us2.make.com/440797/scenarios |

---

## 📂 Arquivos neste Repositório

- **README.md** (este arquivo) - Visão geral e restauração de contexto
- **CONTEXTO.json** - Dados estruturados máquina-legível para Claude
- **ANALISE_COMPLETA.md** - Análise técnica detalhada de todos os workflows

---

*Gerado por Claude Sonnet 4.6 | 29/05/2026*
*Repositório: https://github.com/Rudson-Oliveira/Analise-Claude*
