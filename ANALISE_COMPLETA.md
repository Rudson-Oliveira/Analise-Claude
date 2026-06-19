# 📊 Análise Completa dos Workflows - Hospitalar Soluções em Saúde
**Data:** 29/05/2026 | **Analisado por:** Claude Sonnet 4.6

---

## 🔄 Mapa Completo dos Workflows N8N (Cloud - 39 Workflows)

### CATEGORIA CORE (Criação de Conteúdo)

**01-CORE-INEMA-AI-Criador-Universal**
- Função: Criação de conteúdo universal usando IA sobre mensagens INEMA
- Input: Mensagens do banco de dados Telegram
- Output: Conteúdo gerado para múltiplas plataformas
- IA: Provavelmente GPT-4 ou Claude via API

**02-CORE-Criador-Sites-Vitrine**
- Função: Geração automatizada de landing pages/sites vitrine
- Tecnologia: Provavelmente HTML gerado por IA + deploy automático

**03-CORE-Vision-AI-Observacao-Web**
- Função: Monitoramento visual de páginas web usando Vision AI
- Input: URLs de monitoramento
- Output: Relatório de mudanças detectadas

**04-CORE-Auto-Import-Hospitalar**
- Função: Importação automática de dados do sistema hospitalar
- Integração: API do sistema Hospitalar Saúde

---

### CATEGORIA INFRA (Infraestrutura)

**17-INFRA-WF-Master-Orquestrador**
- Função: Workflow master que coordena todos os outros
- Pattern: Hub-and-spoke (chama outros workflows via webhook)

**18-INFRA-Ollama-Gateway**
- Função: Gateway para o Ollama local (IA self-hosted)
- Configuração: Proxy N8N Cloud → N8N Local → Ollama
- URL Ollama: http://localhost:11434/api/generate
- ⚠️ Necessita Ngrok ou túnel para funcionar

**19-INFRA-WF0-Triggers-Central**
- Função: Central de Schedule Triggers para todos os workflows
- Pattern: Único ponto de controle de agendamentos

**20-INFRA-WF1-Diagnostico**
- Função: Auto-diagnóstico do sistema (health check geral)
- Output: Relatório de status de todos os componentes

**21-INFRA-Backup-GitHub** ⚠️ PARCIALMENTE INATIVO
- Função: Backup automático de todos os workflows para GitHub
- Schedule: Diário às 03:00 Brasília
- Output: Push para github.com/Rudson-Oliveira/n8n-workflows
- Revisão IA: deepseek-coder:6.7b via OpenRouter
- ⚠️ PROBLEMA: API Key OpenRouter não configurada (revisão IA inativa)
- ✅ BACKUP: Provavelmente funciona, só a revisão IA está inativa

---

### CATEGORIA INT (Integrações)

**05-INT-Webhook-Hospitalar-Bridge**
- Função: Bridge entre sistema hospitalar e N8N
- Pattern: Receptor de webhooks do sistema Hospitalar Saúde
- Integração: API REST do sistema hospitalar

**06-INT-Telegram-Import**
- Função: Importação de mensagens do Telegram para banco local
- Fonte: API do Telegram (Bot API ou MTProto)

**07-INT-Telegram-Scraper**
- Função: Scraping de canais Telegram via API Manus
- API: https://tele-scrap-fgfuwhsp.manus.space/api/v1/messages
- Deduplicação: SHA-256 das mensagens

**08-INT-e63-Ticketing**
- Função: Integração com sistema de tickets e63
- Uso: Gestão de chamados do hospital

**09-INT-INEMA-Scraper**
- Função: Scraping específico dos canais INEMA
- Canais: 24 canais pré-configurados

---

### CATEGORIA OP (Operações)

**11-OP-Chatbot-Atendimento**
- Função: Chatbot para atendimento via WhatsApp/Telegram
- IA: Provavelmente Claude ou GPT via API
- Integration: Evolution API (WhatsApp)

**12-OP-Gestor-Agendamentos**
- Função: Gestão de agendamentos de pacientes
- Integração: Calendário + sistema hospitalar

**13-OP-Notificacoes-Pacientes**
- Função: Envio de notificações automáticas para pacientes
- Canais: WhatsApp, SMS, Email

**14-OP-Assistente-Virtual-Saude**
- Função: Assistente virtual especializado em saúde
- Base de conhecimento: Mensagens INEMA classificadas

---

### SISTEMA MULTI-AGENTE (MAS)

**WF-GERENCIADOR-AGENTES**
- Função: Gerencia dinamicamente os agentes disponíveis
- MCC: Lê/escreve no Google Sheets central

**WF-HEALTH-CHECK-AGENTES** (schedule: 5min)
- Função: Verifica disponibilidade de todos os agentes
- Agentes verificados: AGENTE_LOCAL (Ollama), AGENTE_EXTERNO (OpenAI)

**WF-INICIALIZADOR-AGENTES**
- Função: Inicializa agentes ao reiniciar o sistema
- Trigger: Manual ou schedule

**WF-ORQUESTRADOR-DINAMICO** ❌ PARCIALMENTE FALHO
- Função: Roteia requisições para o melhor agente disponível
- Algoritmo: Verifica MCC → escolhe agente → fallback
- ❌ PROBLEMA: Não consegue buscar URL do MCC (WF-MCC-GET ausente)
- URL: http://localhost:5678/webhook/orquestrador-dinamico

**WF-ORQUESTRADOR-MULTI-AGENTE**
- Função: Versão multi-agente do orquestrador
- Pattern: Decomposição de tarefas entre múltiplos agentes

**WF-AGENTE-LOCAL-OLLAMA**
- Função: Agente usando Ollama local
- Endpoint: http://localhost:11434/api/generate
- Modelos disponíveis: Depende do que foi instalado no Docker

**WF-AGENTE-EXTERNO-OPENAI**
- Função: Agente usando OpenAI GPT
- Fallback: Acionado quando Ollama falha

---

### ORCAMENTOS (4 Workflows)

**WF-Agente-Orcamentos-COMPLETO**
- Função: Geração completa de orçamentos com IA
- Fluxo: Recebe pedido → IA processa → Gera PDF → Envia

**WF-Agente-Orcamentos-LOCAL**
- Função: Versão com Ollama local para orçamentos
- Vantagem: Sem custo de API

**WF-Agente-Orcamentos**
- Função: Versão básica do agente de orçamentos

---

## 🔄 Cenários Make.com (11 Cenários)

### Sistema de Publicação de Conteúdo

**Fluxo de Dados:**
```
Google Sheets (PC-GERAL / PC-DATAS) 
  → Make.com (lê a cada 15min)
  → Google Drive (armazena organizado)
  → Placid (gera imagens)
  → Instagram / Facebook / LinkedIn (publica)
```

**1. 3C-Datas Comemorativas - Postagem**
- Lê: Google Sheets (PC-DATAS)
- Ação: Publica posts de datas comemorativas
- Status: ✅ Ativo

**2. 3B-Datas Comemorativas - Revisão**
- Lê: Google Drive pasta datas comemorativas
- Ação: Revisa e aprova conteúdo pendente

**3. 4C-Data Comemorativa - Reels**
- Lê: Bobinas/Reels de datas comemorativas
- Ação: Publica Reels nas redes sociais

**4. Transcrição**
- Lê: Facebook Watch + Monitor Instagram
- Ação: Transcreve vídeos via AssemblyAI
- IA: AssemblyAI para transcrição em PT-BR

**5. 6B-Geração Placid**
- Input: Template + dados
- Ação: Gera imagens automaticamente via Placid ($19/mês)
- Output: Imagens prontas para postagem

**6. Instagram Postagens → LinkedIn**
- Reaproveitamento de conteúdo cross-platform
- Instagram → adaptação → LinkedIn

**7. Review LinkedIn**
- Revisa conteúdo antes de postar no LinkedIn
- Validação humana ou automatizada

**8. Carrossel**
- Gera e publica posts em formato carrossel
- Blueprint: Carrossel.json

**9. Bobinas - Geral**
- Gerencia Reels/Vídeos gerais
- Cataloga e organiza

**10. Bobinas - Datas Comemorativas**
- Específico para vídeos de datas comemorativas

**11. Raspar**
- Scraping de vídeos para transcrição
- Blueprint: Transcricao.json

---

## 🏗️ Arquitetura Geral do Sistema

```
┌─────────────────────────────────────────────────────┐
│                   ENTRADA DE DADOS                   │
├──────────────┬────────────────┬────────────────────┤
│ Telegram     │ Google Sheets  │ Webhooks           │
│ INEMA (24ch) │ PC-GERAL       │ Sistema Hospitalar │
│ @Bot API     │ PC-DATAS       │ e63 Ticketing      │
└──────┬───────┴───────┬────────┴──────────┬─────────┘
       │               │                   │
       ▼               ▼                   ▼
┌──────────────────────────────────────────────────────┐
│                    N8N CLOUD                          │
│         (39 workflows / rudsonoliveira2323)           │
│                                                      │
│  INFRA (triggers, backup, orquestrador)              │
│  INT   (scrapers, bridges, imports)                   │
│  CORE  (criação de conteúdo, IA)                     │
│  OP    (chatbot, agendamentos, notificações)         │
│  MAS   (multi-agent system)                          │
└───────────┬──────────────────────┬───────────────────┘
            │                      │
            ▼                      ▼
┌───────────────────┐   ┌──────────────────────────┐
│   N8N LOCAL       │   │      MAKE.COM             │
│   localhost:5678  │   │   11 cenários ativos      │
│                   │   │   Schedule: 15min         │
│ Docker:           │   │                           │
│ - ollama:11434    │   │ Google Sheets/Drive       │
│ - postgres        │   │ → Placid → Instagram      │
│ - mongo-express   │   │ → Facebook → LinkedIn     │
└───────────────────┘   └──────────────────────────┘
            │
            ▼
┌───────────────────┐
│  ARMAZENAMENTO    │
│                   │
│ Supabase          │
│ (telegram_msgs)   │
│                   │
│ Google Sheets     │
│ (MCC/PC-GERAL)    │
│                   │
│ GitHub            │
│ (backup workflows)│
└───────────────────┘
```

---

## 🚨 Análise de Riscos e Vulnerabilidades

### Riscos de Segurança
1. **Token Telegram exposto** no README do telegram-scraper-inema-n8n
   - Token: `8517983740:AAG********************************` (REDIGIDO — ver SEGURANCA.md)
   - ⚠️ **Ação URGENTE:** Revogar e gerar novo token no @BotFather. O valor original
     já esteve commitado no Git e deve ser considerado COMPROMETIDO.

2. **Supabase Service Role Key** hardcoded no workflow N8N
   - Risco: Acesso total ao banco de dados
   - **Ação:** Mover para Credentials do N8N ou variáveis de ambiente

### Riscos de Disponibilidade
3. **N8N Local depende de Ngrok** para ser acessado pelo Cloud
   - Ngrok gratuito muda URL a cada restart
   - **Solução:** Ngrok pago ou servidor com IP fixo

4. **Ollama local** - porta incerta (11434 vs 11435)
   - Confirmar via: `docker ps`

### Riscos de Custo
5. **Placid** - $19/mês por assinatura
6. **OpenRouter** - Paga por token (monitorar créditos)
7. **OpenAI** - Paga por token
8. **Make.com** - Paga por operação (11 cenários ativos)

---

## 💡 Melhorias Recomendadas

### Prioridade Alta
1. **Implementar tratamento de erros** em todos os workflows N8N
   - Pattern: Try-Catch → Error Handler → Notificação Email/Telegram

2. **Centralizar credenciais** no N8N Credentials Manager
   - Nunca hardcode em nodes Code
   - Usar `$credentials` do N8N

3. **Dashboard de Monitoramento**
   - Criar workflow N8N que agrega status de todos
   - Exibir em painel web simples (HTML node)

### Prioridade Média
4. **Testes automatizados** para workflows críticos
   - Mock data para testar sem chamar APIs externas

5. **Versionamento semântico** dos workflows
   - Atualmente só tem backup por data

6. **Documentação dos webhooks ativos**
   - Lista com URL, método, payload esperado

### Prioridade Baixa
7. **Otimizar queries** das planilhas Google Sheets
   - Cachear dados lidos frequentemente

8. **Alertas de custo** para APIs pagas
   - Webhook quando créditos estiverem baixos

---

*Análise técnica gerada por Claude Sonnet 4.6 em 29/05/2026*
