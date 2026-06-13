"""Ferramentas de análise de concorrentes."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient, safe_call
from ..networks import COMPETITOR_NETWORKS


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.tool()
    async def get_competitors(
        network: str,
        init_date: str,
        end_date: str,
        blog_id: int,
        timezone: str,
        limit: int = 10,
    ) -> Any:
        """Lista os concorrentes da marca em uma rede e suas métricas.

        Redes suportadas: instagram, facebook, twitch, youtube, twitter, bluesky.

        Args:
            network: Rede social (ver lista acima).
            init_date: Data inicial no formato 2025-01-01.
            end_date: Data final no formato 2025-01-01.
            blog_id: blogId da marca (obtido em get_brands).
            timezone: Timezone da marca, ex.: "America/Sao_Paulo" (de get_brands).
            limit: Número máximo de concorrentes (padrão 10).
        """
        if network not in COMPETITOR_NETWORKS:
            return {
                "error": f"network sem suporte a concorrentes: {network!r}",
                "valid": list(COMPETITOR_NETWORKS),
            }
        params = {
            "from": f"{init_date}T00:00:00",
            "to": f"{end_date}T23:59:59",
            "blogId": blog_id,
            "limit": limit,
            "timezone": timezone,
        }
        return await safe_call(client.get(f"/v2/analytics/competitors/{network}", params=params))
