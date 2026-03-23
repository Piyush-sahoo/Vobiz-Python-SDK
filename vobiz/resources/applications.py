from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class Applications:
    """
    Vobiz Applications resource.

    All endpoints are scoped to the authenticated account.
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        # For Vobiz, we treat the RestClient auth_id as the account_id
        return self.client.auth_id

    def create(
        self,
        name: str,
        answer_url: str,
        answer_method: str = "POST",
        hangup_url: Optional[str] = None,
        hangup_method: str = "POST",
        fallback_answer_url: Optional[str] = None,
        fallback_method: str = "POST",
        application_type: Optional[str] = None,
        **extra: Any,
    ):
        """
        POST /api/v1/Account/{account_id}/Application/
        """
        url = f"{VOBIZ_API_V1}/Account/{self._account_id}/Application/"
        body: Dict[str, Any] = {
            "name": name,
            "answer_url": answer_url,
            "answer_method": answer_method,
            "hangup_method": hangup_method,
        }
        if hangup_url is not None:
            body["hangup_url"] = hangup_url
        if fallback_answer_url is not None:
            body["fallback_answer_url"] = fallback_answer_url
        if fallback_method is not None:
            body["fallback_method"] = fallback_method
        if application_type is not None:
            body["application_type"] = application_type
        # allow forward-compatible extra keys
        body.update(extra)

        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def list(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        application_type: Optional[str] = None,
    ):
        """
        GET /api/v1/Account/{account_id}/Application/
        """
        url = f"{VOBIZ_API_V1}/Account/{self._account_id}/Application/"
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if application_type is not None:
            params["application_type"] = application_type

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def get(self, application_id: str):
        """
        GET /api/v1/Account/{account_id}/Application/{application_id}
        """
        url = f"{VOBIZ_API_V1}/Account/{self._account_id}/Application/{application_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, application_id: str, **params: Any):
        """
        POST /api/v1/Account/{account_id}/Application/{application_id}/
        """
        url = f"{VOBIZ_API_V1}/Account/{self._account_id}/Application/{application_id}/"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def delete(self, application_id: str):
        """
        DELETE /api/v1/Account/{account_id}/Application/{application_id}
        """
        url = f"{VOBIZ_API_V1}/Account/{self._account_id}/Application/{application_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)

    def attach_number(self, number: str, application_id: str):
        """
        POST /api/v1/account/{account_id}/numbers/{number}/application

        Attach a phone number to a voice application.
        number: E.164 format, e.g. "+911234567890"
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/numbers/{number}/application"
        body = {"application_id": application_id}
        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def detach_number(self, number: str):
        """
        DELETE /api/v1/account/{account_id}/numbers/{number}/application

        Detach a phone number from its voice application.
        number: E.164 format, e.g. "+911234567890"
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/numbers/{number}/application"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)
