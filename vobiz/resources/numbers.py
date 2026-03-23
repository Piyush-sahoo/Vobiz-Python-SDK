from typing import Any, Dict, Optional

VOBIZ_API_V1 = "https://api.vobiz.ai/api/v1"


class PhoneNumbers:
    """
    Vobiz Phone Numbers resource.

    Implements inventory listing, purchase from inventory, and release,
    as defined in the Vobiz phone number endpoints.
    """

    def __init__(self, client):
        self.client = client

    @property
    def _account_id(self) -> str:
        # For Vobiz, we treat the RestClient auth_id as the account_id
        return self.client.auth_id

    def list(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        include_subaccounts: Optional[bool] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/account/{auth_id}/numbers

        List all phone numbers purchased and assigned to this account.
        include_subaccounts: if True, also returns numbers from sub-accounts (master accounts only).
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/numbers"
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if include_subaccounts is not None:
            params["include_subaccounts"] = include_subaccounts
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def list_inventory(        self,
        country: Optional[str] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        **filters: Any,
    ):
        """
        GET /api/v1/account/{auth_id}/inventory/numbers

        Browse available phone numbers in inventory that are not assigned
        to any account (auth_id IS NULL, status='active').
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/inventory/numbers"
        params: Dict[str, Any] = {}
        if country is not None:
            params["country"] = country
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        params.update(filters)

        resp = self.client.session.get(
            url, params=params, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("GET", resp)

    def purchase_from_inventory(
        self,
        e164: str,
        currency: Optional[str] = None,
        **extra: Any,
    ):
        """
        POST /api/v1/account/{auth_id}/numbers/purchase-from-inventory

        Purchase a phone number from inventory and assign it to the account.
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/numbers/purchase-from-inventory"
        body: Dict[str, Any] = {"e164": e164}
        if currency is not None:
            body["currency"] = currency
        body.update(extra)

        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def release(self, e164_number: str):
        """
        DELETE /api/v1/account/{auth_id}/numbers/{e164_number}

        Release a phone number from the account back to inventory.
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/numbers/{e164_number}"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)

    def assign_to_trunk(self, e164_number: str, trunk_group_id: str):
        """
        POST /api/v1/account/{account_id}/numbers/{PHONE_NUMBER}/assign

        Assign a phone number to a SIP trunk.
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/numbers/{e164_number}/assign"
        body: Dict[str, Any] = {"trunk_group_id": trunk_group_id}
        resp = self.client.session.post(
            url, json=body, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("POST", resp)

    def unassign_from_trunk(self, e164_number: str):
        """
        DELETE /api/v1/account/{account_id}/numbers/{PHONE_NUMBER}/assign

        Unassign a phone number from its SIP trunk.
        """
        url = f"{VOBIZ_API_V1}/account/{self._account_id}/numbers/{e164_number}/assign"
        resp = self.client.session.delete(
            url, timeout=self.client.timeout, proxies=self.client.proxies
        )
        return self.client.process_response("DELETE", resp)
