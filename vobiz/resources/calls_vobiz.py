from typing import Any, Dict, Optional


class Calls:
    """
    Vobiz Calls resource.

    Uses the `/api/v1/account/{auth_id}/call/` endpoints for call control and
    live/queued status listing, plus DTMF.
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        return self.client.auth_id

    def create(self, from_: str, to_: str, answer_url: str, **params: Any):
        """
        POST /api/v1/Account/{auth_id}/Call/
        """
        body: Dict[str, Any] = {
            "from": from_,
            "to": to_,
            "answer_url": answer_url,
        }
        body.update(params)
        return self.client.request("POST", ("Call",), data=body)

    def transfer(self, call_uuid: str, **params: Any):
        """
        POST /api/v1/Account/{auth_id}/Call/{call_uuid}/
        """
        return self.client.request("POST", ("Call", call_uuid), data=dict(params))

    def hangup(self, call_uuid: str):
        """
        DELETE /api/v1/Account/{auth_id}/Call/{call_uuid}/
        """
        return self.client.request("DELETE", ("Call", call_uuid))

    def list(self, status: Optional[str] = None, **filters: Any):
        """
        GET /api/v1/Account/{auth_id}/Call/
        """
        params: Dict[str, Any] = dict(filters)
        if status is not None:
            params["status"] = status
        return self.client.request(
            "GET",
            ("Call",),
            data=params,
        )

    def get(self, call_uuid: str, status: Optional[str] = None):
        """
        GET /api/v1/Account/{auth_id}/Call/{call_uuid}/
        """
        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        return self.client.request("GET", ("Call", call_uuid), data=params)

    def list_live(self):
        return self.list(status="live")

    def list_queued(self):
        return self.list(status="queued")

    def get_live(self, call_uuid: str):
        return self.get(call_uuid, status="live")

    def get_queued(self, call_uuid: str):
        return self.get(call_uuid, status="queued")

    def send_digits(self, call_uuid: str, digits: str, leg: str):
        """
        POST /api/v1/Account/{auth_id}/Call/{call_uuid}/DTMF/
        """
        body: Dict[str, Any] = {"digits": digits, "leg": leg}
        return self.client.request("POST", ("Call", call_uuid, "DTMF"), data=body)

    # ── Recording ──────────────────────────────────────────────────────────────

    def start_recording(
        self,
        call_uuid: str,
        time_limit: Optional[int] = None,
        file_format: Optional[str] = None,
        callback_url: Optional[str] = None,
        callback_method: Optional[str] = None,
        **params: Any,
    ):
        """
        POST /api/v1/Account/{auth_id}/Call/{call_uuid}/Record/

        Start recording an active call.
        """
        body: Dict[str, Any] = {}
        if time_limit is not None:
            body["time_limit"] = time_limit
        if file_format is not None:
            body["file_format"] = file_format
        if callback_url is not None:
            body["callback_url"] = callback_url
        if callback_method is not None:
            body["callback_method"] = callback_method
        body.update(params)
        return self.client.request("POST", ("Call", call_uuid, "Record"), data=body)

    def stop_recording(self, call_uuid: str, url: Optional[str] = None):
        """
        DELETE /api/v1/Account/{auth_id}/Call/{call_uuid}/Record/

        Stop recording on an active call.
        If url is provided, stops only that specific recording.
        If omitted, stops all recordings on the call.
        """
        body: Dict[str, Any] = {}
        if url is not None:
            body["URL"] = url
        return self.client.request("DELETE", ("Call", call_uuid, "Record"), data=body)

    # ── Play Audio ─────────────────────────────────────────────────────────────

    def play_audio(
        self,
        call_uuid: str,
        urls: list,
        length: Optional[int] = None,
        legs: Optional[str] = None,
        loop: Optional[bool] = None,
        mix: Optional[bool] = None,
        **params: Any,
    ):
        """
        POST /api/v1/Account/{auth_id}/Call/{call_uuid}/Play/

        Play one or more audio files during an active call.
        urls: list of HTTPS URLs to audio files (mp3/wav).
        legs: "aleg", "bleg", or "both" (default "aleg").
        """
        body: Dict[str, Any] = {"urls": urls}
        if length is not None:
            body["length"] = length
        if legs is not None:
            body["legs"] = legs
        if loop is not None:
            body["loop"] = loop
        if mix is not None:
            body["mix"] = mix
        body.update(params)
        return self.client.request("POST", ("Call", call_uuid, "Play"), data=body)

    def stop_audio(self, call_uuid: str):
        """
        DELETE /api/v1/Account/{auth_id}/Call/{call_uuid}/Play/

        Stop audio playback on an active call.
        """
        return self.client.request("DELETE", ("Call", call_uuid, "Play"), data={})

    # ── Speak Text (TTS) ───────────────────────────────────────────────────────

    def speak_text(
        self,
        call_uuid: str,
        text: str,
        voice: Optional[str] = None,
        language: Optional[str] = None,
        legs: Optional[str] = None,
        loop: Optional[bool] = None,
        mix: Optional[bool] = None,
        **params: Any,
    ):
        """
        POST /api/v1/Account/{auth_id}/Call/{call_uuid}/Speak/

        Convert text to speech and play it during an active call.
        voice: "WOMAN" or "MAN" (default "WOMAN").
        language: BCP-47 language code, e.g. "en-US" (default).
        legs: "aleg", "bleg", or "both".
        """
        body: Dict[str, Any] = {"text": text}
        if voice is not None:
            body["voice"] = voice
        if language is not None:
            body["language"] = language
        if legs is not None:
            body["legs"] = legs
        if loop is not None:
            body["loop"] = loop
        if mix is not None:
            body["mix"] = mix
        body.update(params)
        return self.client.request("POST", ("Call", call_uuid, "Speak"), data=body)

    def stop_speak(self, call_uuid: str):
        """
        DELETE /api/v1/Account/{auth_id}/Call/{call_uuid}/Speak/

        Stop text-to-speech currently playing on an active call.
        """
        return self.client.request("DELETE", ("Call", call_uuid, "Speak"), data={})

