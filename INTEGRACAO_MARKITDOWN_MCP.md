# Integração — MarkItDown-MCP (Microsoft)

> **Status:** 📋 Documentado / pronto para configurar | **Data:** 15/06/2026
> **Decisão:** conectar via **servidor MCP oficial da Microsoft** (uso pelo agente Claude).

## 🎯 O que é

[MarkItDown](https://github.com/microsoft/markitdown) é uma biblioteca **open-source da Microsoft** (Python)
que converte praticamente qualquer arquivo para **Markdown limpo**, otimizado para consumo por LLMs.

O **[markitdown-mcp](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)** é o
servidor MCP oficial que expõe essa capacidade para clientes compatíveis (Claude Code / Claude Desktop).

### Formatos suportados
PDF, Word (`.docx`), PowerPoint (`.pptx`), Excel (`.xlsx`), imagens (OCR + descrição), áudio (transcrição),
HTML, CSV, JSON, XML, ZIP e conteúdo do YouTube.

### Ferramenta exposta pelo MCP
- `convert_to_markdown(uri)` — aceita URIs nos esquemas `http:`, `https:`, `file:` e `data:`.

## 🧩 Onde encaixa no nosso ecossistema

```
Anexo (PDF/Word/Excel/Imagem) → MarkItDown → Markdown limpo → OpenRouter (Claude) → triagem/resposta
```

Ponto natural de uso: **COCKPIT-07 (Inbox WhatsApp/Email/Notion)**, quando chega um anexo que hoje não é
extraído de forma limpa antes de ir para a IA.

> ⚠️ **Nota de arquitetura:** o `markitdown-mcp` roda **localmente** (STDIO/Docker) e serve ao **agente
> Claude**. Ele **não** se conecta diretamente ao n8n **Cloud**. Para um pipeline 100% automático dentro do
> n8n Cloud, o caminho seria um microserviço HTTP (ex.: Railway) chamado por um HTTP Request node — avaliar
> em fase futura, se necessário.

## ⚙️ Como configurar (Claude Code / Desktop)

### Opção A — via pip (Python local)

```bash
pip install markitdown-mcp
```

Rodar em modo STDIO (padrão, usado pelo cliente MCP):

```bash
markitdown-mcp
```

Modo HTTP/SSE (opcional, para testes locais):

```bash
markitdown-mcp --http --host 127.0.0.1 --port 3001
```

### Opção B — via Docker

```bash
docker build -t markitdown-mcp:latest .
docker run -it --rm markitdown-mcp:latest
```

Com diretório montado (para ler arquivos locais via `file:`):

```bash
docker run -it --rm -v /home/user/data:/workdir markitdown-mcp:latest
```

### Bloco de configuração MCP

> ✅ **Pronto no repo:** já existe um **`.mcp.json`** na raiz do projeto com a variante **pip** abaixo —
> basta rodar `pip install markitdown-mcp` e abrir o Claude Code neste diretório.

Variante **pip** (a que está no `.mcp.json`):

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "markitdown-mcp",
      "args": []
    }
  }
}
```

Variante **Docker** (alternativa — exige `docker build -t markitdown-mcp:latest .` antes),
para adicionar ao `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "markitdown": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "markitdown-mcp:latest"]
    }
  }
}
```

Para dar acesso a arquivos locais, acrescentar `"-v"` e `"/home/user/data:/workdir"` ao array `args`.

## 🔒 Segurança

- Nos modos HTTP/SSE o servidor faz bind em `localhost` por padrão e **não tem autenticação**.
- **Não** expor a interfaces não-locais sem entender as implicações de segurança.

## 📋 Próximos passos

1. Configurar o bloco MCP acima no cliente Claude (Desktop ou Code).
2. Testar conversão de um PDF/Word real do hospital → Markdown.
3. Se o uso justificar automação total no n8n Cloud, avaliar o microserviço HTTP no Railway.
