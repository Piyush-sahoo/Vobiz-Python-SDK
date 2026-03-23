from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class CDRs:
    """
    Vobiz Call Detail Records (CDRs) resource.

    Endpoint: https://api.vobiz.ai/api/v1/account/{account_id}/cdr
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        return self.client.auth_id

    def list(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/account/{account_id}/cdr
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/cdr"
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)
