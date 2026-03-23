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


def test_create_application(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.applications.create(
        name="App",
        answer_url="https://example.com/answer",
        hangup_url="https://example.com/hangup",
        application_type="voice",
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Application/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["name"] == "App"
    assert body["answer_url"] == "https://example.com/answer"
    assert body["hangup_url"] == "https://example.com/hangup"
    assert body["application_type"] == "voice"


def test_list_applications(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.applications.list(page=2, size=25, application_type="voice")

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/Account/MA_TEST/Application/"
    )
    assert "page=2" in (req.url or "")
    assert "size=25" in (req.url or "")
    assert "application_type=voice" in (req.url or "")


def test_get_application(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.applications.get("APP_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Application/APP_ID"
    )


def test_update_application(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.applications.update("APP_ID", name="NewName", application_type="voice")

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Application/APP_ID/"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["name"] == "NewName"
    assert body["application_type"] == "voice"


def test_delete_application(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.applications.delete("APP_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Application/APP_ID"
    )

