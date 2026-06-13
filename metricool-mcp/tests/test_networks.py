from metricool_mcp.networks import ADS, ANALYTICS, AnalyticsEndpoint, build_date_params


def test_iso_style_uses_from_to_with_time():
    ep = ANALYTICS["instagram_posts"]
    params = build_date_params(ep, "2025-01-01", "2025-01-31")
    assert params == {"from": "2025-01-01T00:00:00", "to": "2025-01-31T23:59:59"}


def test_stories_use_start_end_params():
    ep = ANALYTICS["instagram_stories"]
    params = build_date_params(ep, "2025-01-01", "2025-01-02")
    assert set(params) == {"start", "end"}


def test_compact_style_strips_dashes():
    ep = ANALYTICS["x_posts"]
    params = build_date_params(ep, "2025-01-01", "2025-01-31")
    assert params == {"start": "20250101", "end": "20250131"}


def test_ads_registry_has_three_platforms():
    assert set(ADS) == {"facebook", "google", "tiktok"}


def test_endpoint_defaults():
    ep = AnalyticsEndpoint("/x")
    assert ep.start_param == "from" and ep.end_param == "to" and ep.style == "iso"
