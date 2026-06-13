"""Registro de endpoints de analytics e utilitários de data.

A API do Metricool é inconsistente: a maioria dos endpoints novos vive em
``/v2/analytics/...`` e usa ``from``/``to`` com datas ISO; alguns endpoints
legados vivem em ``/stats/...`` e usam ``start``/``end`` com datas compactas
(``YYYYMMDD``). Este módulo centraliza essas diferenças para que as ferramentas
fiquem triviais e consistentes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalyticsEndpoint:
    path: str
    start_param: str = "from"
    end_param: str = "to"
    style: str = "iso"  # "iso" -> 2025-01-01T00:00:00 | "compact" -> 20250101


# Conteúdo orgânico por rede ------------------------------------------------
ANALYTICS: dict[str, AnalyticsEndpoint] = {
    "instagram_posts": AnalyticsEndpoint("/v2/analytics/posts/instagram"),
    "instagram_reels": AnalyticsEndpoint("/v2/analytics/reels/instagram"),
    "instagram_stories": AnalyticsEndpoint(
        "/v2/analytics/stories/instagram", start_param="start", end_param="end"
    ),
    "facebook_posts": AnalyticsEndpoint("/v2/analytics/posts/facebook"),
    "facebook_reels": AnalyticsEndpoint("/v2/analytics/reels/facebook"),
    "facebook_stories": AnalyticsEndpoint("/v2/analytics/stories/facebook"),
    "tiktok_videos": AnalyticsEndpoint("/v2/analytics/posts/tiktok"),
    "threads_posts": AnalyticsEndpoint("/v2/analytics/posts/threads"),
    "bluesky_posts": AnalyticsEndpoint("/v2/analytics/posts/bluesky"),
    "linkedin_posts": AnalyticsEndpoint("/v2/analytics/posts/linkedin"),
    "pinterest_pins": AnalyticsEndpoint("/v2/analytics/posts/pinterest"),
    "youtube_videos": AnalyticsEndpoint("/v2/analytics/posts/youtube"),
    # Legados em /stats com data compacta.
    "x_posts": AnalyticsEndpoint(
        "/stats/twitter/posts", start_param="start", end_param="end", style="compact"
    ),
    "twitch_videos": AnalyticsEndpoint(
        "/stats/twitch/videos", start_param="start", end_param="end", style="compact"
    ),
}

# Campanhas de anúncios ------------------------------------------------------
ADS: dict[str, AnalyticsEndpoint] = {
    "facebook": AnalyticsEndpoint(
        "/stats/facebookads/campaigns", start_param="start", end_param="end", style="compact"
    ),
    "google": AnalyticsEndpoint(
        "/stats/adwords/campaigns", start_param="start", end_param="end", style="compact"
    ),
    "tiktok": AnalyticsEndpoint("/v2/analytics/campaigns/tiktokads"),
}

# Redes que suportam análise de concorrentes.
COMPETITOR_NETWORKS = ("instagram", "facebook", "twitch", "youtube", "twitter", "bluesky")

# Provedores aceitos pelo endpoint de "melhor horário".
BEST_TIME_PROVIDERS = ("twitter", "facebook", "instagram", "linkedin", "youtube", "tiktok")


def build_date_params(
    endpoint: AnalyticsEndpoint, init_date: str, end_date: str
) -> dict[str, str]:
    """Monta os parâmetros de data conforme o estilo do endpoint.

    ``init_date``/``end_date`` devem chegar como ``YYYY-MM-DD``.
    """
    if endpoint.style == "compact":
        return {
            endpoint.start_param: init_date.replace("-", ""),
            endpoint.end_param: end_date.replace("-", ""),
        }
    return {
        endpoint.start_param: f"{init_date}T00:00:00",
        endpoint.end_param: f"{end_date}T23:59:59",
    }
