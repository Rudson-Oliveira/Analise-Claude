"""Construção do servidor FastMCP do Metricool."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from . import resources
from .client import MetricoolClient
from .config import Settings
from .tools import register_all


def create_server(
    settings: Settings | None = None, *, client: MetricoolClient | None = None
) -> tuple[FastMCP, MetricoolClient]:
    """Cria a instância FastMCP com todas as ferramentas, resources e prompts.

    ``client`` pode ser injetado (útil em testes com transporte mockado).
    """
    settings = settings or Settings.from_env()
    client = client or MetricoolClient(settings)

    mcp = FastMCP(
        "metricool-swiss",
        instructions=(
            "Canivete suíço para o Metricool. Comece por get_brands (ou "
            "find_brand) para obter o blogId e o timezone da marca — eles são "
            "exigidos pela maioria das ferramentas. Datas usam o formato "
            "AAAA-MM-DD. Para agendar posts, normalize as mídias com "
            "normalize_media_url e respeite os requisitos de cada rede. Quando "
            "não houver ferramenta dedicada, use metricool_request."
        ),
    )

    register_all(mcp, client)
    resources.register(mcp, client)
    return mcp, client


def build() -> FastMCP:
    """Atalho que retorna apenas o FastMCP (para `mcp.run`)."""
    mcp, _ = create_server()
    return mcp
