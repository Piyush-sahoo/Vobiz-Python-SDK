import vobiz


def _capture(monkeypatch):
    captured = {}

    def capture_send(self, request, **kwargs):
        captured["request"] = request
        from requests import Response

        resp = Response()
        resp.status_code = 200
        resp._content = b"{}"
        resp.headers["Content-Type"] = "application/json"
        return resp

    monkeypatch.setattr("requests.sessions.Session.send", capture_send, raising=True)
    return captured


def test_list_cdrs(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.cdrs.list(
        page=3,
        per_page=100,
        start_date="2026-03-01 00:00:00",
        end_date="2026-03-10 23:59:59",
        from_number="+111111111",
        to_number="+222222222",
        direction="outbound",
    )

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/account/MA_TEST/cdr"
    )
    assert "page=3" in (req.url or "")
    assert "per_page=100" in (req.url or "")
    assert "start_date=2026-03-01+00%3A00%3A00" in (req.url or "") or "start_date=2026-03-01+00:00:00" in (req.url or "")
    assert "end_date=2026-03-10+23%3A59%3A59" in (req.url or "") or "end_date=2026-03-10+23:59:59" in (req.url or "")
    assert "direction=outbound" in (req.url or "")
    assert "from_number=%2B111111111" in (req.url or "") or "from_number=+111111111" in (req.url or "")
    assert "to_number=%2B222222222" in (req.url or "") or "to_number=+222222222" in (req.url or "")

