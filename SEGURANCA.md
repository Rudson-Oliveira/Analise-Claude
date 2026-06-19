# 🔐 Segurança — Achados e Plano de Remediação
## Hospitalar Soluções em Saúde

> **Auditoria de segurança** | Data: 19/06/2026
> Este documento registra credenciais expostas detectadas no repositório e as ações necessárias.

---

## 🔴 CRÍTICO — Credenciais expostas no Git

| # | Credencial | Onde estava | Status no arquivo | Ação necessária |
|---|---|---|---|---|
| 1 | **Token Bot Telegram** (`8517983740:AAG...`) | `ANALISE_COMPLETA.md` | ✅ Redigido | 🔴 **Revogar no @BotFather** |
| 2 | **OpenRouter API Key** (`sk-or-v1-...`) | `CONTEXTO.json` | ✅ Redigido | 🟡 **Rotacionar a chave** |

### ⚠️ Importante: redigir NÃO basta

Mascarar o valor no arquivo atual **não remove o segredo do histórico do Git**.
O valor original continua acessível em commits antigos. Por isso:

1. **Revogue/rotacione as credenciais na origem** (é a única proteção real):
   - **Telegram:** abra o @BotFather → `/revoke` → gere novo token.
   - **OpenRouter:** painel → Keys → revogue a chave antiga → gere nova.
2. Atualize as novas credenciais **apenas** no N8N Credentials Manager (nunca em arquivos).
3. (Opcional, avançado) Reescrever o histórico do Git com `git filter-repo` ou BFG
   para limpar os valores antigos — fazer só com backup e cuidado.

---

## 🟠 Boas práticas adotadas

- ✅ Adicionado `.gitignore` cobrindo `.env`, `*.key`, `*.pem`, `credentials.json`, etc.
- ✅ Credenciais nos documentos agora aparecem mascaradas (prefixo + `***`).

## 🟡 Recomendações pendentes (do ANALISE_COMPLETA.md)

- **Supabase Service Role Key hardcoded** no workflow `telegram-scraper-inema-n8n`
  → mover para o N8N Credentials Manager (acesso total ao banco em risco).
- **Centralizar todas as credenciais** no N8N Credentials Manager — nunca em nodes Code.
- **Alertas de custo** para APIs pagas (OpenRouter, OpenAI, Placid, Make.com).

---

## ✅ Checklist de remediação

- [ ] Revogar token do Telegram no @BotFather e gerar novo
- [ ] Rotacionar OpenRouter API Key
- [ ] Mover Supabase Service Role Key para N8N Credentials
- [ ] Confirmar que nenhuma nova credencial seja commitada (proteção via `.gitignore`)
- [ ] (Opcional) Limpar segredos do histórico do Git

---

*Documento de segurança — atualizar conforme as credenciais forem rotacionadas.*
