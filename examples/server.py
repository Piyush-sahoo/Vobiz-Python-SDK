# -*- coding: utf-8 -*-
"""
examples/server.py — Vobiz Answer Server

Serves VobizXML when Vobiz calls your answer URL.
Uses the SDK's own XML builder to construct the response.

Run:
    python examples/server.py

Then expose it:
    ngrok http 5001

Copy the ngrok HTTPS URL into .env as:
    ANSWER_URL=https://<ngrok-id>.ngrok-free.dev/answer
"""
import os
import sys

# Make sure the SDK root is on the path when running from examples/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, Response
from dotenv import load_dotenv
from vobiz import vobizxml

load_dotenv()

app = Flask(__name__)


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    """
    Vobiz calls this URL when the outbound call is answered.
    We respond with VobizXML built using the SDK.
    """
    call_uuid  = request.values.get('CallUUID', 'unknown')
    from_number = request.values.get('From', 'unknown')
    to_number   = request.values.get('To', 'unknown')

    print(f"\n[/answer] Incoming call answered")
    print(f"  CallUUID : {call_uuid}")
    print(f"  From     : {from_number}")
    print(f"  To       : {to_number}")

    response = vobizxml.ResponseElement()

    # IVR: Ask for input instead of killing the call immediately
    get_digits = response.add_get_digits(
        action="/handle-input",
        method="POST",
        num_digits=1,
        timeout=5
    )

    get_digits.add_speak(
        "Hello! Welcome to the Vobiz Python SDK demo. "
        "Press 1 for sales, press 2 for support.",
        voice="WOMAN",
        language="en-US",
    )

    # Fallback if no input
    response.add_speak(
        "No input received. Goodbye!",
        voice="WOMAN",
        language="en-US",
    )
    response.add_hangup()

    xml = response.to_string(pretty=False)
    print(f"  Responding with XML:\n  {xml}\n")

    return Response(xml, status=200, mimetype='application/xml')


@app.route('/handle-input', methods=['GET', 'POST'])
def handle_input():
    """
    Handles digit input from the caller.
    """
    digit = request.values.get('Digits', '')

    print(f"\n[/handle-input] Received input: {digit}")

    response = vobizxml.ResponseElement()

    if digit == "1":
        response.add_speak(
            "You selected sales. Our team will contact you soon.",
            voice="WOMAN",
            language="en-US",
        )
    elif digit == "2":
        response.add_speak(
            "You selected support. Please hold while we assist you.",
            voice="WOMAN",
            language="en-US",
        )
    else:
        response.add_speak(
            "Invalid input received. Goodbye!",
            voice="WOMAN",
            language="en-US",
        )

    response.add_hangup()

    xml = response.to_string(pretty=False)
    print(f"  Responding with XML:\n  {xml}\n")

    return Response(xml, status=200, mimetype='application/xml')


@app.route('/hangup', methods=['GET', 'POST'])
def hangup():
    """
    Optional: Vobiz calls this URL when the call ends.
    """
    call_uuid = request.values.get('CallUUID', 'unknown')
    duration  = request.values.get('Duration', 'unknown')
    status    = request.values.get('CallStatus', 'unknown')

    print(f"\n[/hangup] Call ended")
    print(f"  CallUUID : {call_uuid}")
    print(f"  Status   : {status}")
    print(f"  Duration : {duration}s\n")

    return Response('OK', status=200)


@app.route('/status', methods=['GET', 'POST'])
def status():
    """
    Optional: Vobiz status callback.
    """
    print(f"\n[/status] Status callback: {dict(request.values)}\n")
    return Response('OK', status=200)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"\n Vobiz Answer Server starting on http://localhost:{port}")
    print(f" Endpoints:")
    print(f"   GET/POST /answer  — VobizXML response")
    print(f"   GET/POST /hangup  — hangup callback")
    print(f"   GET/POST /status  — status callback")
    print(f"\n NOTE: macOS AirPlay Receiver uses port 5000.")
    print(f" This server runs on port {port} by default.")
    print(f" Next step: run  ngrok http {port}")
    print(f" Then update .env:  ANSWER_URL=https://<ngrok-id>.ngrok-free.app/answer\n")
    app.run(host='0.0.0.0', port=port, debug=True)