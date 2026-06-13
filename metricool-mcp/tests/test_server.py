import httpx

from metricool_mcp.client import MetricoolClient
from metricool_mcp.config import Settings
from metricool_mcp.server import create_server


def test_server_registers_expected_tools():
    mcp, _ = create_server(Settings(user_token="t", user_id="1"))
    # FastMCP expõe as ferramentas registradas de forma assíncrona.
    import asyncio

    tools = asyncio.run(mcp.list_tools())
    names = {t.name for t in tools}

    expected = {
        "get_brands",
        "find_brand",
        "metricool_status",
        "get_analytics",
        "get_instagram_posts",
        "get_x_posts",
        "get_twitch_videos",
        "get_ads_campaigns",
        "get_facebookads_campaigns",
        "get_competitors",
        "schedule_post",
        "update_scheduled_post",
        "get_scheduled_posts",
        "delete_scheduled_post",
        "get_best_time_to_post",
        "normalize_media_url",
        "metricool_request",
    }
    missing = expected - names
    assert not missing, f"ferramentas ausentes: {missing}"


def test_named_analytics_tool_calls_correct_endpoint():
    import asyncio

    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, json={"ok": True})

    http = httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://app.metricool.com/api"
    )
    client = MetricoolClient(Settings(user_token="t", user_id="1"), http_client=http)
    mcp, _ = create_server(Settings(user_token="t", user_id="1"), client=client)

    asyncio.run(
        mcp.call_tool(
            "get_instagram_posts",
            {"init_date": "2025-01-01", "end_date": "2025-01-31", "blog_id": 99},
        )
    )
    assert captured["path"].endswith("/v2/analytics/posts/instagram")
    assert captured["params"]["blogId"] == "99"
    assert captured["params"]["from"] == "2025-01-01T00:00:00"
    asyncio.run(http.aclose())
