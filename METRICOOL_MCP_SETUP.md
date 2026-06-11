# Metricool MCP — Guia de Instalação

> Conecta o Metricool ao Claude (e ao n8n) via MCP (Model Context Protocol).
> Depois de conectado, dá pra pedir ao Claude coisas como:
> *"Acessa o Metricool, escaneia meus concorrentes (Instagram, TikTok, YouTube, LinkedIn) e me dá sugestão de conteúdo de verdade pro meu nicho."*

**Endpoint oficial (MCP remoto):** `https://ai.metricool.com/mcp`
**Autenticação:** OAuth (no app Claude) ou header `X-Mc-Auth` com API Key (no n8n)
**Plano:** funciona em qualquer plano Metricool, inclusive Free — com as limitações do plano (Free não consulta dados com mais de 3 meses nem agenda mais de 20 posts).

---

## Opção 1 — App Claude (claude.ai / Claude Desktop)  ⭐ recomendado

É o fluxo das imagens enviadas. Tudo pela interface, sem token manual (usa OAuth):

1. Abra o Claude → **Settings / Configurações** → **Connectors / Conectores**.
2. Clique em **Add custom connector** (Adicionar conector personalizado).
3. **Name:** `Metricool`
4. **URL:** `https://ai.metricool.com/mcp`
5. Clique em **Add**.
6. O Metricool abre a tela **"Authorize application"** — revise as permissões (ver, gerenciar marcas e redes, baixar métricas/relatórios, criar/publicar posts, SmartLinks, inbox, GMB, etc.) e clique em **Grant access**.
7. Pronto. O conector aparece ativo e o Claude já consegue usar as ferramentas do Metricool.

> Faça login no Metricool no mesmo navegador antes do passo 6 para o OAuth fluir direto.

---

## Opção 2 — Claude Code (CLI)

Já deixei o arquivo [`.mcp.json`](./.mcp.json) na raiz deste repositório. Qualquer sessão do Claude Code aberta nesta pasta detecta o servidor `metricool` automaticamente — basta autenticar com OAuth na primeira vez (comando `/mcp` dentro do Claude Code).

Se preferir registrar manualmente (escopo do usuário, vale em qualquer pasta):

```bash
claude mcp add --transport http metricool https://ai.metricool.com/mcp
```

Depois rode `/mcp` no Claude Code e siga o fluxo de autorização.

> Observação: em sessões do **Claude Code na web**, a conexão depende da política de rede do ambiente permitir saída para `ai.metricool.com`. Em ambiente local funciona direto.

---

## Opção 3 — n8n (encaixa no stack atual)

O stack do projeto (COCKPIT-07/08, briefing diário, etc.) roda em n8n. Dá pra usar o Metricool de duas formas:

**a) Via MCP Client Tool node** (n8n com nó de MCP):
- Endpoint: `https://ai.metricool.com/mcp`
- Autenticação: **Header Auth** → nome do header `X-Mc-Auth`, valor = sua **API Key** do Metricool.

**b) Via HTTP Request node** (sempre funciona):
- Chamar a API do Metricool diretamente, passando o header `X-Mc-Auth: <API_KEY>`.

### Onde pegar a API Key
Metricool → **Configurações da conta / Account Settings → API**. Copie a **API Key** (para o n8n, é o valor do header `X-Mc-Auth`).

> ⚠️ Nunca commite a API Key no GitHub. No n8n, guarde como **credencial**; em scripts, use variável de ambiente.

---

## Casos de uso (depois de conectado)

- **Análise de concorrentes** — escanear perfis (Insta, TikTok, YouTube, LinkedIn) e comparar desempenho.
- **Sugestão de conteúdo** — ideias e calendário com base no que performa no nicho.
- **Relatórios** — puxar métricas e montar resumos automáticos (encaixa no COCKPIT-08 Briefing Diário).
- **Agendamento** — criar/programar posts nas redes conectadas.

---

## Segurança

- O `.mcp.json` deste repo **não contém segredos** — a Opção 1/2 usa OAuth, e o token fica no Claude, não no Git.
- Para n8n, a API Key vai em credencial/variável de ambiente (header `X-Mc-Auth`), nunca no código versionado.

## Fontes
- [Como conectar o MCP do Metricool — Metricool Help Center](https://help.metricool.com/how-to-connect-metricools-mcp-eqp9h)
- [mcp-metricool — PyPI](https://pypi.org/project/mcp-metricool/)
