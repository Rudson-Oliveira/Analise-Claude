# CHECKPOINT 2 - 29/05/2026 - Fase 1 Continuação

## 🔄 PARA RESTAURAR CONTEXTO
Ao iniciar nova sessão, leia:
1. https://github.com/Rudson-Oliveira/Analise-Claude/blob/main/CHECKPOINT_29052026_2.md (ESTE ARQUIVO - mais recente)
2. https://github.com/Rudson-Oliveira/Analise-Claude/blob/main/ANALISE_COMPLETA.md (análise técnica completa)

---

## 🚨 BLOQUEIO CRÍTICO: EXECUTION LIMIT N8N CLOUD

### Status: 2.500/2.500 execuções em Maio 2026 - LIMITE ATINGIDO
- O N8N Cloud gratuito tem limite de 2.500 execuções/mês
- Limite foi consumido pelas 9.345 execuções em erro do WF-HEALTH-CHECK-AGENTES (antes do nosso fix)
- **Todos os workflows retornam "Execution limit reached"**
- **Reset do contador: 01/06/2026 (daqui 3 dias)**
- Ação necessária: Aguardar reset OU fazer upgrade do plano em https://app.n8n.cloud

---

## ✅ PROGRESSO DESTA SESSÃO (FASE 1 - FASE 2 INÍCIO)

### Fixes Completados:
1. ✅ WF-HEALTH-CHECK-AGENTES (ID: 9arDgUsepPgKE2K6) - FIXADO + REATIVADO
   - Fix: throw new Error → return graceful when no agents registered
   - Status: ATIVO (mas bloqueado por execution limit até 01/06)

2. ✅ WF-MCC-GET-URL-GS (ID: 2fuDZ6gYLsRxQM93) - CRIADO + ATIVADO
   - Webhook: GET /webhook/mcc/get-url?service_name=XXX
   - Retorna URL do agente do Google Sheets MCC_CONFIG
   - Google Sheets: 1-rRo3CAb2QunpNJfsAzqYm2lyqmRGsi_nyYnS_FqcDA (aba MCC_CONFIG)
   - Credencial: "Google Sheets account" (iWwYR5lhrrUABiru)

3. ✅ WF-MCC-SET-URL (ID: MIo8VUzGX77YJuSq) - FIXADO + ATIVADO
   - Problema: usava n8n-nodes-base.dataTables (node não reconhecido em n8n@2.21.8)
   - Fix: Substituído por fluxo Webhook → Code (validação) → Google Sheets (appendOrUpdate) → RespondToWebhook
   - Webhook: POST /webhook/mcc/set-url
   - Body esperado: { service_name, url, description?, is_active? }
   - Status: ATIVO (mas bloqueado por execution limit até 01/06)

4. ✅ WF-ORQUESTRADOR-DINAMICO (ID: vZjIt5q0Nh9pRic4) - JÁ ESTAVA ATIVO
   - 9 nodes: Webhook → Classificador → If → Preparar → HTTP → Processar → If → Resposta
   - Chama agente via URL do MCC (dependente do MCC-GET-URL)
   - Status: ATIVO

### Pendente:
- [ ] Verificar WF-HEALTH-CHECK-AGENTES - AINDA FALHANDO (execution limit, não bug de código)
- [ ] Configurar planilha MCC_CONFIG com entrada AGENTE_LOCAL
- [ ] Adicionar OpenRouter API Key no 21-INFRA-Backup-GitHub
- [ ] FASE 2: Implementar 9 workflows do hospitalar-ia-evolutiva

---

## 📊 ESTADO ATUAL N8N CLOUD

### Workflows Críticos - Status:
| ID | Nome | Status | Notas |
|---|---|---|---|
| 9arDgUsepPgKE2K6 | WF-HEALTH-CHECK-AGENTES | ✅ ATIVO | Código fixado. Bloqueado por exec limit |
| 2fuDZ6gYLsRxQM93 | WF-MCC-GET-URL-GS | ✅ ATIVO | Criado nessa sessão. Bloqueado por exec limit |
| MIo8VUzGX77YJuSq | WF-MCC-SET-URL | ✅ ATIVO | Fixado (dataTables→Sheets). Bloqueado por exec limit |
| vZjIt5q0Nh9pRic4 | WF-ORQUESTRADOR-DINAMICO | ✅ ATIVO | Já estava ativo |
| QazJlHJIbIfaSfFI | 21-INFRA-Backup-GitHub | ❓ Verificar | Precisa OpenRouter API Key |

### Plano N8N Cloud:
- Plano: Free (2.500 execuções/mês)
- Consumo Maio: 2.500/2.500 (100%)
- Reset: 01/06/2026
- URL Dashboard: https://app.n8n.cloud/dashboard

---

## 🗂️ GOOGLE SHEETS MCC_CONFIG

### Planilha:
- ID: 1-rRo3CAb2QunpNJfsAzqYm2lyqmRGsi_nyYnS_FqcDA
- Aba: MCC_CONFIG
- Credencial N8N: "Google Sheets account" (iWwYR5lhrrUABiru)

### Estrutura esperada (colunas):
| service_name | url | description | is_active | updated_at |
|---|---|---|---|---|
| AGENTE_LOCAL | http://localhost:5678/webhook/agente-local | Agente N8N Local com Ollama | true | (data) |
| AGENTE_GPT4 | https://... | OpenAI GPT-4 | true | (data) |

### Para adicionar AGENTE_LOCAL via webhook (após reset 01/06):
```bash
curl -X POST https://rudsonoliveira2323.app.n8n.cloud/webhook/mcc/set-url \
  -H "Content-Type: application/json" \
  -d '{"service_name":"AGENTE_LOCAL","url":"http://localhost:5678/webhook/agente-local","description":"Agente N8N Local com Ollama (Llama3.2)","is_active":true}'
```

---

## 🔧 API TÉCNICA N8N CLOUD

### Endpoints (usa cookie de sessão):
- Listar workflows: GET /rest/workflows?limit=100
- Fetch workflow: GET /rest/workflows/{id}
- Update workflow: PATCH /rest/workflows/{id}
- Ativar: POST /rest/workflows/{id}/activate  (body: {versionId: "..."})
- Desativar: POST /rest/workflows/{id}/deactivate (body: {versionId: "..."})
- Listar execuções: GET /rest/executions?workflowId={id}&limit=5
- Listar credenciais: GET /rest/credentials

### Credenciais disponíveis (37 total):
- Google Sheets: "Google Sheets account" (ID: iWwYR5lhrrUABiru)
- Telegram: Múltiplas credenciais para bots diferentes
- OpenAI: Configurado
- Evolution API: Para WhatsApp

---

## 📁 REPOSITÓRIOS ANALISADOS

### 1. telegram-scraper (React+Node.js)
- Versão: v3.0 - Sistema completo de scraping
- 24 canais monitorados, ROI R$170k/ano
- Status: ✅ Operacional (não usa N8N)

### 2. telegram-scraper-inema-n8n
- Stack: N8N + Supabase + Telegram Bot
- Status: ✅ Operacional em produção

### 3. n8n-workflows-pessoal-2026-01-08
- Sistema de code review com OpenRouter
- Precisa: OpenRouter API Key

### 4. hospitalar-automation
- Playwright + Python dual-module
- Status: Local (não cloud)

### 5. MAKE-25-01-26
- Make.com: 11 cenários ativos
- Social media automation
- Status: ✅ Independente do N8N Cloud

### 6. hospitalar-multi-agent-system
- N8N + Ollama Docker (MCC Orchestrator)
- SISTEMA CENTRAL - Orquestrador Dinâmico
- 68 workflows N8N Cloud, 36 ativos

### 7. n8n-workflows
- 35 workflows backup
- Versão v2.0

### 8. hospitalar-ia-evolutiva-projeto-completo
- Documentação do sistema IA Autonoma
- 9 workflows para implementar (FASE 2)

---

## ⏭️ PRÓXIMOS PASSOS (EM ORDEM)

### IMEDIATO (agora - sem precisar de execuções):
1. Verificar 21-INFRA-Backup-GitHub (ID: QazJlHJIbIfaSfFI) - estado atual
2. Documentar todos os outros 36 workflows ativos que precisam de verificação
3. Preparar lista de workflows para ativar depois do reset

### APÓS RESET 01/06/2026:
1. Testar WF-MCC-SET-URL: POST /webhook/mcc/set-url com AGENTE_LOCAL
2. Testar WF-MCC-GET-URL-GS: GET /webhook/mcc/get-url?service_name=AGENTE_LOCAL
3. Testar WF-ORQUESTRADOR-DINAMICO end-to-end
4. Verificar se WF-HEALTH-CHECK-AGENTES passa sem erros
5. Adicionar OpenRouter API Key no 21-INFRA-Backup-GitHub
6. Iniciar FASE 2: hospitalar-ia-evolutiva 9 workflows

### FASE 2 - Workflows a Implementar (hospitalar-ia-evolutiva):
1. WF-IA-AUTONOMA-MONITOR
2. WF-IA-AUTONOMA-ANALYZER  
3. WF-IA-AUTONOMA-DECISION
4. WF-IA-AUTONOMA-EXECUTOR
5. WF-IA-AUTONOMA-FEEDBACK
6. WF-IA-AUTONOMA-LEARNING
7. WF-IA-AUTONOMA-COORDINATOR
8. WF-IA-AUTONOMA-NOTIFIER
9. WF-IA-AUTONOMA-DASHBOARD

---

## 🔑 WORKFLOW IDs DESCOBERTOS

| Workflow | ID N8N Cloud |
|---|---|
| WF-HEALTH-CHECK-AGENTES | 9arDgUsepPgKE2K6 |
| WF-MCC-GET-URL-GS | 2fuDZ6gYLsRxQM93 |
| WF-MCC-SET-URL | MIo8VUzGX77YJuSq |
| WF-ORQUESTRADOR-DINAMICO | vZjIt5q0Nh9pRic4 |
| 21-INFRA-Backup-GitHub | QazJlHJIbIfaSfFI |

---

## 📝 HISTÓRICO DE ERROS E SOLUÇÕES

| Problema | Solução |
|---|---|
| WF-HEALTH-CHECK-AGENTES lançava Error quando sem agentes | Substituir throw por return graceful |
| WF-MCC-SET-URL usava dataTables (node não disponível) | Substituir por Code + Google Sheets appendOrUpdate |
| WF-MCC-GET-URL-GS não existia | Criado via REST API com 5 nodes |
| Execution limit 2500/2500 | Aguardar reset 01/06/2026 ou upgrade |
| GitHub editor congelando com conteúdo grande | Usar JavaScript cmTile.view.dispatch() |
| N8N API /api/v1/ requer X-N8N-API-KEY | Usar /rest/ endpoints com cookie session |
| POST activate retorna 400 sem versionId | Buscar versionId via GET antes de ativar |

---

*Checkpoint salvo em: 29/05/2026*
*Próxima sessão: Após reset 01/06/2026 - retomar testes e FASE 2*
*Para restaurar: "leia o documento CHECKPOINT_29052026_2.md"*
