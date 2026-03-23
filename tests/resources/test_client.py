import json

import vobiz


def test_client_sets_vobiz_headers(monkeypatch):
    captured = {}

    def capture_send(self, request, **kwargs):
        captured["request"] = request
        from requests import Response

        resp = Response()
        resp.status_code = 200
        resp._content = b"{}"
        resp.headers["Content-Type"] = "application/json"
        return resp

    # Patch all Session.send calls
    monkeypatch.setattr("requests.sessions.Session.send", capture_send, raising=True)

    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN_TEST")

    # any call will do to exercise request/headers; use a simple list
    try:
        client.calls.list()
    except Exception:
        # we only care about the constructed request here
        pass

    req = captured["request"]
    assert req.headers["X-Auth-ID"] == "MA_TEST"
    assert req.headers["X-Auth-Token"] == "TOKEN_TEST"
    assert req.headers["Content-Type"] == "application/json"
