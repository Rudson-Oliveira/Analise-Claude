"""Ferramentas de analytics de conteúdo orgânico por rede social.

Mantém os nomes do MCP oficial (superset compatível) e adiciona uma ferramenta
genérica ``get_analytics`` parametrizada por rede para cobrir tudo de uma vez.
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient, safe_call
from ..networks import ANALYTICS, build_date_params


async def _fetch(client: MetricoolClient, key: str, init_date: str, end_date: str, blog_id: int):
    endpoint = ANALYTICS[key]
    params = build_date_params(endpoint, init_date, end_date)
    params["blogId"] = blog_id
    return await safe_call(client.get(endpoint.path, params=params))


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.tool()
    async def get_analytics(network_content: str, init_date: str, end_date: str, blog_id: int) -> Any:
        """Analytics de conteúdo para qualquer rede (ferramenta unificada).

        Args:
            network_content: Uma das chaves: instagram_posts, instagram_reels,
                instagram_stories, facebook_posts, facebook_reels,
                facebook_stories, tiktok_videos, threads_posts, bluesky_posts,
                linkedin_posts, pinterest_pins, youtube_videos, x_posts,
                twitch_videos.
            init_date: Data inicial no formato 2025-01-01.
            end_date: Data final no formato 2025-01-01.
            blog_id: blogId da marca (obtido em get_brands).
        """
        if network_content not in ANALYTICS:
            return {
                "error": f"network_content inválido: {network_content!r}",
                "valid": sorted(ANALYTICS),
            }
        return await _fetch(client, network_content, init_date, end_date, blog_id)

    # --- Ferramentas nomeadas (compatíveis com o MCP oficial) ---------------
    def _named(key: str, label: str):
        async def tool(init_date: str, end_date: str, blog_id: int) -> Any:
            return await _fetch(client, key, init_date, end_date, blog_id)

        tool.__name__ = f"get_{key}"
        tool.__doc__ = (
            f"Lista {label} da sua conta Metricool.\n\n"
            "Args:\n"
            "    init_date: Data inicial no formato 2025-01-01.\n"
            "    end_date: Data final no formato 2025-01-01.\n"
            "    blog_id: blogId da marca (obtido em get_brands).\n"
        )
        return tool

    named = [
        ("instagram_posts", "os posts do Instagram"),
        ("instagram_reels", "os Reels do Instagram"),
        ("instagram_stories", "os Stories do Instagram"),
        ("facebook_posts", "os posts do Facebook"),
        ("facebook_reels", "os Reels do Facebook"),
        ("facebook_stories", "os Stories do Facebook"),
        ("tiktok_videos", "os vídeos do TikTok"),
        ("threads_posts", "os posts do Threads"),
        ("bluesky_posts", "os posts do Bluesky"),
        ("linkedin_posts", "os posts do LinkedIn"),
        ("pinterest_pins", "os Pins do Pinterest"),
        ("youtube_videos", "os vídeos do YouTube"),
        ("x_posts", "os posts do X (Twitter)"),
        ("twitch_videos", "os vídeos da Twitch"),
    ]
    for key, label in named:
        mcp.tool()(_named(key, label))
