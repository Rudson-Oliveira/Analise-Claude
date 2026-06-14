"""Servidor MCP que entrega a memória/contexto do projeto Análise-Claude."""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from .config import find_root
from .repo import Repo

# Orientação aprimorada — injetada como instruções do servidor para que o
# agente assuma o contexto e o tom corretos sem precisar perguntar.
INSTRUCTIONS = """\
Você está conectado à MEMÓRIA do projeto "Análise-Claude" — o sistema de
automação da Hospitalar Soluções em Saúde (CEO: Rudson Oliveira).

COMO COMEÇAR (sempre, no início da sessão):
1. Chame `restaurar_contexto` (ou leia o resource analise://contexto) para
   carregar o estado atual: versão, próximo passo, pendências e plataformas.
2. Use `get_project_summary` para um panorama enxuto e `list_documents` para ver
   os checkpoints disponíveis. Aprofunde com `read_document` quando necessário.
3. Use `search_context` para localizar decisões, erros já resolvidos e IDs de
   workflows antes de propor mudanças (evita refazer o que já foi feito).

STACK DO PROJETO: n8n Cloud + OpenRouter + Evolution API (WhatsApp) + Notion +
Google Sheets + Microsoft Outlook. Os workflows seguem o padrão COCKPIT-XX.

COMO PERFORMAR (regras de ouro):
- Seja conciso e acione: quando tiver contexto suficiente, aja; não repergunte o
  que já está na memória.
- Antes de alterar um workflow, confira em `search_context` os "erros corrigidos"
  para não repetir armadilhas conhecidas (ex.: usar PATCH e não PUT; manter o
  nome original do node; specifyBody string e não json para expressões n8n).
- Ao concluir uma sessão, proponha atualizar CONTEXTO.json/README com o novo
  estado (checkpoint), mantendo o formato existente.
- Trate tokens e chaves como segredos: nunca os exponha em commits ou logs.

Esta é uma memória somente-leitura — você não escreve nos arquivos por aqui;
proponha as mudanças ao usuário para que sejam versionadas no Git.
"""


def create_server(root: str | None = None) -> FastMCP:
    repo = Repo(find_root(root))
    mcp = FastMCP("analise-claude-context", instructions=INSTRUCTIONS)

    # ----------------------------------------------------------------- tools
    @mcp.tool()
    def restaurar_contexto() -> dict[str, Any]:
        """Restaura o contexto do projeto: retorna o CONTEXTO.json completo.

        Primeira chamada recomendada em toda nova sessão. Equivale ao gatilho
        "leia o documento no GitHub Analise-Claude e continue".
        """
        return repo.context_json()

    @mcp.tool()
    def get_project_summary() -> dict[str, Any]:
        """Panorama enxuto: versão, próximo passo, pendências, estado e plataformas."""
        return repo.summary()

    @mcp.tool()
    def list_documents() -> list[dict[str, Any]]:
        """Lista os documentos de memória (checkpoints, análises) do repositório."""
        return repo.list_documents()

    @mcp.tool()
    def read_document(name: str) -> dict[str, Any]:
        """Lê um documento de memória pelo nome.

        Args:
            name: Nome do arquivo, ex.: "CHECKPOINT_29052026_4.md".
        """
        return repo.read_document(name)

    @mcp.tool()
    def search_context(query: str) -> dict[str, Any]:
        """Busca um termo em toda a memória do projeto (decisões, erros, IDs).

        Args:
            query: Texto a procurar, ex.: "OPENROUTER" ou "COCKPIT-07".
        """
        return repo.search(query)

    @mcp.tool()
    def get_pending_tasks() -> Any:
        """Retorna as pendências técnicas registradas (com prioridade)."""
        ctx = repo.context_json()
        if "error" in ctx:
            return ctx
        return ctx.get("pendencias_tecnicas", [])

    # ------------------------------------------------------------- resources
    @mcp.resource("analise://contexto")
    def contexto_resource() -> str:
        """CONTEXTO.json — estado estruturado do projeto."""
        return json.dumps(repo.context_json(), ensure_ascii=False, indent=2)

    @mcp.resource("analise://resumo")
    def resumo_resource() -> str:
        """Resumo enxuto do projeto."""
        return json.dumps(repo.summary(), ensure_ascii=False, indent=2)

    # --------------------------------------------------------------- prompts
    @mcp.prompt()
    def continuar_projeto() -> str:
        """Prompt de retomada: orienta o agente a assumir o projeto."""
        return (
            "Leia o contexto do projeto Análise-Claude e continue de onde paramos.\n"
            "1. Chame restaurar_contexto e get_project_summary.\n"
            "2. Liste as pendências (get_pending_tasks) e priorize.\n"
            "3. Antes de qualquer alteração, use search_context para conferir o "
            "histórico de erros já resolvidos.\n"
            "4. Proponha o próximo passo concreto e aguarde minha confirmação."
        )

    return mcp
