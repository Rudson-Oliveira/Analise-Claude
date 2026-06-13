"""Ferramentas de campanhas de anúncios (Facebook Ads, Google Ads, TikTok Ads)."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient, safe_call
from ..networks import ADS, build_date_params


async def _fetch_ads(client: MetricoolClient, platform: str, init_date: str, end_date: str, blog_id: int):
    endpoint = ADS[platform]
    params = build_date_params(endpoint, init_date, end_date)
    params["blogId"] = blog_id
    return await safe_call(client.get(endpoint.path, params=params))


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.tool()
    async def get_ads_campaigns(platform: str, init_date: str, end_date: str, blog_id: int) -> Any:
        """Campanhas de anúncios para a plataforma escolhida (unificada).

        Args:
            platform: "facebook", "google" ou "tiktok".
            init_date: Data inicial no formato 2025-01-01.
            end_date: Data final no formato 2025-01-01.
            blog_id: blogId da marca (obtido em get_brands).
        """
        if platform not in ADS:
            return {"error": f"platform inválida: {platform!r}", "valid": sorted(ADS)}
        return await _fetch_ads(client, platform, init_date, end_date, blog_id)

    @mcp.tool()
    async def get_facebookads_campaigns(init_date: str, end_date: str, blog_id: int) -> Any:
        """Campanhas do Facebook Ads. Datas no formato 2025-01-01. blog_id de get_brands."""
        return await _fetch_ads(client, "facebook", init_date, end_date, blog_id)

    @mcp.tool()
    async def get_googleads_campaigns(init_date: str, end_date: str, blog_id: int) -> Any:
        """Campanhas do Google Ads. Datas no formato 2025-01-01. blog_id de get_brands."""
        return await _fetch_ads(client, "google", init_date, end_date, blog_id)

    @mcp.tool()
    async def get_tiktokads_campaigns(init_date: str, end_date: str, blog_id: int) -> Any:
        """Campanhas do TikTok Ads. Datas no formato 2025-01-01. blog_id de get_brands."""
        return await _fetch_ads(client, "tiktok", init_date, end_date, blog_id)
