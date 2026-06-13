"""metricool-mcp-swiss: canivete suíço MCP para o Metricool."""

from __future__ import annotations

from .config import Settings
from .server import build, create_server

__version__ = "1.0.0"
__all__ = ["build", "create_server", "Settings", "main", "__version__"]


def main() -> None:
    """Ponto de entrada do CLI: inicia o servidor MCP no transporte configurado."""
    settings = Settings.from_env()
    mcp = build()
    transport = settings.transport.lower()
    if transport not in {"stdio", "sse", "streamable-http"}:
        transport = "stdio"
    mcp.run(transport=transport)
