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


def test_create_sip_trunk(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.sip_trunks.create(
        name="Main Trunk",
        inbound_uri="sip:inbound@example.com",
        outbound_uri="sip:outbound@example.com",
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/trunks"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["name"] == "Main Trunk"
    assert body["inbound_uri"] == "sip:inbound@example.com"
    assert body["outbound_uri"] == "sip:outbound@example.com"


def test_list_sip_trunks(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.sip_trunks.list(page=1, size=20)

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/account/MA_TEST/trunks"
    )
    assert "page=1" in (req.url or "")
    assert "size=20" in (req.url or "")


def test_get_sip_trunk(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.sip_trunks.get("TRUNK_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/trunks/TRUNK_ID"
    )


def test_update_sip_trunk(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.sip_trunks.update("TRUNK_ID", name="Updated")

    req = captured["request"]
    assert req.method == "PUT"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/trunks/TRUNK_ID"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["name"] == "Updated"


def test_delete_sip_trunk(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.sip_trunks.delete("TRUNK_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/trunks/TRUNK_ID"
    )

