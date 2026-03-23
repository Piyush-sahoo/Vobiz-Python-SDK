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


def test_list_inventory_numbers(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.list_inventory(
        country="US",
        page=2,
        per_page=50,
    )

    req = captured["request"]
    assert req.method == "GET"
    assert req.url.startswith(
        "https://api.vobiz.ai/api/v1/account/MA_TEST/inventory/numbers"
    )
    assert "country=US" in (req.url or "")
    assert "page=2" in (req.url or "")
    assert "per_page=50" in (req.url or "")


def test_purchase_from_inventory(monkeypatch):
    import json

    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.purchase_from_inventory(
        e164="+14155550100",
        currency="USD",
    )

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/numbers/purchase-from-inventory"
    )
    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["e164"] == "+14155550100"
    assert body["currency"] == "USD"


def test_release_phone_number(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.release("%2B14155550100")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/numbers/%2B14155550100"
    )


def test_assign_number_to_trunk(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.assign_to_trunk("%2B1234567890", trunk_group_id="TRUNK_ID")

    req = captured["request"]
    assert req.method == "POST"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/numbers/%2B1234567890/assign"
    )
    import json

    body = json.loads(req.body.decode() if isinstance(req.body, (bytes, bytearray)) else req.body)
    assert body["trunk_group_id"] == "TRUNK_ID"


def test_unassign_number_from_trunk(monkeypatch):
    captured = _capture(monkeypatch)
    client = vobiz.RestClient(auth_id="MA_TEST", auth_token="TOKEN")

    client.phone_numbers.unassign_from_trunk("%2B1234567890")

    req = captured["request"]
    assert req.method == "DELETE"
    assert (
        req.url
        == "https://api.vobiz.ai/api/v1/account/MA_TEST/numbers/%2B1234567890/assign"
    )

