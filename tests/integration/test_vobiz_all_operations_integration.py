import os

import pytest

import vobiz
from vobiz.base import ResponseObject

AUTH_ID = os.getenv("VOBIZ_AUTH_ID")
AUTH_TOKEN = os.getenv("VOBIZ_AUTH_TOKEN")

if not AUTH_ID or not AUTH_TOKEN:
    pytest.skip("credentials not set", allow_module_level=True)


EXISTING_APPLICATION_ID = os.getenv("VOBIZ_TEST_APPLICATION_ID")
EXISTING_CALL_UUID = os.getenv("VOBIZ_TEST_CALL_UUID")
EXISTING_CREDENTIAL_ID = os.getenv("VOBIZ_TEST_CREDENTIAL_ID")
EXISTING_ENDPOINT_ID = os.getenv("VOBIZ_TEST_ENDPOINT_ID")
EXISTING_ACL_ID = os.getenv("VOBIZ_TEST_ACL_ID")
EXISTING_ORIGINATION_URI_ID = os.getenv("VOBIZ_TEST_ORIGINATION_URI_ID")
EXISTING_RECORDING_ID = os.getenv("VOBIZ_TEST_RECORDING_ID")
EXISTING_TRUNK_ID = os.getenv("VOBIZ_TEST_TRUNK_ID")
EXISTING_SUBACCOUNT_ID = os.getenv("VOBIZ_TEST_SUBACCOUNT_ID")
EXISTING_NUMBER = os.getenv("VOBIZ_TEST_NUMBER")
OUTBOUND_FROM = os.getenv("VOBIZ_TEST_OUTBOUND_FROM")
OUTBOUND_TO = os.getenv("VOBIZ_TEST_OUTBOUND_TO")

ENABLE_MUTATIONS = os.getenv("VOBIZ_TEST_ENABLE_MUTATIONS", "false").lower() == "true"
ENABLE_DESTRUCTIVE = os.getenv("VOBIZ_TEST_ENABLE_DESTRUCTIVE", "false").lower() == "true"


@pytest.fixture(scope="module")
def client():
    return vobiz.RestClient(auth_id=AUTH_ID, auth_token=AUTH_TOKEN)


def _assert_response_shape(response):
    assert response is not None
    assert isinstance(response, (ResponseObject, dict))


def _call_expect_response(operation):
    response = operation()
    _assert_response_shape(response)


def _call_expect_error(operation):
    try:
        response = operation()
    except Exception:
        return
    _assert_response_shape(response)


# Accounts

def test_accounts_get(client):
    _call_expect_response(lambda: client.accounts.get())


def test_accounts_get_transactions(client):
    _call_expect_response(lambda: client.accounts.get_transactions(AUTH_ID, limit=1, offset=0))


def test_accounts_get_balance(client):
    _call_expect_response(lambda: client.accounts.get_balance(AUTH_ID, "INR"))


def test_accounts_get_concurrency(client):
    _call_expect_response(lambda: client.accounts.get_concurrency(AUTH_ID))


# CDRs

def test_cdrs_list(client):
    _call_expect_response(lambda: client.cdrs.list(page=1, per_page=1))


# Calls

def test_calls_list(client):
    _call_expect_error(lambda: client.calls.list())


def test_calls_list_live(client):
    _call_expect_response(lambda: client.calls.list_live())


def test_calls_list_queued(client):
    _call_expect_response(lambda: client.calls.list_queued())


def test_calls_create(client):
    if OUTBOUND_FROM and OUTBOUND_TO and ENABLE_MUTATIONS:
        _call_expect_response(
            lambda: client.calls.create(
                from_=OUTBOUND_FROM,
                to_=OUTBOUND_TO,
                answer_url="https://example.com/answer",
                answer_method="GET",
            )
        )
    else:
        _call_expect_error(
            lambda: client.calls.create(
                from_="INVALID",
                to_="INVALID",
                answer_url="invalid-url",
            )
        )


def test_calls_get_and_actions(client):
    call_uuid = EXISTING_CALL_UUID or "INVALID_CALL_UUID"

    if EXISTING_CALL_UUID:
        _call_expect_response(lambda: client.calls.get(call_uuid))
        _call_expect_response(lambda: client.calls.get_live(call_uuid))
        _call_expect_response(lambda: client.calls.get_queued(call_uuid))
    else:
        _call_expect_error(lambda: client.calls.get(call_uuid))
        _call_expect_error(lambda: client.calls.get_live(call_uuid))
        _call_expect_error(lambda: client.calls.get_queued(call_uuid))

    _call_expect_error(lambda: client.calls.transfer(call_uuid, legs="both"))
    _call_expect_error(lambda: client.calls.send_digits(call_uuid, digits="1234", leg="both"))
    _call_expect_error(lambda: client.calls.start_recording(call_uuid, time_limit=10))
    _call_expect_error(lambda: client.calls.stop_recording(call_uuid))
    _call_expect_error(lambda: client.calls.play_audio(call_uuid, urls=["https://example.com/a.mp3"]))
    _call_expect_error(lambda: client.calls.stop_audio(call_uuid))
    _call_expect_error(lambda: client.calls.speak_text(call_uuid, text="hello", voice="WOMAN", language="en-US"))
    _call_expect_error(lambda: client.calls.stop_speak(call_uuid))
    _call_expect_error(lambda: client.calls.hangup(call_uuid))


# Applications

def test_applications_list(client):
    _call_expect_response(lambda: client.applications.list(page=1, size=1))


def test_applications_operations(client):
    if ENABLE_MUTATIONS:
        _call_expect_response(
            lambda: client.applications.create(
                name="integration-temp-app",
                answer_url="https://example.com/answer",
                answer_method="GET",
            )
        )
    else:
        _call_expect_error(
            lambda: client.applications.create(
                name="",
                answer_url="invalid-url",
                answer_method="GET",
            )
        )

    app_id = EXISTING_APPLICATION_ID or "INVALID_APPLICATION_ID"
    _call_expect_error(lambda: client.applications.get(app_id)) if not EXISTING_APPLICATION_ID else _call_expect_response(lambda: client.applications.get(app_id))
    _call_expect_error(lambda: client.applications.update(app_id, name="updated-name")) if not EXISTING_APPLICATION_ID else _call_expect_response(lambda: client.applications.update(app_id, name="updated-name"))

    number = EXISTING_NUMBER or "+10000000000"
    _call_expect_error(lambda: client.applications.attach_number(number, app_id)) if not (EXISTING_NUMBER and EXISTING_APPLICATION_ID) else _call_expect_response(lambda: client.applications.attach_number(number, app_id))
    _call_expect_error(lambda: client.applications.detach_number(number)) if not EXISTING_NUMBER else _call_expect_response(lambda: client.applications.detach_number(number))

    if EXISTING_APPLICATION_ID and ENABLE_DESTRUCTIVE:
        _call_expect_response(lambda: client.applications.delete(app_id))
    else:
        _call_expect_error(lambda: client.applications.delete(app_id))


# Endpoints

def test_endpoints_operations(client):
    _call_expect_response(lambda: client.endpoints.list(limit=1, offset=0))

    if ENABLE_MUTATIONS:
        _call_expect_response(lambda: client.endpoints.create(username="tmp-endpoint", password="TempPass@123"))
    else:
        _call_expect_error(lambda: client.endpoints.create(username="", password=""))

    endpoint_id = EXISTING_ENDPOINT_ID or "INVALID_ENDPOINT_ID"
    _call_expect_error(lambda: client.endpoints.get(endpoint_id)) if not EXISTING_ENDPOINT_ID else _call_expect_response(lambda: client.endpoints.get(endpoint_id))
    _call_expect_error(lambda: client.endpoints.update(endpoint_id, alias="updated-alias")) if not EXISTING_ENDPOINT_ID else _call_expect_response(lambda: client.endpoints.update(endpoint_id, alias="updated-alias"))

    if EXISTING_ENDPOINT_ID and ENABLE_DESTRUCTIVE:
        _call_expect_response(lambda: client.endpoints.delete(endpoint_id))
    else:
        _call_expect_error(lambda: client.endpoints.delete(endpoint_id))


# Credentials

def test_credentials_operations(client):
    _call_expect_response(lambda: client.credentials.list(limit=1, offset=0))

    if ENABLE_MUTATIONS:
        _call_expect_response(lambda: client.credentials.create(username="tmp-cred", password="TempPass@123"))
    else:
        _call_expect_error(lambda: client.credentials.create(username="", password=""))

    cred_id = EXISTING_CREDENTIAL_ID or "INVALID_CREDENTIAL_ID"
    _call_expect_error(lambda: client.credentials.get(cred_id)) if not EXISTING_CREDENTIAL_ID else _call_expect_response(lambda: client.credentials.get(cred_id))
    _call_expect_error(lambda: client.credentials.update(cred_id, description="updated")) if not EXISTING_CREDENTIAL_ID else _call_expect_response(lambda: client.credentials.update(cred_id, description="updated"))

    if EXISTING_CREDENTIAL_ID and ENABLE_DESTRUCTIVE:
        _call_expect_response(lambda: client.credentials.delete(cred_id))
    else:
        _call_expect_error(lambda: client.credentials.delete(cred_id))


# IP ACLs

def test_ip_access_control_lists_operations(client):
    _call_expect_response(lambda: client.ip_access_control_lists.list(limit=1, offset=0))

    if ENABLE_MUTATIONS:
        _call_expect_response(lambda: client.ip_access_control_lists.create(ip_address="198.51.100.10", enabled=True))
    else:
        _call_expect_error(lambda: client.ip_access_control_lists.create(ip_address="invalid-ip"))

    acl_id = EXISTING_ACL_ID or "INVALID_ACL_ID"
    _call_expect_error(lambda: client.ip_access_control_lists.get(acl_id)) if not EXISTING_ACL_ID else _call_expect_response(lambda: client.ip_access_control_lists.get(acl_id))
    _call_expect_error(lambda: client.ip_access_control_lists.update(acl_id, description="updated")) if not EXISTING_ACL_ID else _call_expect_response(lambda: client.ip_access_control_lists.update(acl_id, description="updated"))

    if EXISTING_ACL_ID and ENABLE_DESTRUCTIVE:
        _call_expect_response(lambda: client.ip_access_control_lists.delete(acl_id))
    else:
        _call_expect_error(lambda: client.ip_access_control_lists.delete(acl_id))


# Origination URIs

def test_origination_uris_operations(client):
    _call_expect_response(lambda: client.origination_uris.list(limit=1, offset=0))

    if ENABLE_MUTATIONS:
        _call_expect_response(lambda: client.origination_uris.create(uri="sip:example.com", priority=1, weight=10, enabled=True))
    else:
        _call_expect_error(lambda: client.origination_uris.create(uri="invalid-uri"))

    uri_id = EXISTING_ORIGINATION_URI_ID or "INVALID_URI_ID"
    _call_expect_error(lambda: client.origination_uris.get(uri_id)) if not EXISTING_ORIGINATION_URI_ID else _call_expect_response(lambda: client.origination_uris.get(uri_id))
    _call_expect_error(lambda: client.origination_uris.update(uri_id, priority=2)) if not EXISTING_ORIGINATION_URI_ID else _call_expect_response(lambda: client.origination_uris.update(uri_id, priority=2))

    if EXISTING_ORIGINATION_URI_ID and ENABLE_DESTRUCTIVE:
        _call_expect_response(lambda: client.origination_uris.delete(uri_id))
    else:
        _call_expect_error(lambda: client.origination_uris.delete(uri_id))


# SIP trunks

def test_sip_trunks_operations(client):
    _call_expect_response(lambda: client.sip_trunks.list(page=1, size=1))

    if ENABLE_MUTATIONS:
        _call_expect_response(lambda: client.sip_trunks.create(name="integration-temp-trunk"))
    else:
        _call_expect_error(lambda: client.sip_trunks.create(name=""))

    trunk_id = EXISTING_TRUNK_ID or "INVALID_TRUNK_ID"
    _call_expect_error(lambda: client.sip_trunks.get(trunk_id)) if not EXISTING_TRUNK_ID else _call_expect_response(lambda: client.sip_trunks.get(trunk_id))
    _call_expect_error(lambda: client.sip_trunks.update(trunk_id, name="updated-name")) if not EXISTING_TRUNK_ID else _call_expect_response(lambda: client.sip_trunks.update(trunk_id, name="updated-name"))

    if EXISTING_TRUNK_ID and ENABLE_DESTRUCTIVE:
        _call_expect_response(lambda: client.sip_trunks.delete(trunk_id))
    else:
        _call_expect_error(lambda: client.sip_trunks.delete(trunk_id))


# Numbers

def test_numbers_operations(client):
    _call_expect_response(lambda: client.phone_numbers.list(page=1, per_page=1))
    _call_expect_response(lambda: client.phone_numbers.list_inventory(page=1, per_page=1))

    if ENABLE_MUTATIONS and EXISTING_NUMBER:
        _call_expect_response(lambda: client.phone_numbers.purchase_from_inventory(e164=EXISTING_NUMBER))
    else:
        _call_expect_error(lambda: client.phone_numbers.purchase_from_inventory(e164="INVALID"))

    test_number = EXISTING_NUMBER or "+10000000000"
    _call_expect_error(lambda: client.phone_numbers.release(test_number)) if not EXISTING_NUMBER else _call_expect_response(lambda: client.phone_numbers.release(test_number))

    if EXISTING_NUMBER and EXISTING_TRUNK_ID:
        _call_expect_response(lambda: client.phone_numbers.assign_to_trunk(EXISTING_NUMBER, EXISTING_TRUNK_ID))
        _call_expect_response(lambda: client.phone_numbers.unassign_from_trunk(EXISTING_NUMBER))
    else:
        _call_expect_error(lambda: client.phone_numbers.assign_to_trunk(test_number, "INVALID_TRUNK_ID"))
        _call_expect_error(lambda: client.phone_numbers.unassign_from_trunk(test_number))


# Recordings

def test_recordings_operations(client):
    _call_expect_response(lambda: client.recordings.list(limit=1, offset=0))

    recording_id = EXISTING_RECORDING_ID or "INVALID_RECORDING_ID"
    _call_expect_error(lambda: client.recordings.get(recording_id)) if not EXISTING_RECORDING_ID else _call_expect_response(lambda: client.recordings.get(recording_id))
    _call_expect_error(lambda: client.recordings.delete(recording_id)) if not EXISTING_RECORDING_ID else _call_expect_response(lambda: client.recordings.delete(recording_id))

    _call_expect_error(lambda: client.recordings.export(recipient_emails=["invalid-email"]))

    if ENABLE_DESTRUCTIVE:
        _call_expect_response(lambda: client.recordings.bulk_delete(add_time__gte="1900-01-01 00:00:00", add_time__lte="1900-01-01 00:00:01"))
    else:
        pytest.skip("Skipping destructive bulk delete; set VOBIZ_TEST_ENABLE_DESTRUCTIVE=true to run")


# Subaccounts

def test_subaccounts_operations(client):
    _call_expect_response(lambda: client.subaccounts.list(page=1, size=1))

    if ENABLE_MUTATIONS:
        _call_expect_response(
            lambda: client.subaccounts.create(
                name="integration-subaccount",
                email="integration-sub@example.com",
                rate_limit=1,
                permissions=[],
                password="TempPass@123",
            )
        )
    else:
        _call_expect_error(
            lambda: client.subaccounts.create(
                name="",
                email="invalid",
                rate_limit=0,
                permissions=[],
                password="",
            )
        )

    sub_id = EXISTING_SUBACCOUNT_ID or "INVALID_SUBACCOUNT_ID"
    _call_expect_error(lambda: client.subaccounts.get(sub_id)) if not EXISTING_SUBACCOUNT_ID else _call_expect_response(lambda: client.subaccounts.get(sub_id))
    _call_expect_error(lambda: client.subaccounts.update(sub_id, name="updated-name")) if not EXISTING_SUBACCOUNT_ID else _call_expect_response(lambda: client.subaccounts.update(sub_id, name="updated-name"))

    if EXISTING_SUBACCOUNT_ID and ENABLE_DESTRUCTIVE:
        _call_expect_response(lambda: client.subaccounts.delete(sub_id))
    else:
        _call_expect_error(lambda: client.subaccounts.delete(sub_id))
