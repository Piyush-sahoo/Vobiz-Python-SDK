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


def test_get_account(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.accounts.get()

    req = captured["request"]
    assert req.method == "GET"
    assert req.url == "https://api.vobiz.ai/api/v1/auth/me"


def test_get_transactions(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.accounts.get_transactions("ACC_ID", limit=10, offset=20)

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith("https://api.vobiz.ai/api/v1/account/ACC_ID/transactions")
    assert "limit=10" in (req.url or "")
    assert "offset=20" in (req.url or "")


def test_get_balance(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.accounts.get_balance("ACC_ID", "USD")

    req = captured["request"]
    assert req.method == "GET"
    assert req.url == "https://api.vobiz.ai/api/v1/account/ACC_ID/balance/USD"


def test_get_concurrency(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.accounts.get_concurrency("ACC_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert req.url == "https://api.vobiz.ai/api/v1/account/ACC_ID/concurrency"

