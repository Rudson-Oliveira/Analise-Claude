"""analise-context-mcp: memória do projeto Análise-Claude via MCP."""

from __future__ import annotations

from .config import transport
from .server import create_server

__version__ = "1.0.0"
__all__ = ["create_server", "main", "__version__"]


def main() -> None:
    """Inicia o servidor MCP no transporte configurado (stdio por padrão)."""
    mcp = create_server()
    mcp.run(transport=transport())
