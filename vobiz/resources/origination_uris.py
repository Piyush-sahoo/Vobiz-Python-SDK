from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class OriginationUris:
    """
    Vobiz Origination URIs resource.

    Implements create, list, update, and delete operations using the
    `/api/v1/account/{account_id}/origination-uris` and
    `/api/v1/account/{account_id}/trunks/origination-uris` endpoints.
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        # For Vobiz, we treat the RestClient auth_id as the account_id
        return self.client.auth_id

    def create(
        self,
        uri: str,
        priority: Optional[int] = None,
        weight: Optional[int] = None,
        enabled: Optional[bool] = None,
        **extra: Any,
    ):
        """
        POST /api/v1/account/{account_id}/origination-uris

        Create a new origination URI for outbound routing.
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/origination-uris"
        body: Dict[str, Any] = {"uri": uri}
        if priority is not None:
            body["priority"] = priority
        if weight is not None:
            body["weight"] = weight
        if enabled is not None:
            body["enabled"] = enabled
        body.update(extra)

        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def list(
        self,
        trunk_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/account/{account_id}/trunks/origination-uris

        Retrieve a paginated list of origination URIs.
        Optionally filter by trunk_id.
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/trunks/origination-uris"
        params: Dict[str, Any] = {}
        if trunk_id is not None:
            params["trunk_id"] = trunk_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def get(self, uri_id: str):
        """
        GET /api/v1/account/{account_id}/origination-uris/{uri_id}
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/origination-uris/{uri_id}"
        resp = self.client.session.get(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def update(self, uri_id: str, **params: Any):
        """
        PUT /api/v1/account/{account_id}/origination-uris/{uri_id}
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/origination-uris/{uri_id}"
        body: Dict[str, Any] = dict(params)
        resp = self.client.session.put(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("PUT", resp)

    def delete(self, uri_id: str):
        """
        DELETE /api/v1/account/{account_id}/origination-uris/{uri_id}
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/origination-uris/{uri_id}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)

