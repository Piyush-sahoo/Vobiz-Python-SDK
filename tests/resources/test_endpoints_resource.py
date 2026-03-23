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


def test_create_endpoint(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.endpoints.create(
        username="user1",
        password="secret",
        alias="Desk Phone",
        application="APP_ID",
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Endpoint/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["username"] == "user1"
    assert body["password"] == "secret"
    assert body["alias"] == "Desk Phone"
    assert body["application"] == "APP_ID"


def test_list_endpoints(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.endpoints.list(limit=20, offset=0, username__contains="john")

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/Account/MA_TEST/Endpoint/"
    )
    assert "limit=20" in (req.url or "")
    assert "offset=0" in (req.url or "")
    assert "username__contains=john" in (req.url or "")


def test_get_endpoint(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.endpoints.get("EP_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Endpoint/EP_ID/"
    )


def test_update_endpoint(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.endpoints.update("EP_ID", alias="Softphone", password="newpass")

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Endpoint/EP_ID/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["alias"] == "Softphone"
    assert body["password"] == "newpass"


def test_delete_endpoint(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.endpoints.delete("EP_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Endpoint/EP_ID/"
    )

