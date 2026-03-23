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


def test_create_ip_acl(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.create(
        ip_address="203.0.113.50",
        description="Office static IP",
        enabled=True,
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/ip-acl"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["ip_address"] == "203.0.113.50"
    assert body["description"] == "Office static IP"
    assert body["enabled"] is True


def test_list_ip_acls(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.list(limit=20, offset=0)

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/account/MA_TEST/trunks/ip-acl"
    )
    assert "limit=20" in (req.url or "")
    assert "offset=0" in (req.url or "")


def test_get_ip_acl(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.get("ACL_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/ip-acl/ACL_ID"
    )


def test_update_ip_acl(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.update("ACL_ID", ip_address="192.168.1.200")

    req = captured["request"]
    assert req.method == "PUT"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/ip-acl/ACL_ID"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["ip_address"] == "192.168.1.200"


def test_delete_ip_acl(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.ip_access_control_lists.delete("ACL_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/ip-acl/ACL_ID"
    )

