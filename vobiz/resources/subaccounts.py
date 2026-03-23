from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class Subaccounts:
    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        # For Vobiz, we treat the RestClient auth_id as the account_id
        return self.client.auth_id

    def create(
        self,
        name: str,
        email: str,
        rate_limit: int,
        permissions: Any,
        password: str,
        phone: Optional[str] = None,
        description: Optional[str] = None,
        enabled: bool = True,
    ):
        """
        POST /api/v1/accounts/{account_id}/sub-accounts/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sub-accounts/"
        body: Dict[str, Any] = {
            "name": name,
            "email": email,
            "rate_limit": rate_limit,
            "permissions": permissions,
            "password": password,
            "enabled": enabled,
        }
        if phone is not None:
            body["phone"] = phone
        if description is not None:
            body["description"] = description

        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def list(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        active_only: Optional[bool] = None,
    ):
        """
        GET /api/v1/accounts/{account_id}/sub-accounts/
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sub-accounts/"
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if active_only is not None:
            params["active_only"] = active_only

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def get(self, sub_account_id: str):
        """
        GET /api/v1/accounts/{account_id}/sub-accounts/{sub_account_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sub-accounts/{sub_account_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, sub_account_id: str, **params: Any):
        """
        PUT /api/v1/accounts/{account_id}/sub-accounts/{sub_account_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sub-accounts/{sub_account_id}"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.put(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("PUT", resp)

    def delete(self, sub_account_id: str):
        """
        DELETE /api/v1/accounts/{account_id}/sub-accounts/{sub_account_id}
        """
        url = f"{VOBIZ_API_V1}/accounts/{self._account_id}/sub-accounts/{sub_account_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)

