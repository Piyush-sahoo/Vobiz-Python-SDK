# Vobiz Python SDK

The official Python SDK for the [Vobiz](https://vobiz.ai) voice & telephony platform.

Make outbound calls, manage SIP trunks, phone numbers, endpoints, and build dynamic call flows with VobizXML — all from Python.

---

## Table of Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [Making Your First Call](#making-your-first-call)
- [Receiving Calls — Answer Server](#receiving-calls--answer-server)
- [Local Development with ngrok](#local-development-with-ngrok)
- [Resources](#resources)
  - [Account](#account)
  - [Calls](#calls)
  - [Applications](#applications)
  - [Phone Numbers](#phone-numbers)
  - [SIP Endpoints](#sip-endpoints)
  - [SIP Trunks](#sip-trunks)
  - [Credentials](#credentials)
  - [IP Access Control Lists](#ip-access-control-lists)
  - [Origination URIs](#origination-uris)
  - [Recordings](#recordings)
  - [CDRs](#cdrs)
  - [Subaccounts](#subaccounts)
- [VobizXML — Call Flow Control](#vobizxml--call-flow-control)
- [Environment Variables](#environment-variables)
- [Running Tests](#running-tests)
- [License](#license)

---

## Installation

```bash
pip install vobiz-python
```

Or install from source:

```bash
git clone https://github.com/Piyush-sahoo/Vobiz-Python-SDK.git
cd Vobiz-Python-SDK
pip install -e .
```

**Requires Python 3.7+**

---

## Authentication

Vobiz uses `Auth ID` + `Auth Token` for all REST API calls. Find yours in the [Vobiz Console](https://console.vobiz.ai).

**Recommended:** store credentials in a `.env` file (never commit it to git):

```bash
cp .env.example .env
# Edit .env and fill in your real values
```

```python
import vobiz

# Reads VOBIZ_AUTH_ID and VOBIZ_AUTH_TOKEN from .env automatically
client = vobiz.RestClient()

# Or pass explicitly
client = vobiz.RestClient(auth_id="MA_XXXXXXXXXX", auth_token="your_token")
```

---

## Making Your First Call

```python
import vobiz

client = vobiz.RestClient()

response = client.calls.create(
    from_="+911234567890",          # Your Vobiz DID number
    to_="+919876543210",            # Destination number
    answer_url="https://your-server.com/answer",  # Returns VobizXML
    answer_method="GET",
)

print("Call UUID:", response.request_uuid)
```

When the call is answered, Vobiz makes an HTTP request to your `answer_url`. That URL must return **VobizXML** telling Vobiz what to do — speak text, play audio, record, collect digits, etc.

---

## Receiving Calls — Answer Server

Create a simple Flask server that returns VobizXML:

```python
# answer_server.py
from flask import Flask, request, Response
from vobiz import vobizxml

app = Flask(__name__)

@app.route('/answer', methods=['GET', 'POST'])
def answer():
    # Vobiz sends call details as query/form params
    call_uuid  = request.values.get('CallUUID')
    from_num   = request.values.get('From')
    to_num     = request.values.get('To')

    print(f"Incoming call {call_uuid}: {from_num} → {to_num}")

    # Build XML response using the SDK
    response = vobizxml.ResponseElement()
    response.add_speak(
        "Hello! You have reached our service. Thank you for calling.",
        voice="WOMAN",
        language="en-US",
    )
    response.add_hangup()

    return Response(response.to_string(), status=200, mimetype='application/xml')


@app.route('/hangup', methods=['GET', 'POST'])
def hangup():
    print("Call ended:", request.values.get('CallUUID'))
    print("Duration:", request.values.get('Duration'), "seconds")
    return Response('OK', status=200)


if __name__ == '__main__':
    # NOTE: macOS users — port 5000 is reserved by AirPlay Receiver.
    # Use port 5001 or higher.
    app.run(port=5001)
```

Run it:

```bash
python answer_server.py
```

---

## Local Development with ngrok

Your answer server must be reachable over the internet. Use [ngrok](https://ngrok.com) to expose your local server:

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 5001
```

ngrok will print a public HTTPS URL like:

```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:5001
```

Copy that URL and set it in your `.env`:

```
ANSWER_URL=https://abc123.ngrok-free.app/answer
```

Now trigger the call using `client.calls.create(...)` with the ngrok URL as your `answer_url`.

**Full flow:**
1. Your code fires an outbound call via `client.calls.create(...)`
2. The called phone rings
3. When answered, Vobiz calls your `ANSWER_URL` (via ngrok → your Flask server)
4. Your server returns VobizXML
5. Vobiz executes the XML — speaks text, plays audio, etc.
6. Call ends; Vobiz calls your `hangup_url` with final call details

---

## Resources

### Account

```python
# Get your account details
account = client.accounts.get()
print(account.auth_id, account.name)

# Get balance (currency: "INR", "USD", etc.)
balance = client.accounts.get_balance(auth_id="MA_XXXXXXXXXX", currency="INR")
print(f"Balance: {balance.available_balance} {balance.currency}")

# Get transaction history
txns = client.accounts.get_transactions(auth_id="MA_XXXXXXXXXX", limit=20, offset=0)

# Get current concurrent call usage
concurrency = client.accounts.get_concurrency(auth_id="MA_XXXXXXXXXX")
print(f"{concurrency.concurrent_calls} / {concurrency.max_concurrent} concurrent calls")
```

---

### Calls

```python
# Make an outbound call
resp = client.calls.create(
    from_="+911234567890",
    to_="+919876543210",
    answer_url="https://your-server.com/answer",
    answer_method="GET",
    hangup_url="https://your-server.com/hangup",
    hangup_method="GET",
)
call_uuid = resp.request_uuid

# List currently live calls
live = client.calls.list_live()

# List queued calls
queued = client.calls.list_queued()

# Transfer an active call to a new XML URL
client.calls.transfer(
    call_uuid,
    legs="aleg",
    aleg_url="https://your-server.com/transfer",
    aleg_method="GET",
)

# Send DTMF digits to an active call
client.calls.send_digits(call_uuid, digits="1", leg="aleg")

# Hang up a call
client.calls.hangup(call_uuid)
```

---

### Applications

Applications define the default XML URL for inbound calls to a number.

```python
# Create an application
app = client.applications.create(
    name="Customer Support",
    answer_url="https://your-server.com/answer",
    hangup_url="https://your-server.com/hangup",
    application_type="XML",   # "XML" or "Siptrunk"
)
app_id = app.app_id

# List all applications
apps = client.applications.list()

# Get a specific application
app = client.applications.get(app_id)

# Update an application
client.applications.update(app_id, name="Support Line", answer_url="https://new-url.com/answer")

# Delete an application
client.applications.delete(app_id)
```

---

### Phone Numbers

```python
# Browse available numbers in inventory
inventory = client.phone_numbers.list_inventory(country="IN", page=1, per_page=20)
for num in inventory.items:
    print(num['e164'], num['monthly_rate'])

# Purchase a number
client.phone_numbers.purchase_from_inventory(e164="+911234567890", currency="INR")

# Release a number back to inventory
client.phone_numbers.release(e164_number="+911234567890")

# Assign a number to a SIP trunk
client.phone_numbers.assign_to_trunk(e164_number="+911234567890", trunk_group_id="trunk-uuid")

# Unassign a number from its trunk
client.phone_numbers.unassign_from_trunk(e164_number="+911234567890")
```

---

### SIP Endpoints

SIP endpoints are devices or softphones that register with Vobiz via SIP.

```python
# Create an endpoint
ep = client.endpoints.create(
    username="agent_jane",
    password="SecurePass123!",
    alias="Jane - Support Desk",
)
endpoint_id = ep.endpoint_id
print(f"SIP URI: sip:{ep.username}@sip.vobiz.ai")

# List all endpoints
endpoints = client.endpoints.list()

# Get a specific endpoint (includes registration status)
ep = client.endpoints.get(endpoint_id)
print("Registered:", ep.sip_registered)

# Update an endpoint
client.endpoints.update(endpoint_id, alias="Jane - Sales")

# Delete an endpoint
client.endpoints.delete(endpoint_id)
```

**Connect your SIP client:**

| Setting | Value |
|---------|-------|
| SIP Server | `sip.vobiz.ai` |
| Port | `5060` (UDP/TCP) / `5061` (TLS) |
| Username | your endpoint username |
| Password | your endpoint password |

---

### SIP Trunks

```python
# List all SIP trunks
trunks = client.sip_trunks.list()
for trunk in trunks.objects:
    print(trunk.id, trunk.name)

# Get a specific trunk
trunk = client.sip_trunks.get("trunk-uuid")
print(trunk.cps_limit, trunk.concurrent_calls_limit)
```

---

### Credentials

SIP digest credentials for outbound trunk authentication.

```python
# List all credentials
creds = client.credentials.list()
for cred in creds.objects:
    print(cred.username)
```

---

### IP Access Control Lists

Whitelist IP addresses for inbound SIP traffic.

```python
# Create an IP ACL entry
acl = client.ip_access_control_lists.create(
    ip_address="203.0.113.10",
    description="Office static IP",
)
acl_id = acl.id

# List all ACL entries
acls = client.ip_access_control_lists.list()

# Delete an ACL entry
client.ip_access_control_lists.delete(acl_id)
```

---

### Origination URIs

Define where inbound SIP calls are sent.

```python
# List all origination URIs
uris = client.origination_uris.list()

# List origination URIs for a specific trunk
uris = client.origination_uris.list(trunk_id="trunk-uuid")
for uri in uris.objects:
    print(uri.uri, uri.priority)
```

---

### Recordings

```python
# List recordings (paginated)
recordings = client.recordings.list(limit=20, offset=0)
for rec in recordings.objects:
    print(rec.recording_id, rec.recording_url)

# Filter by recording type
trunk_recs = client.recordings.list(recording_type="trunk")

# Get a specific recording
rec = client.recordings.get("recording-uuid")
print("Duration:", rec.recording_duration_ms)
print("URL:", rec.recording_url)

# Delete a recording
client.recordings.delete("recording-uuid")
```

---

### CDRs (Call Detail Records)

```python
# List CDRs (most recent first)
cdrs = client.cdrs.list()

# Filter by date range and paginate
cdrs = client.cdrs.list(
    start_date="2026-01-01",
    end_date="2026-01-31",
    page=1,
    per_page=20,
)
for cdr in cdrs.data:
    print(cdr['call_id'], cdr['duration'], cdr['status'])
```

---

### Subaccounts

Isolate resources per customer, department, or environment.

```python
# Create a subaccount
result = client.subaccounts.create(
    name="Support Team",
    email="support@example.com",
    rate_limit=500,
    permissions={"calls": True, "cdr": True},
    password="SecurePass123!",
)
sub_id = result.sub_account.id
sub_auth_id = result.auth_credentials.auth_id
sub_auth_token = result.auth_credentials.auth_token
# ⚠️  Save the auth_token — it is only returned once at creation

# List all subaccounts
subs = client.subaccounts.list(page=1, size=25)

# Get a specific subaccount
sub = client.subaccounts.get(sub_id)

# Update a subaccount
client.subaccounts.update(sub_id, description="Updated team", rate_limit=750)

# Delete a subaccount
client.subaccounts.delete(sub_id)
```

---

## VobizXML — Call Flow Control

VobizXML is returned from your answer URL to tell Vobiz what to do with a call.

```python
from vobiz import vobizxml

response = vobizxml.ResponseElement()

# Speak text (TTS)
response.add_speak("Welcome to Acme Corp.", voice="WOMAN", language="en-US")

# Play an audio file
response.add_play("https://your-server.com/audio/hold-music.mp3")

# Collect DTMF digits (IVR menu)
get_digits = response.add_get_digits(
    action="https://your-server.com/menu",
    method="GET",
    num_digits=1,
    timeout=5,
)
get_digits.add_speak("Press 1 for sales. Press 2 for support.")

# Record the call
response.add_record(
    action="https://your-server.com/recording",
    max_length=300,
    play_beep=True,
)

# Dial / transfer to another number
dial = response.add_dial(timeout=30, caller_id="+911234567890")
dial.add_number("+919876543210")

# Wait / hold
response.add_wait(length=5)

# Redirect to another URL
response.add_redirect("https://your-server.com/next-step")

# Hang up
response.add_hangup()

# Render to string
xml_string = response.to_string(pretty=True)
print(xml_string)
```

**Example output:**

```xml
<Response>
  <Speak voice="WOMAN" language="en-US">Welcome to Acme Corp.</Speak>
  <Hangup/>
</Response>
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|----------|----------|-------------|
| `VOBIZ_AUTH_ID` | **Yes** | Your account Auth ID (e.g. `MA_XXXXXXXXXX`) |
| `VOBIZ_AUTH_TOKEN` | **Yes** | Your account Auth Token |
| `FROM_PHONE_NUMBER` | For call demos | Your Vobiz DID in E.164 format (e.g. `+911234567890`) |
| `TO_PHONE_NUMBER` | For call demos | Destination number in E.164 format |
| `ANSWER_URL` | For call demos | Public HTTPS URL for the answer webhook |

> **Security:** `.env` is in `.gitignore`. Never commit real credentials to git. Use `.env.example` as the template for your team.

---

## Running Tests

**End-to-end live API tests** (requires valid credentials in `.env`):

```bash
python testing.py
```

Expected output: `40 PASS, 1 SKIP` across 11 sections:
1. Account (get, balance, transactions, concurrency)
2. Calls (list live, list queued)
3. Applications (create, list, get, update, delete)
4. Phone Numbers (list inventory)
5. SIP Endpoints (create, list, get, update, delete)
6. SIP Trunks (list, get)
7. Credentials (list)
8. IP ACLs (create, list, delete)
9. Origination URIs (list)
10. Recordings (list)
11. CDRs (list)

**Unit tests:**

```bash
pip install pytest
pytest -q
```

---

## License

MIT — see [LICENSE.txt](LICENSE.txt)

---

## Support

- Documentation: [https://vobiz.ai/docs](https://vobiz.ai)
- Console: [https://console.vobiz.ai](https://console.vobiz.ai)
- Email: support@vobiz.ai
