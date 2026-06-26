"""Registro central de todas as ferramentas MCP."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient
from . import ads, analytics, brands, competitors, generic, media, scheduler, timing

_MODULES = [brands, analytics, ads, competitors, scheduler, timing, media, generic]


def register_all(mcp: FastMCP, client: MetricoolClient) -> None:
    """Registra todas as ferramentas no servidor FastMCP."""
    for module in _MODULES:
        module.register(mcp, client)
