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


def test_create_call(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.calls.create(
        from_="14155551234",
        to_="14155555678",
        answer_url="https://example.com/answer",
    )

    req = captured["request"]
    assert req.method == "POST"
    assert req.url == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Call/"
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["from"] == "14155551234"
    assert body["to"] == "14155555678"


def test_transfer_call(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")
    call_uuid = "CALL_UUID"

    client.calls.transfer(
        call_uuid,
        legs="both",
        aleg_url="https://example.com/aleg",
        aleg_method="POST",
        bleg_url="https://example.com/bleg",
        bleg_method="POST",
    )

    req = captured["request"]
    assert req.method == "POST"
    assert req.url == f"https://api.vobiz.ai/api/v1/Account/MA_TEST/Call/{call_uuid}/"
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["legs"] == "both"
    assert body["aleg_url"] == "https://example.com/aleg"
    assert body["bleg_url"] == "https://example.com/bleg"


def test_hangup_call(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")
    call_uuid = "CALL_UUID"

    client.calls.hangup(call_uuid)

    req = captured["request"]
    assert req.method == "DELETE"
    assert req.url == f"https://api.vobiz.ai/api/v1/Account/MA_TEST/Call/{call_uuid}/"


def test_list_live_calls(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.calls.list_live()

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith("https://api.vobiz.ai/api/v1/Account/MA_TEST/Call/")
    # status should be a query param
    assert "status=live" in (req.url or "")


def test_list_queued_calls(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.calls.list_queued()

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith("https://api.vobiz.ai/api/v1/Account/MA_TEST/Call/")
    assert "status=queued" in (req.url or "")


def test_get_live_call_detail(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")
    call_uuid = "CALL_UUID"

    client.calls.get_live(call_uuid)

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        f"https://api.vobiz.ai/api/v1/Account/MA_TEST/Call/{call_uuid}/"
    )
    assert "status=live" in (req.url or "")


def test_get_queued_call_detail(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")
    call_uuid = "CALL_UUID"

    client.calls.get_queued(call_uuid)

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        f"https://api.vobiz.ai/api/v1/Account/MA_TEST/Call/{call_uuid}/"
    )
    assert "status=queued" in (req.url or "")


def test_send_dtmf(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")
    call_uuid = "CALL_UUID"

    client.calls.send_digits(call_uuid, digits="1234", leg="both")

    req = captured["request"]
    assert req.method == "POST"
    assert req.url == f"https://api.vobiz.ai/api/v1/Account/MA_TEST/Call/{call_uuid}/DTMF/"
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["digits"] == "1234"
    assert body["leg"] == "both"


def test_api_error_raises(monkeypatch):
    import pytest
    from requests import Response

    def error_send(self, request, **kwargs):
        resp = Response()
        resp.status_code = 400
        resp._content = b'{"error": "invalid request"}'
        resp.headers["Content-Type"] = "application/json"
        return resp

    monkeypatch.setattr("requests.sessions.Session.send", error_send, raising=True)

    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    with pytest.raises(Exception):
        client.calls.create(
            from_="14155551234",
            to_="14155555678",
            answer_url="https://example.com/answer",
        )