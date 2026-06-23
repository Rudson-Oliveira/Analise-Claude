# Frontend — Painel do Ecossistema

Painel visual (HTML autocontido, sem dependências) do ecossistema de automação da
**Hospitalar Soluções em Saúde**, com foco na arquitetura **multicanal ("canivete suíço")**:
um cérebro de IA (Claude) acionável de qualquer canal e que entrega resultado em qualquer canal.

## Como abrir

- **Local:** basta abrir `frontend/index.html` no navegador (duplo clique). Não precisa de build.
- **Servidor local (opcional):**
  ```bash
  cd frontend && python3 -m http.server 8080
  # acesse http://localhost:8080
  ```

## Publicar no GitHub Pages (grátis)

1. No GitHub: **Settings → Pages**.
2. **Source:** branch `main`, pasta `/frontend` (ou mova o conteúdo para `/docs`).
3. A URL pública fica algo como `https://rudson-oliveira.github.io/Analise-Claude/`.

## O que mostra

- **Hero** + estatísticas do ecossistema.
- **Diagrama multicanal interativo:** clique num canal de entrada (WhatsApp, Email, Notion,
  Telegram, Sheets, Webhook) para ver o fluxo entrada → Claude → saída.
- **Integrações:** Managed Agents, MarkItDown-MCP, n8n, OpenRouter.
- **Workflows:** estado dos COCKPIT-* / WF-* (sincronizado com `CONTEXTO.json`).
- **Variáveis n8n:** status das chaves (configuradas / pendentes / futuras).

## Atualizar os dados

Os números e status são estáticos no HTML e refletem o `CONTEXTO.json` (v4.2). Ao mudar o
estado do projeto, atualize as tabelas/cards do `index.html` junto com o `CONTEXTO.json`.

> Próximo passo possível: tornar o painel **dinâmico**, lendo o `CONTEXTO.json` via `fetch()`
> para não precisar editar o HTML manualmente.
