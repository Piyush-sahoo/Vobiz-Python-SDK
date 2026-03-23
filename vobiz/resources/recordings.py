from typing import Any, Dict, Optional


class Recordings:
    """
    Vobiz Recordings resource.

    Endpoint: https://api.vobiz.ai/api/v1/Account/{auth_id}/Recording/
    """

    def __init__(self, client):
        self.client = client

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        call_uuid: Optional[str] = None,
        recording_type: Optional[str] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/Account/{auth_id}/Recording/
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if call_uuid is not None:
            params["call_uuid"] = call_uuid
        if recording_type is not None:
            params["recording_type"] = recording_type
        params.update(filters)

        return self.client.request("GET", ("Recording",), data=params)

    def get(self, recording_id: str):
        """
        GET /api/v1/Account/{auth_id}/Recording/{recording_id}/
        """
        return self.client.request("GET", ("Recording", recording_id))

    def delete(self, recording_id: str):
        """
        DELETE /api/v1/Account/{auth_id}/Recording/{recording_id}/
        """
        return self.client.request("DELETE", ("Recording", recording_id))

    def export(self, recipient_emails: list, **filters: Any):
        """
        POST /api/v1/Account/{auth_id}/export/recording/

        Async export — recordings matching filters are packaged and emailed.
        recipient_emails: list of email addresses to receive the download link.

        Date range filters (use one or the other, not both):
          from_date / to_date  — e.g. "2025-01-01 00:00:00"
          recording_storage_duration — exact days old
          recording_storage_duration__gte / __lte — range of days old

        Optional additional filters (only for ranges <= 30 days):
          from_number, to_number, conference_name, recording_format ("mp3"/"wav")
        """
        VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"
        url = f"{VOBIZ_API_V1}/Account/{self.client.auth_id}/export/recording/"
        body: Dict[str, Any] = {
            "recipient": {"customer_account": recipient_emails}
        }
        body.update(filters)
        resp = self.client.session.post(
            url, json=body,
            timeout=self.client.timeout,
            proxies=self.client.proxies,
        )
        return self.client.process_response("POST", resp)

    def bulk_delete(self, **filters: Any):
        """
        DELETE /api/v1/Account/{auth_id}/Recording/BulkDelete/

        Async bulk delete — permanently removes all recordings matching filters.
        At least one filter is recommended to avoid deleting everything.

        Filter params (as query string kwargs):
          add_time__gte / add_time__lte  — "YYYY-MM-DD HH:MM:SS"
          conference_name, recording_format, from_number, to_number
        """
        return self.client.request(
            "DELETE", ("Recording", "BulkDelete"), data=filters
        )
