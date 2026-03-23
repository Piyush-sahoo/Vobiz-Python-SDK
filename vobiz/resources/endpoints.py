from typing import Any, Dict, Optional


class Endpoints:
    """
    Vobiz Endpoints (SIP endpoints / devices) resource.

    Uses the `/v1/Account/{auth_id}/Endpoint/...` paths described in the
    Vobiz endpoint documentation.
    """

    def __init__(self, client):
        self.client = client

    def create(
        self,
        username: str,
        password: str,
        alias: Optional[str] = None,
        application: Optional[str] = None,
        **extra: Any,
    ):
        """
        POST /v1/Account/{auth_id}/Endpoint/

        Create a new SIP endpoint.
        """
        body: Dict[str, Any] = {
            "username": username,
            "password": password,
        }
        if alias is not None:
            body["alias"] = alias
        if application is not None:
            body["application"] = application
        body.update(extra)

        return self.client.request(
            "POST",
            ("Endpoint",),
            data=body,
        )

    def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **filters: Any,
    ):
        """
        GET /v1/Account/{auth_id}/Endpoint/

        Retrieve a paginated list of all SIP endpoints in the account.
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        params.update(filters)

        return self.client.request(
            "GET",
            ("Endpoint",),
            data=params,
        )

    def get(self, endpoint_id: str):
        """
        GET /v1/Account/{auth_id}/Endpoint/{endpoint_id}/

        Retrieve details for a specific endpoint.
        """
        return self.client.request(
            "GET",
            ("Endpoint", endpoint_id),
        )

    def update(self, endpoint_id: str, **params: Any):
        """
        POST /v1/Account/{auth_id}/Endpoint/{endpoint_id}/

        Update an endpoint's password, alias, application, or permissions.
        """
        body: Dict[str, Any] = dict(params)
        return self.client.request(
            "POST",
            ("Endpoint", endpoint_id),
            data=body,
        )

    def delete(self, endpoint_id: str):
        """
        DELETE /v1/Account/{auth_id}/Endpoint/{endpoint_id}/

        Delete an endpoint. On success, the API returns 204 No Content.
        """
        return self.client.request(
            "DELETE",
            ("Endpoint", endpoint_id),
        )
