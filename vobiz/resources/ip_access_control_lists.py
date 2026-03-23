from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class IpAccessControlLists:
    """
    Vobiz IP Access Control Lists resource.

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
        ip_address: str,
        description: Optional[str] = None,
        enabled: Optional[bool] = None,
        **extra: Any,
    ):
        """
        POST /api/v1/account/{account_id}/ip-acl

        Create a new IP ACL entry.
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/ip-acl"
        body: Dict[str, Any] = {"ip_address": ip_address}
        if description is not None:
            body["description"] = description
        if enabled is not None:
            body["enabled"] = enabled
        body.update(extra)

        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/account/{account_id}/trunks/ip-acl

        Retrieve a paginated list of all IP ACL entries.
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/trunks/ip-acl"
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def get(self, acl_id: str):
        """
        GET /api/v1/account/{account_id}/ip-acl/{ip_acl_id}
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/ip-acl/{acl_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, acl_id: str, **params: Any):
        """
        PUT /api/v1/account/{account_id}/ip-acl/{ip_acl_id}
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/ip-acl/{acl_id}"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.put(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("PUT", resp)

    def delete(self, acl_id: str):
        """
        DELETE /api/v1/account/{account_id}/ip-acl/{ip_acl_id}
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/ip-acl/{acl_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)

