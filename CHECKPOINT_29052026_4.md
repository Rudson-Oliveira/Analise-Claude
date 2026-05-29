# CHECKPOINT 4 - 29/05/2026 - Estado Final da Sessão

## 🔄 PARA RESTAURAR CONTEXTO NA PRÓXIMA SESSÃO
**Arquivo mais recente:** https://github.com/Rudson-Oliveira/Analise-Claude/blob/main/CHECKPOINT_29052026_4.md

---

## 📊 RESUMO EXECUTIVO

**Sessão iniciada com:** 38 workflows ativos  
**Sessão encerrada com:** 44 workflows ativos (+6)  
**Plano N8N:** 10.000 exec/mês (upgrade feito pelo usuário)  
**Execuções usadas em Maio:** ~2.800/10.000 (28%)

---

## ✅ TUDO QUE FOI FEITO NESTA SESSÃO

### Workflows Corrigidos e Ativados:
| Workflow | ID | Ação | Status |
|---|---|---|---|
| WF-MCC-SET-URL | MIo8VUzGX77YJuSq | Fix aba MCC_CONFIG + teste | ✅ FUNCIONANDO |
| WF-MCC-GET-URL-GS | 2fuDZ6gYLsRxQM93 | Fix Google Sheets → HTTP API | ✅ FUNCIONANDO |
| WF-ORQUESTRADOR-MULTI-AGENTE | RREL5BmuDu3HBqcR | Ativado | ✅ ATIVO |
| 19-INFRA-WF0-Triggers | MgOrbuP6cWvNwNaE | Ativado | ✅ ATIVO |
| WF-99-Observabilidade-Logs | BCC5aExZklz2KHTZ | Fix credenciais + Ativado | ✅ ATIVO |
| WF-BACKUP-GITHUB | Qbgwo4yCDqX7QAMy | Fix nodes obsoletos + Ativado | ✅ ATIVO |
| WF-RESTAURACAO-GITHUB | WHSdG2ovJPyCnCXL | Reconstruído + Ativado | ✅ ATIVO |
| 08-INT-e63-Ticketing | AITTSGpLcImXF3Nt | Ativado | ✅ ATIVO |

### Google Sheets MCC_CONFIG:
- Aba renomeada de "Folha1" → "MCC_CONFIG"
- Dados existentes: ORQUESTRADOR e AGENTE_LOCAL
- URL planilha: https://docs.google.com/spreadsheets/d/1-rRo3CAb2QunpNJfsAzqYm2lyqmRGsi_nyYnS_FqcDA

---

## 🔍 MAPEAMENTO INTEL (SEM ALTERAÇÕES - apenas leitura)

### HospitaLar-Intel-Dispatcher [UwmGLjOivexhtvV7]
- **Status:** ATIVO
- **Webhook:** POST /webhook/hospitalarsaude-intel
- **Nós:** 4 (Webhook → Router → Log → Responder)
- **Função:** Recebe eventos do sistema Intel e roteia por tipo

### Intel-Proposta-Automatica [CL2CJ91yjqRhPyI7]
- **Status:** ATIVO
- **Webhook:** POST /webhook/intel-proposta
- **Nós:** 4 (Webhook → Preparar WhatsApp → Notificar → Responder)
- **Função:** Notifica responsável via WhatsApp quando deal movido para Proposta

### Intel-Conteudo-IA [LkLctxmxWtjbVE8F]
- **Status:** ATIVO
- **Webhook:** POST /webhook/intel-conteudo-ia
- **Nós:** 3 (Webhook → Processar Mídia → Responder)
- **Função:** Processa solicitações de geração de conteúdo/mídia com IA

**⚠️ IMPORTANTE:** Esses 3 workflows são do projeto Intel ativo. Não modificar sem autorização de Rudson.

---

## 📋 ESTADO COMPLETO - 69 WORKFLOWS

### ✅ ATIVOS (44 total):

**Infraestrutura:**
- 21-INFRA-Backup-GitHub [QazJlHJIbIfaSfFI] - Backup automático para GitHub
- WF-BACKUP-GITHUB [Qbgwo4yCDqX7QAMy] - Backup alternativo (reconstruído)
- WF-RESTAURACAO-GITHUB [WHSdG2ovJPyCnCXL] - Restauração do GitHub (reconstruído)
- 19-INFRA-WF0-Triggers [MgOrbuP6cWvNwNaE] - Central de Gatilhos
- 18-INFRA-Ollama-Gateway [oB6o3r4iEMXULyAH] - API Local Ollama
- WF-99-Observabilidade-Logs [BCC5aExZklz2KHTZ] - Logs → Google Sheets
- 22-INFRA-AI-Code-Reviewer [B7BBCjKDX5sGIfGU] - Revisor de código IA
- 17-INFRA-WF-Master [Gx6ak7bXif9Zh3Cn] - Orquestrador de Equipes

**MCC (Multi-Channel Controller):**
- WF-MCC-GET-URL-GS [2fuDZ6gYLsRxQM93] ✅ GET /webhook/mcc/get-url
- WF-MCC-SET-URL [MIo8VUzGX77YJuSq] ✅ POST /webhook/mcc/set-url
- WF-ORQUESTRADOR-DINAMICO [vZjIt5q0Nh9pRic4] - Orquestrador principal
- WF-ORQUESTRADOR-MULTI-AGENTE [RREL5BmuDu3HBqcR] - Multi-agente com fallback
- WF-HEALTH-CHECK-AGENTES [9arDgUsepPgKE2K6] - Health check (falha por Ollama offline)
- WF-GERENCIADOR-AGENTES [exkT2c1GtIbNJmxr]
- WF-INICIALIZADOR-AGENTES [KGtAUkYFhH9UxLSt]

**Integrações:**
- 04-CORE-Auto-Import [LxuhS8681nX9NrB1] - MySQL Schedule
- 06-INT-Telegram-Import [mEw1hJz1cJMYMDNe] - Telegram → INEMA
- 07-INT-Telegram-Scraper [NM89ewNy9WvjsPQ5] - Scraper Produção
- 08-INT-e63-Ticketing [AITTSGpLcImXF3Nt] - Integração Hospitalar
- 09-INT-INEMA-Scraper [uDHrit1TlBfWUxCh]
- 05-INT-Webhook-Hospitalar [33xIKaVlBU1RTI8O]
- 📧 Triagem Email [i7f12WgSoAAHraWA]
- 📅 VAGA-LUME Calendário [TEOEiAyVSlcyTa31Rgjb9]
- 📱 Triagem WhatsApp [JiSB5D56uGUTRifp]

**Operações:**
- 01-CORE-INEMA-AI [5GQFEcl4PqYaPqXr] - Criador de automações via IA
- 02-CORE-Criador-Sites [YRxqBEDiRd4j22yJ]
- 03-CORE-Vision-AI [BRsMiqymKjnnomFr]
- 14-OP-Assistente-Virtual [Esi1dNLQtzZGgECL]
- WF-12-Captura-Formulario-Site [1QDmhEjBoeYtCCP1]
- WF-COMET-01-ANALISADOR [CHB6gdswY4UAQ9gT]

**Funil de Vendas:**
- WF-00-Orquestrador-Funil [lVC4kyju9m0hPFo2]
- WF-01-Agente-Prospeccao [09c0hYoQw6T6KVm8]
- WF-02-Agente-Qualificacao [eQRTnUM9CDRnAcAy]
- WF-03-Agente-Apresentacao [AH57c4jXxxwV8ild]
- WF-04-Agente-Maturacao [km91d8MWMWqdljv7]
- WF-05-Agente-Negociacao [VFEiDVW51R9gNdQi]
- WF-06-Agente-Encerramento [gUqDltSpRoomJ6ge]
- WF-07-Agente-Prospeccao-Mercados [c4WmIUPjX0iH0ktY]
- WF-Agente-Orcamentos-Completo [vigd0lMGWAGZaSRB]

**Intel (PROJETO ATIVO - não alterar):**
- HospitaLar-Intel-Dispatcher [UwmGLjOivexhtvV7]
- Intel-Proposta-Automatica [CL2CJ91yjqRhPyI7]
- Intel-Conteudo-IA [LkLctxmxWtjbVE8F]

**Outros:**
- TEMP-Test-Workflow [Dta0y1alnKLwdJtq]
- My workflow 2 [mmc1HmynsbkYcAvm]

### ❌ INATIVOS (25 total - não podem ser ativados por agora):
Motivos: Apenas manualTrigger, dependências externas não configuradas (Postgres, HuggingFace), ou ambiente local necessário.
- 11-OP-Chatbot-Atendimento [UZaFiDVTYEehjTmq] - Só manualTrigger
- 12-OP-Gestor-Agendamentos [tHTuOdVtcsoDadTf] - Postgres + HuggingFace
- 13-OP-Notificacoes-Pacientes [QHdNijZ3JYY2nIK6] - Postgres
- 20-INFRA-WF1-Diagnostico [blTLFKOWd4It5KMB] - DeepSeek + Memory
- WF-SIMULADOR-FRONTEND [8AXWxG4OYbCqsI1P] - Old nodes
- E outros workflows de template/test/etapas

---

## 🔗 ENDPOINTS FUNCIONANDO

| Endpoint | Método | Workflow | Retorno |
|---|---|---|---|
| /webhook/mcc/set-url | POST | WF-MCC-SET-URL | {success: true, service_name, url} |
| /webhook/mcc/get-url?service_name=X | GET | WF-MCC-GET-URL-GS | {success: true, url, description} |
| /webhook/hospitalarsaude-intel | POST | Intel-Dispatcher | {ok} |
| /webhook/intel-proposta | POST | Intel-Proposta | {ok} |
| /webhook/intel-conteudo-ia | POST | Intel-Conteudo | {ok} |
| /webhook/restaurar-workflow | POST | WF-RESTAURACAO-GITHUB | {success, workflow_id} |

---

## 🚨 PENDÊNCIAS IDENTIFICADAS

### Alta Prioridade:
1. **WF-HEALTH-CHECK-AGENTES** - Falha a cada 5 min pois Ollama está OFFLINE
   - Solução: Ligar N8N Local + Ollama OU desativar se Ollama não estiver sendo usado
   - ID: 9arDgUsepPgKE2K6

2. **N8N Local (Ollama)** - Não está acessível do cloud
   - URL atual no MCC_CONFIG: http://host.docker.internal:5678/webhook/agente-local
   - Precisaria estar rodando localmente ou em um servidor público

### Média Prioridade:
3. **WF-SIMULADOR-FRONTEND** [8AXWxG4OYbCqsI1P] - Usa nodes antigos (n8n-nodes-base.start)
4. **FASE 2** - Implementar 9 workflows do hospitalar-ia-evolutiva

---

## ⚙️ CONFIGURAÇÕES TÉCNICAS IMPORTANTES

### N8N Cloud:
- URL: https://rudsonoliveira2323.app.n8n.cloud
- Versão: n8n@2.21.8
- API: /rest/ (session cookie) ou /api/v1/ (X-N8N-API-KEY)
- Timezone: America/Sao_Paulo

### Credenciais-chave:
- Google Sheets: "Google Sheets account" (iWwYR5lhrrUABiru)
- Header Auth (GitHub/N8N API): "Header Auth account" (RKtcfFzRmcnJZBgu)
- Evolution API: "Evolution API Rudson" (XUO0KTV1AZe2pBXT)
- OpenAI: "OpenAi account" (HKGFp46mQxWxySRb)

### Técnica HTTP Google Sheets (para workflows que leem planilhas):
```
type: n8n-nodes-base.httpRequest, typeVersion: 4
parameters:
  url: https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{TAB}!A:E
  authentication: predefinedCredentialType
  nodeCredentialType: googleSheetsOAuth2Api
credentials:
  googleSheetsOAuth2Api: {id: iWwYR5lhrrUABiru, name: Google Sheets account}
```

---

## ⏭️ PRÓXIMA SESSÃO - O QUE FAZER

1. Ligar N8N Local com Ollama (se necessário)
2. Decidir sobre WF-HEALTH-CHECK-AGENTES (manter ou desativar)
3. Implementar FASE 2: 9 workflows do hospitalar-ia-evolutiva
4. Testar WF-ORQUESTRADOR-DINAMICO end-to-end com mensagem real
5. Verificar 08-INT-e63-Ticketing em mais detalhe

---

*Checkpoint final da sessão: 29/05/2026*
*Para restaurar: diga "leia o documento CHECKPOINT_29052026_4.md"*
*Repositório: https://github.com/Rudson-Oliveira/Analise-Claude*
