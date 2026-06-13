import httpx
import pytest

from metricool_mcp.client import MetricoolClient, MetricoolError, safe_call
from metricool_mcp.config import Settings


def _settings(**kw):
    base = dict(user_token="tok", user_id="42", max_retries=2, backoff_base=0.0)
    base.update(kw)
    return Settings(**base)


def _client(handler, **kw):
    transport = httpx.MockTransport(handler)
    http = httpx.AsyncClient(transport=transport, base_url="https://app.metricool.com/api")
    return MetricoolClient(_settings(**kw), http_client=http)


async def test_injects_userid_and_integration_source():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["params"] = dict(request.url.params)
        seen["auth"] = request.headers.get("X-Mc-Auth")
        return httpx.Response(200, json={"ok": True})

    client = _client(handler)
    out = await client.get("/v2/settings/brands", params={"blogId": 7})
    assert out == {"ok": True}
    assert seen["params"]["userId"] == "42"
    assert seen["params"]["integrationSource"] == "MCP"
    assert seen["params"]["blogId"] == "7"
    assert seen["auth"] == "tok"
    await client.aclose()


async def test_drops_none_params():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["params"] = dict(request.url.params)
        return httpx.Response(200, json=[])

    client = _client(handler)
    await client.get("/x", params={"timezone": None, "blogId": 1})
    assert "timezone" not in seen["params"]
    await client.aclose()


async def test_retries_on_500_then_succeeds():
    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] < 2:
            return httpx.Response(500, json={"err": "boom"})
        return httpx.Response(200, json={"ok": 1})

    client = _client(handler)
    out = await client.get("/x")
    assert out == {"ok": 1}
    assert calls["n"] == 2
    await client.aclose()


async def test_raises_structured_error_on_4xx():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"message": "forbidden"})

    client = _client(handler)
    with pytest.raises(MetricoolError) as ei:
        await client.get("/x")
    assert ei.value.status == 403
    assert ei.value.detail == {"message": "forbidden"}
    await client.aclose()


async def test_safe_call_converts_error_to_dict():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="nope")

    client = _client(handler)
    out = await safe_call(client.get("/x"))
    assert out["status"] == 404
    assert "error" in out
    await client.aclose()


async def test_missing_credentials_returns_error_without_http():
    client = MetricoolClient(_settings(user_token=None))
    out = await safe_call(client.get("/x"))
    assert out["status"] is None
    assert "METRICOOL_USER_TOKEN" in out["detail"]["missing"]
    await client.aclose()
