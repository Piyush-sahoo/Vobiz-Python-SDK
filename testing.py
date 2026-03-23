# -*- coding: utf-8 -*-
"""
testing.py — Vobiz SDK end-to-end sanity test

Reads credentials from .env and exercises every major resource.
Run:
    in another terminal run 
    ngrok http 5001 
    
    and then run
    python testing.py
"""

import os
import sys
import time
import json
import threading
import subprocess

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))
import vobiz


# ── helpers ────────────────────────────────────────────────────────────────────

PASS  = "[PASS]"
FAIL  = "[FAIL]"
SKIP  = "[SKIP]"
SEP   = "─" * 60

results = []   # (label, status, detail)


def section(title):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)


def run(label, fn):
    try:
        result = fn()
        detail = repr(result)[:120] if result is not None else "(no content)"
        print(f"  {PASS}  {label}")
        print(f"         {detail}")
        results.append((label, "PASS", ""))
        return result
    except Exception as e:
        msg = str(e)
        print(f"  {FAIL}  {label}")
        print(f"         {msg}")
        results.append((label, "FAIL", msg))
        return None


def skip(label, reason):
    print(f"  {SKIP}  {label}  ({reason})")
    results.append((label, "SKIP", reason))


# ── answer server ──────────────────────────────────────────────────────────────

def start_answer_server(port=5001):
    """Start a minimal Flask answer server in a background thread."""
    try:
        from flask import Flask, Response
        app = Flask(__name__)

        @app.route("/answer", methods=["GET", "POST"])
        def answer():
            xml = (
                "<Response>"
                "<Speak voice='WOMAN' language='en-US'>"
                "SDK test call. Please wait."
                "</Speak>"
                "<Wait length='30'/>"
                "</Response>"
            )
            return Response(xml, status=200, mimetype="application/xml")

        t = threading.Thread(
            target=lambda: app.run(port=port, use_reloader=False, debug=False),
            daemon=True,
        )
        t.start()
        time.sleep(1)  # give Flask a moment to bind
        return True
    except Exception as e:
        print(f"  [WARN] Could not start answer server: {e}")
        return False


def get_ngrok_url(timeout=12):
    """
    Start ngrok tunnel on port and return the public HTTPS URL.
    Polls the ngrok local API until tunnel is ready.
    """
    import requests as req

    time.sleep(1)

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = req.get("http://localhost:4040/api/tunnels", timeout=2)
            tunnels = r.json().get("tunnels", [])
            for t in tunnels:
                url = t.get("public_url", "")
                if url.startswith("https://"):
                    return url
        except Exception:
            pass
        time.sleep(1)

    return None


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'═'*60}")
    print("  Vobiz SDK — End-to-End Test")
    print(f"{'═'*60}")

    auth_id     = os.environ.get("VOBIZ_AUTH_ID")
    auth_token  = os.environ.get("VOBIZ_AUTH_TOKEN")
    from_number = os.environ.get("FROM_PHONE_NUMBER")
    to_number   = os.environ.get("TO_PHONE_NUMBER")

    # Number that is NOT assigned to any trunk — safe for attach/detach test
    ATTACH_TEST_NUMBER = "+911171366943"

    if not auth_id or not auth_token:
        print("\n  ERROR: VOBIZ_AUTH_ID / VOBIZ_AUTH_TOKEN not set in .env")
        sys.exit(1)

    print(f"\n  Auth ID   : {auth_id}")
    print(f"  Auth Token: {'*' * 8}{auth_token[-6:]}")

    client = vobiz.RestClient(auth_id=auth_id, auth_token=auth_token)

    # ── 1. Account ──────────────────────────────────────────────────────────────
    section("1. Account")
    run("GET  /auth/me",           lambda: client.accounts.get())
    run("GET  get_balance(INR)",   lambda: client.accounts.get_balance(auth_id, "INR"))
    run("GET  get_transactions()", lambda: client.accounts.get_transactions(auth_id, limit=5, offset=0))
    run("GET  get_concurrency()",  lambda: client.accounts.get_concurrency(auth_id))

    # ── 2. Calls — list ─────────────────────────────────────────────────────────
    section("2. Calls — list live / queued")
    run("GET  list_live()",   lambda: client.calls.list_live())
    run("GET  list_queued()", lambda: client.calls.list_queued())

    # ── 2b. Calls — live call: record / play / speak ────────────────────────────
    section("2b. Calls — Live Call (record / play / speak)")

    answer_url = None

    if from_number and to_number:
        print("  Starting local answer server on port 5001...")
        server_ok = start_answer_server(port=5001)

        if server_ok:
            print("  Starting ngrok tunnel...")
            ngrok_url = get_ngrok_url(timeout=15)
            if ngrok_url:
                answer_url = f"{ngrok_url}/answer"
                print(f"  Answer URL: {answer_url}")
            else:
                print("  [WARN] ngrok tunnel did not start in time — skipping live call tests")

    if answer_url:
        call_result = run("POST create call",
            lambda: client.calls.create(
                from_=from_number,
                to_=to_number,
                answer_url=answer_url,
                answer_method="GET",
            )
        )

        call_uuid = None
        if call_result is not None:
            call_uuid = (
                getattr(call_result, "request_uuid", None)
                or getattr(call_result, "call_uuid", None)
                or getattr(call_result, "uuid", None)
            )

        if call_uuid:
            print(f"\n         Call UUID: {call_uuid}")
            print("         Waiting 10s for call to connect...")
            time.sleep(10)

            run("POST start_recording",
                lambda: client.calls.start_recording(
                    call_uuid, time_limit=30, file_format="mp3"
                )
            )

            run("POST play_audio",
                lambda: client.calls.play_audio(
                    call_uuid,
                    urls=["https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"],
                    length=5,
                    legs="aleg",
                    loop=False,
                )
            )
            time.sleep(3)

            run("DEL  stop_audio",
                lambda: client.calls.stop_audio(call_uuid))

            run("POST speak_text",
                lambda: client.calls.speak_text(
                    call_uuid,
                    text="This is a live SDK test. All systems are working correctly.",
                    voice="WOMAN",
                    language="en-US",
                    legs="aleg",
                )
            )
            time.sleep(4)

            run("DEL  stop_speak",
                lambda: client.calls.stop_speak(call_uuid))

            run("DEL  stop_recording",
                lambda: client.calls.stop_recording(call_uuid))

            run("DEL  hangup call",
                lambda: client.calls.hangup(call_uuid))
        else:
            skip("start_recording / play_audio / speak_text / stop_* / hangup",
                 "call creation did not return a UUID")
    else:
        skip("Live call tests (record / play / speak)",
             "FROM/TO numbers not set or ngrok failed to start")


    # ── 3. Applications ─────────────────────────────────────────────────────────
    section("3. Applications")
    app_result = run("POST create application",
        lambda: client.applications.create(
            name="SDK-Test-App",
            answer_url="https://example.com/answer",
            hangup_url="https://example.com/hangup",
            application_type="XML",
        )
    )

    app_id = None
    if app_result is not None:
        app_id = getattr(app_result, "app_id", None) or getattr(app_result, "id", None)

    run("GET  list applications", lambda: client.applications.list())

    if app_id:
        run(f"GET  get application {app_id}",
            lambda: client.applications.get(app_id))
        run(f"POST update application {app_id}",
            lambda: client.applications.update(app_id, name="SDK-Test-App-Updated"))
        run(f"DEL  delete application {app_id}",
            lambda: client.applications.delete(app_id))
    else:
        skip("GET/POST/DEL application by id", "create did not return app_id")

    # ── 3b. Applications — attach / detach number ───────────────────────────────
    section("3b. Applications — Link Numbers")

    link_app_result = run("POST create app for link test",
        lambda: client.applications.create(
            name="SDK-Link-Test-App",
            answer_url="https://example.com/answer",
            application_type="XML",
        )
    )
    link_app_id = None
    if link_app_result is not None:
        link_app_id = (
            getattr(link_app_result, "app_id", None)
            or getattr(link_app_result, "id", None)
        )

    if link_app_id:
        run(f"POST attach_number {ATTACH_TEST_NUMBER} → app",
            lambda: client.applications.attach_number(ATTACH_TEST_NUMBER, link_app_id))
        run(f"DEL  detach_number {ATTACH_TEST_NUMBER}",
            lambda: client.applications.detach_number(ATTACH_TEST_NUMBER))
        run(f"DEL  delete link test app {link_app_id}",
            lambda: client.applications.delete(link_app_id))
    else:
        skip("attach_number / detach_number", "app creation failed")

    # ── 4. Phone Numbers ────────────────────────────────────────────────────────
    section("4. Phone Numbers")
    run("GET  list owned numbers",
        lambda: client.phone_numbers.list(page=1, per_page=10))
    run("GET  list_inventory(IN)",
        lambda: client.phone_numbers.list_inventory(country="IN", page=1, per_page=10))

    # ── 5. SIP Endpoints ────────────────────────────────────────────────────────
    section("5. SIP Endpoints")
    ep_result = run("POST create endpoint",
        lambda: client.endpoints.create(
            username="sdktestuser",
            password="TestPass@123",
            alias="SDK Test User",
        )
    )

    ep_id = None
    if ep_result is not None:
        ep_id = (
            getattr(ep_result, "endpoint_id", None)
            or getattr(ep_result, "id", None)
        )

    run("GET  list endpoints", lambda: client.endpoints.list())

    if ep_id:
        run(f"GET  get endpoint {ep_id}",
            lambda: client.endpoints.get(ep_id))
        run(f"POST update endpoint {ep_id}",
            lambda: client.endpoints.update(ep_id, alias="SDK Test User Updated"))
        run(f"DEL  delete endpoint {ep_id}",
            lambda: client.endpoints.delete(ep_id))
    else:
        skip("GET/POST/DEL endpoint by id", "create did not return endpoint_id")

    # ── 6. SIP Trunks ───────────────────────────────────────────────────────────
    section("6. SIP Trunks")
    trunks_result = run("GET  list sip_trunks", lambda: client.sip_trunks.list())

    trunk_id = None
    if trunks_result is not None:
        objs = getattr(trunks_result, "objects", None) or (
            list(trunks_result) if hasattr(trunks_result, "__iter__") else []
        )
        if objs:
            trunk_id = (
                getattr(objs[0], "id", None)
                or getattr(objs[0], "trunk_id", None)
            )

    if trunk_id:
        run(f"GET  get trunk {trunk_id}",
            lambda: client.sip_trunks.get(trunk_id))
    else:
        skip("GET trunk by id", "no trunks found or list failed")

    # ── 7. Credentials ──────────────────────────────────────────────────────────
    section("7. Credentials")
    run("GET  list credentials", lambda: client.credentials.list())

    # ── 8. IP ACLs ──────────────────────────────────────────────────────────────
    section("8. IP Access Control Lists")
    acl_result = run("POST create ip-acl",
        lambda: client.ip_access_control_lists.create(
            ip_address="8.8.8.8",
            description="SDK test ACL",
        )
    )

    acl_id = None
    if acl_result is not None:
        acl_id = (
            getattr(acl_result, "id", None)
            or getattr(acl_result, "acl_id", None)
        )

    run("GET  list ip-acls", lambda: client.ip_access_control_lists.list())

    if acl_id:
        run(f"DEL  delete acl {acl_id}",
            lambda: client.ip_access_control_lists.delete(acl_id))
    else:
        skip("DEL ip-acl by id", "create did not return id")

    # ── 9. Origination URIs ─────────────────────────────────────────────────────
    section("9. Origination URIs")
    run("GET  list origination_uris", lambda: client.origination_uris.list())

    # ── 10. Recordings ──────────────────────────────────────────────────────────
    section("10. Recordings")
    run("GET  list recordings", lambda: client.recordings.list())

    # export() uses JWT auth (access token), not API key — not testable here
    skip("POST export recordings",
         "requires JWT access token (different auth scheme) — not API key auth")

    # bulk_delete with a far-future date so nothing is actually deleted
    run("DEL  bulk_delete recordings (safe future date — no-op)",
        lambda: client.recordings.bulk_delete(
            **{"add_time__gte": "2099-01-01 00:00:00",
               "add_time__lte": "2099-01-31 23:59:59"}
        )
    )

    # ── 11. CDRs ────────────────────────────────────────────────────────────────
    section("11. CDRs")
    run("GET  list cdrs", lambda: client.cdrs.list())

    # ── Summary ─────────────────────────────────────────────────────────────────
    print(f"\n{'═'*60}")
    print("  Summary")
    print(f"{'═'*60}")

    passed  = sum(1 for _, s, _ in results if s == "PASS")
    failed  = sum(1 for _, s, _ in results if s == "FAIL")
    skipped = sum(1 for _, s, _ in results if s == "SKIP")

    print(f"\n  Total : {len(results)}")
    print(f"  Pass  : {passed}")
    print(f"  Fail  : {failed}")
    print(f"  Skip  : {skipped}")

    if failed:
        print(f"\n  Failed tests:")
        for label, status, detail in results:
            if status == "FAIL":
                print(f"    - {label}: {detail}")

    print()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
