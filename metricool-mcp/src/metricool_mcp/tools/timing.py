"""Ferramenta de melhor horário para publicar."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient, safe_call
from ..networks import BEST_TIME_PROVIDERS


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.tool()
    async def get_best_time_to_post(
        start: str,
        end: str,
        blog_id: int,
        provider: str,
        timezone: str,
    ) -> Any:
        """Retorna os melhores horários para publicar em uma rede.

        A resposta é uma lista de horas/dias com um valor: quanto maior o valor,
        melhor o horário. Prefira janelas de no máximo 1 semana. Se houver dia
        mas não hora, use início e fim do dia.

        Args:
            start: Data inicial no formato 2025-01-01.
            end: Data final no formato 2025-01-01.
            blog_id: blogId da marca (obtido em get_brands).
            provider: "twitter", "facebook", "instagram", "linkedin", "youtube"
                ou "tiktok".
            timezone: Timezone da marca, ex.: "America/Sao_Paulo" (de get_brands).
        """
        if provider not in BEST_TIME_PROVIDERS:
            return {"error": f"provider inválido: {provider!r}", "valid": list(BEST_TIME_PROVIDERS)}
        params = {
            "start": f"{start}T00:00:00",
            "end": f"{end}T23:59:59",
            "timezone": timezone,
            "blogId": blog_id,
        }
        return await safe_call(client.get(f"/v2/scheduler/besttimes/{provider}", params=params))
