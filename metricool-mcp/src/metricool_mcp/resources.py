"""Resources e prompts MCP — contexto e fluxos reutilizáveis."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from .client import MetricoolClient, safe_call


def register(mcp: FastMCP, client: MetricoolClient) -> None:
    @mcp.resource("metricool://brands")
    async def brands_resource() -> str:
        """Lista de marcas da conta como recurso consultável (JSON)."""
        data = await safe_call(client.get("/v2/settings/brands"))
        return json.dumps(data, ensure_ascii=False, indent=2)

    @mcp.prompt()
    def weekly_report(brand: str) -> str:
        """Prompt: monta um relatório semanal de desempenho da marca."""
        return (
            f"Gere um relatório semanal de redes sociais para a marca '{brand}'.\n"
            "Passos:\n"
            "1. Use find_brand para obter o blogId e o timezone.\n"
            "2. Para os últimos 7 dias, colete analytics das redes ativas "
            "(get_instagram_posts, get_facebook_posts, etc.).\n"
            "3. Resuma alcance, engajamento, melhores posts e variação vs. período "
            "anterior.\n"
            "4. Liste 3 recomendações acionáveis e os melhores horários "
            "(get_best_time_to_post) para a próxima semana."
        )

    @mcp.prompt()
    def schedule_campaign(brand: str, theme: str) -> str:
        """Prompt: planeja e agenda uma campanha de conteúdo."""
        return (
            f"Planeje uma campanha de conteúdo para a marca '{brand}' sobre "
            f"'{theme}'.\n"
            "1. find_brand -> blogId + timezone.\n"
            "2. get_best_time_to_post para cada rede alvo.\n"
            "3. Proponha o calendário (data, rede, texto, mídia) e confirme comigo.\n"
            "4. Para cada mídia, chame normalize_media_url.\n"
            "5. Após minha aprovação, use schedule_post para cada item."
        )
