# analise-context-mcp 🧠

MCP server que entrega a **memória do projeto Análise-Claude** (automação da
Hospitalar Soluções em Saúde) a qualquer agente compatível com MCP — Claude
Desktop, Claude Code, Cursor, etc. Em vez de pedir "leia o documento no GitHub e
continue", o agente conecta uma vez e **restaura o contexto automaticamente**.

## O que ele expõe

**Ferramentas**
- `restaurar_contexto` — retorna o `CONTEXTO.json` completo (estado do projeto).
- `get_project_summary` — panorama enxuto (versão, próximo passo, pendências).
- `list_documents` — lista os checkpoints/análises do repositório.
- `read_document(name)` — lê um documento específico (com proteção anti-traversal).
- `search_context(query)` — busca decisões, erros já resolvidos e IDs de workflow.
- `get_pending_tasks` — pendências técnicas com prioridade.

**Resources:** `analise://contexto`, `analise://resumo`
**Prompt:** `continuar_projeto`

Além disso, injeta uma **orientação** (instructions) que diz ao agente como
começar e como performar sem repetir erros já corrigidos.

## Instalação

```bash
cd context-mcp
pip install -e .
```

A raiz do repositório é detectada automaticamente (procura `CONTEXTO.json` +
`README.md`). Para fixar, use a variável `ANALISE_CLAUDE_ROOT`.

## Execução

```bash
analise-context-mcp                 # stdio (padrão)
# ou
python -m analise_context_mcp
```

## Claude Desktop (manual)

`%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "analise-claude": {
      "command": "python",
      "args": ["-m", "analise_context_mcp"],
      "env": { "ANALISE_CLAUDE_ROOT": "C:\\caminho\\para\\Analise-Claude" }
    }
  }
}
```

> Mais fácil: rode `scripts/connect-claude-desktop.ps1` (na raiz do repo), que
> instala e registra tudo automaticamente.

## Testes

```bash
pip install -e ".[dev]" && pytest -q
```
