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


def test_list_recordings(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.recordings.list(
        limit=50,
        offset=1,
        call_uuid="CALL_ID",
        recording_type="mp3",
        from_number="+111111111",
        to_number="+222222222",
    )

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/Account/MA_TEST/Recording/"
    )
    assert "limit=50" in (req.url or "")
    assert "offset=1" in (req.url or "")
    assert "call_uuid=CALL_ID" in (req.url or "")
    assert "recording_type=mp3" in (req.url or "")
    assert "from_number=%2B111111111" in (req.url or "") or "from_number=+111111111" in (req.url or "")
    assert "to_number=%2B222222222" in (req.url or "") or "to_number=+222222222" in (req.url or "")


def test_get_recording(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.recordings.get("REC_ID")

    req = captured["request"]
    assert req.method == "GET"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Recording/REC_ID/"
    )


def test_delete_recording(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.recordings.delete("REC_ID")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/Account/MA_TEST/Recording/REC_ID/"
    )

