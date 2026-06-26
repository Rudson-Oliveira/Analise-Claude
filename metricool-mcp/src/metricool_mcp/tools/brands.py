"""Ferramentas de marcas (brands) e diagnóstico."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient, safe_call


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.tool()
    async def get_brands() -> Any:
        """Lista as marcas (brands) da sua conta Metricool.

        Cada marca traz, entre outros campos, o ``blogId`` (o id usado em todas
        as demais ferramentas), o nome e o ``timezone`` da marca. Use o
        ``timezone`` ao agendar posts e ao consultar concorrentes/melhores
        horários.

        Apenas Instagram, Facebook, Twitch, YouTube, Twitter (X) e Bluesky
        suportam análise de concorrentes.
        """
        return await safe_call(client.get("/v2/settings/brands"))

    @mcp.tool()
    async def find_brand(query: str) -> Any:
        """Resolve uma marca pelo nome (busca parcial, case-insensitive).

        Atalho prático para descobrir o ``blogId`` a partir do nome da marca,
        sem precisar inspecionar a lista inteira.

        Args:
            query: Parte do nome da marca, ex.: "Hospitalar".
        """
        brands = await safe_call(client.get("/v2/settings/brands"))
        if isinstance(brands, dict) and "error" in brands:
            return brands
        items = brands if isinstance(brands, list) else brands.get("data", brands)
        if not isinstance(items, list):
            return {"error": "Formato inesperado da lista de marcas", "detail": brands}

        q = query.casefold().strip()
        matches = [
            b
            for b in items
            if isinstance(b, dict)
            and q in str(b.get("label") or b.get("title") or b.get("name") or "").casefold()
        ]
        return {"query": query, "matches": matches, "count": len(matches)}

    @mcp.tool()
    async def metricool_status() -> Any:
        """Diagnóstico do servidor: confirma credenciais e conectividade.

        Útil como primeira chamada para validar a configuração antes de operar.
        """
        missing = client.settings.missing_credentials()
        status: dict[str, Any] = {
            "base_url": client.settings.base_url,
            "user_id_present": bool(client.settings.user_id),
            "token_present": bool(client.settings.user_token),
            "missing_env": missing,
        }
        if missing:
            status["ok"] = False
            status["hint"] = "Defina as variáveis de ambiente ausentes e reinicie o servidor."
            return status

        ping = await safe_call(client.get("/v2/settings/brands"))
        if isinstance(ping, dict) and "error" in ping:
            status["ok"] = False
            status["api_error"] = ping
        else:
            items = ping if isinstance(ping, list) else ping.get("data", [])
            status["ok"] = True
            status["brands_reachable"] = True
            status["brand_count"] = len(items) if isinstance(items, list) else None
        return status
