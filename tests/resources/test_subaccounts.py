import json

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


def test_create_subaccount(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.subaccounts.create(
        name="Sub",
        email="sub@example.com",
        rate_limit=10,
        permissions=["calls"],
        password="secret",
        phone="+1234567890",
        description="Test subaccount",
        enabled=True,
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/sub-accounts/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["name"] == "Sub"
    assert body["email"] == "sub@example.com"
    assert body["rate_limit"] == 10
    assert body["permissions"] == ["calls"]
    assert body["password"] == "secret"
    assert body["phone"] == "+1234567890"
    assert body["description"] == "Test subaccount"
    assert body["enabled"] is True


def test_list_subaccounts(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.subaccounts.list(page=2, size=50, active_only=True)

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/accounts/MA_TEST/sub-accounts/"
    )
    assert "page=2" in (req.url or "")
    assert "size=50" in (req.url or "")
    assert "active_only=true" in (req.url or "").lower()


def test_get_subaccount(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.subaccounts.get("SUB_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/sub-accounts/SUB_ID"
    )


def test_update_subaccount(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.subaccounts.update("SUB_ID", name="NewName", enabled=False)

    req = captured["request"]
    assert req.method == "PUT"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/sub-accounts/SUB_ID"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["name"] == "NewName"
    assert body["enabled"] is False


def test_delete_subaccount(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.subaccounts.delete("SUB_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/accounts/MA_TEST/sub-accounts/SUB_ID"
    )

