"""Ferramenta genérica (escape hatch) — o verdadeiro 'canivete suíço'.

Permite chamar QUALQUER endpoint da API do Metricool que ainda não tenha uma
ferramenta dedicada, com ``userId`` e ``integrationSource`` injetados
automaticamente. Cobre relatórios, métricas de série temporal, boards do
Pinterest, inbox e quaisquer endpoints futuros.
"""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..client import MetricoolClient, safe_call

_ALLOWED = {"GET", "POST", "PUT", "PATCH", "DELETE"}


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.tool()
    async def metricool_request(
        method: str,
        path: str,
        params: dict | None = None,
        body: dict | None = None,
    ) -> Any:
        """Chama um endpoint arbitrário da API do Metricool.

        Use quando nenhuma ferramenta dedicada cobrir o que você precisa. O
        ``blogId`` deve ir em ``params`` quando o endpoint exigir; ``userId`` e
        ``integrationSource`` são adicionados automaticamente.

        Args:
            method: GET, POST, PUT, PATCH ou DELETE.
            path: Caminho relativo à API, ex.: "/v2/analytics/posts/instagram"
                (a base https://app.metricool.com/api é adicionada).
            params: Query string como objeto JSON (ex.: {"blogId": 123}).
            body: Corpo JSON para POST/PUT/PATCH.

        Exemplos:
            metricool_request("GET", "/v2/settings/brands")
            metricool_request("GET", "/stats/instagram/community",
                              {"blogId": 123, "start": "20250101", "end": "20250131"})
        """
        verb = method.upper()
        if verb not in _ALLOWED:
            return {"error": f"método inválido: {method!r}", "valid": sorted(_ALLOWED)}
        return await safe_call(
            client.request(verb, path, params=params, json_body=body)
        )
