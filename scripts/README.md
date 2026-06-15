# scripts/

## Connect-Claude.ps1

Conecta um agente/usuário ao **Claude (Anthropic API)** via PowerShell, com o
contexto do projeto (`CONTEXTO.json`) carregado, e abre um chat interativo onde
o Claude explica onde paramos e orienta o próximo passo.

> PowerShell não tem SDK oficial da Anthropic, então o script usa HTTP puro
> (`Invoke-RestMethod`) contra `POST https://api.anthropic.com/v1/messages`.

### Pré-requisitos
- PowerShell 7+ (recomendado) ou 5.1
- Uma API key da Anthropic em `ANTHROPIC_API_KEY`

### Uso rápido
```powershell
# 1. Defina a chave (não comite isso em lugar nenhum)
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# 2. Rode (baixa o CONTEXTO.json do GitHub main automaticamente)
./Connect-Claude.ps1

# Ou usando o CONTEXTO.json local do repositório:
./Connect-Claude.ps1 -ContextPath ../CONTEXTO.json
```

No chat, digite suas mensagens normalmente. Para sair: `sair`, `exit` ou `quit`.

### Parâmetros
| Parâmetro | Padrão | Descrição |
|---|---|---|
| `-ContextPath` | (vazio) | Caminho local do `CONTEXTO.json`. Se ausente, baixa do GitHub. |
| `-ContextUrl` | raw do branch `main` | URL do `CONTEXTO.json` no GitHub. |
| `-Model` | `claude-opus-4-8` | Modelo Claude a usar. |
| `-MaxTokens` | `8000` | Limite de tokens por resposta. |

### Como a orientação foi melhorada
O `system prompt` do script embute o **protocolo de engenharia de contexto** (a
mesma skill instalada em `.claude/skills/context-engineering/`):
- `CONTEXTO.json` é a **única fonte da verdade**;
- resumo curto na abertura (onde paramos + pendências ALTA + próxima ação);
- respostas concisas, sem colar blocos grandes — economia de tokens;
- primeira ação: confirmar `OPENAI_API_KEY` e `EVOLUTION_API_KEY`.

### Segurança
- **Nunca** comite sua `ANTHROPIC_API_KEY`. Use variável de ambiente.
- O script só lê o `CONTEXTO.json` (público) e envia suas mensagens à Anthropic.
