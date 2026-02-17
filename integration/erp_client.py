import time
import requests
from dataclasses import dataclass
from typing import Any, Dict, Optional, List

from django.conf import settings


class ERPNextError(Exception):
    pass


class ERPNextAuthError(ERPNextError):
    pass


class ERPNextUnavailable(ERPNextError):
    pass


@dataclass
class ERPNextClient:
    base_url: str
    api_key: str
    api_secret: str
    timeout: int = 15
    max_retries: int = 2
    backoff_seconds: float = 0.6

    def _headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"token {self.api_key}:{self.api_secret}",
        }

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"

        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                r = requests.request(
                    method=method,
                    url=url,
                    headers=self._headers(),
                    params=params,
                    json=json,
                    timeout=self.timeout,
                )

                if r.status_code in (401, 403):
                    raise ERPNextAuthError(f"{r.status_code} auth error: {r.text}")

                if r.status_code == 404:
                    raise ERPNextError(f"Endpoint not found: {url}")

                if r.status_code >= 400:
                    raise ERPNextError(f"{r.status_code} ERPNext error: {r.text}")

                return r.json()

            except (requests.Timeout, requests.ConnectionError) as e:
                last_exc = e
                if attempt < self.max_retries:
                    time.sleep(self.backoff_seconds * (attempt + 1))
                    continue
                raise ERPNextUnavailable(f"ERPNext unavailable: {e}") from e

        raise ERPNextError(f"Unexpected ERPNext error: {last_exc}")

    def download_pdf(
        self,
        doctype: str,
        name: str,
        print_format: str = "Standard",
    ) -> bytes:
        """Download print-format PDF from ERPNext.

        Returns raw PDF bytes.
        """
        url = (
            f"{self.base_url}/api/method/"
            f"frappe.utils.print_format.download_pdf"
        )
        params = {
            "doctype": doctype,
            "name": name,
            "format": print_format,
            "no_letterhead": "1",
        }

        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                r = requests.get(
                    url,
                    headers=self._headers(),
                    params=params,
                    timeout=self.timeout,
                )

                if r.status_code in (401, 403):
                    raise ERPNextAuthError(f"{r.status_code} auth error: {r.text}")

                if r.status_code == 404:
                    raise ERPNextError(f"PDF not found for {doctype}/{name}")

                if r.status_code >= 400:
                    raise ERPNextError(f"{r.status_code} ERPNext PDF error: {r.text}")

                return r.content

            except (requests.Timeout, requests.ConnectionError) as e:
                last_exc = e
                if attempt < self.max_retries:
                    time.sleep(self.backoff_seconds * (attempt + 1))
                    continue
                raise ERPNextUnavailable(f"ERPNext unavailable: {e}") from e

        raise ERPNextError(f"Unexpected ERPNext PDF error: {last_exc}")


def get_erp_client() -> ERPNextClient:
    if not settings.ERPNEXT_API_KEY or not settings.ERPNEXT_API_SECRET:
        raise ERPNextAuthError("Missing ERPNEXT_API_KEY/ERPNEXT_API_SECRET in .env")

    return ERPNextClient(
        base_url=settings.ERPNEXT_BASE_URL,
        api_key=settings.ERPNEXT_API_KEY,
        api_secret=settings.ERPNEXT_API_SECRET,
        timeout=settings.ERPNEXT_TIMEOUT_SECONDS,
    )
