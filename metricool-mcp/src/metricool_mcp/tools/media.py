"""Ferramentas de mídia (normalização de URLs antes do agendamento)."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient, safe_call


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.tool()
    async def normalize_media_url(url: str) -> Any:
        """Normaliza uma URL de imagem/vídeo para uso no agendamento.

        O Metricool exige que as URLs de mídia sejam normalizadas antes de
        anexá-las a um post. Chame esta ferramenta para cada mídia e use a URL
        retornada no campo ``media`` de schedule_post / update_scheduled_post.

        Args:
            url: URL pública da mídia original.
        """
        return await safe_call(client.get("/actions/normalize/image/url", params={"url": url}))
