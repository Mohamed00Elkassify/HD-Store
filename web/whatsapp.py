import base64
import logging
import re
import time
import threading
from typing import Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

WASENDER_API_URL = "https://wasenderapi.com/api/send-message"
WASENDER_UPLOAD_URL = "https://wasenderapi.com/api/upload"


def _normalize_phone(raw: str) -> Optional[str]:
    digits = re.sub(r"\D+", "", raw or "")
    if not digits:
        return None
    # Egypt local numbers like 01XXXXXXXXX -> +20XXXXXXXXXX
    if digits.startswith("0") and settings.WHATSAPP_DEFAULT_COUNTRY_CODE:
        digits = digits[1:]
        return f"{settings.WHATSAPP_DEFAULT_COUNTRY_CODE}{digits}"
    if digits.startswith("+"):
        return digits
    if settings.WHATSAPP_DEFAULT_COUNTRY_CODE and not digits.startswith("+"):
        return f"{settings.WHATSAPP_DEFAULT_COUNTRY_CODE}{digits}"
    return digits


def _send_wasender(phone: str, message: str) -> None:
    """Send WhatsApp message via WasenderAPI."""
    api_key = getattr(settings, "WASENDER_API_KEY", None)
    if not api_key:
        logger.warning("WhatsApp automation skipped: WASENDER_API_KEY not configured")
        return

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                WASENDER_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "to": phone.lstrip("+"),  # WasenderAPI expects number without +
                    "text": message,
                },
                timeout=30,
            )
            if response.status_code == 429 and attempt < max_retries - 1:
                wait = int(response.headers.get("Retry-After", 2 ** (attempt + 1)))
                logger.info("WasenderAPI rate-limited, retrying in %ds...", wait)
                time.sleep(wait)
                continue
            response.raise_for_status()
            logger.info("WhatsApp message sent successfully to %s", phone)
            return
        except requests.RequestException as exc:
            if attempt < max_retries - 1 and "429" in str(exc):
                time.sleep(2 ** (attempt + 1))
                continue
            logger.warning("WhatsApp automation failed: %s", exc)
            return


def send_welcome_message(*, message: str, phone: str) -> None:
    if not settings.WHATSAPP_AUTOMATION_ENABLED:
        return

    normalized = _normalize_phone(phone)
    if not normalized:
        logger.warning("WhatsApp automation skipped: invalid phone")
        return

    # Run in a background thread so it doesn't block the request.
    thread = threading.Thread(
        target=_send_wasender,
        args=(normalized, message),
        daemon=True,
    )
    thread.start()


# ---------------------------------------------------------------------------
# Upload media & send document helpers (for Sales Invoice PDF)
# ---------------------------------------------------------------------------

def _upload_to_wasender(pdf_bytes: bytes, filename: str) -> Optional[str]:
    """Upload a PDF to WasenderAPI and return the temporary public URL.

    WasenderAPI hosts the file for 24 hours, which is enough for WhatsApp
    to download it when we send the document message.
    """
    api_key = getattr(settings, "WASENDER_API_KEY", None)
    if not api_key:
        logger.warning("WhatsApp upload skipped: WASENDER_API_KEY not configured")
        return None

    b64_data = base64.b64encode(pdf_bytes).decode()
    data_url = f"data:application/pdf;base64,{b64_data}"

    try:
        response = requests.post(
            WASENDER_UPLOAD_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"base64": data_url},
            timeout=60,
        )
        response.raise_for_status()
        result = response.json()
        public_url = result.get("publicUrl") or (result.get("data") or {}).get("publicUrl")
        if public_url:
            logger.info("PDF uploaded to WasenderAPI: %s", public_url)
        else:
            logger.warning("WasenderAPI upload succeeded but no publicUrl in response: %s", result)
        return public_url
    except requests.RequestException as exc:
        logger.warning("WasenderAPI PDF upload failed: %s", exc)
        return None


def _send_document_wasender(phone: str, document_url: str, filename: str, caption: str) -> None:
    """Send a document message via WasenderAPI."""
    api_key = getattr(settings, "WASENDER_API_KEY", None)
    if not api_key:
        logger.warning("WhatsApp document send skipped: WASENDER_API_KEY not configured")
        return

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                WASENDER_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "to": phone.lstrip("+"),
                    "documentUrl": document_url,
                    "fileName": filename,
                    "text": caption,
                },
                timeout=30,
            )
            if response.status_code == 429 and attempt < max_retries - 1:
                wait = int(response.headers.get("Retry-After", 2 ** (attempt + 1)))
                logger.info("WasenderAPI rate-limited, retrying in %ds...", wait)
                time.sleep(wait)
                continue
            response.raise_for_status()
            logger.info("WhatsApp document sent successfully to %s", phone)
            return
        except requests.RequestException as exc:
            if attempt < max_retries - 1 and "429" in str(exc):
                time.sleep(2 ** (attempt + 1))
                continue
            logger.warning("WhatsApp document send failed: %s", exc)
            return


def _send_sales_order_pdf_task(phone: str, so_name: str) -> None:
    """Background task: fetch PDF from ERPNext → upload to WasenderAPI → send."""
    from integration.erp_client import get_erp_client, ERPNextError

    try:
        client = get_erp_client()
        pdf_bytes = client.download_pdf(doctype="Sales Order", name=so_name)
    except ERPNextError as exc:
        logger.warning("Failed to download Sales Order PDF (%s): %s", so_name, exc)
        return

    filename = f"{so_name}.pdf"

    public_url = _upload_to_wasender(pdf_bytes, filename)
    if not public_url:
        return

    caption = f"Thank you for your order! Please find your Sales Order ({so_name}) attached."
    _send_document_wasender(phone, public_url, filename, caption)


def send_sales_order_pdf(*, phone: str, so_name: str) -> None:
    """Send the Sales Order PDF to the customer via WhatsApp.

    Called after a successful checkout + ERP sync. Runs in a background
    thread so the HTTP response is not delayed.
    """
    if not settings.WHATSAPP_AUTOMATION_ENABLED:
        return

    normalized = _normalize_phone(phone)
    if not normalized:
        logger.warning("WhatsApp PDF skipped: invalid phone %s", phone)
        return

    thread = threading.Thread(
        target=_send_sales_order_pdf_task,
        args=(normalized, so_name),
        daemon=True,
    )
    thread.start()


# ---------------------------------------------------------------------------
# Sales Invoice PDF (sent when invoice is submitted in ERPNext)
# ---------------------------------------------------------------------------

def _send_sales_invoice_pdf_task(phone: str, invoice_name: str) -> None:
    """Background task: fetch Sales Invoice data → generate PDF locally → upload → send."""
    from integration.erp_client import get_erp_client, ERPNextError
    from integration.pdf_generator import generate_sales_invoice_pdf

    try:
        client = get_erp_client()

        # Try ERPNext native PDF first; fall back to local generation
        try:
            pdf_bytes = client.download_pdf(doctype="Sales Invoice", name=invoice_name)
            logger.info("Downloaded Sales Invoice PDF from ERPNext (%s)", invoice_name)
        except ERPNextError:
            logger.info(
                "ERPNext PDF download failed for %s, generating locally", invoice_name
            )
            inv_resp = client.request("GET", f"/api/resource/Sales Invoice/{invoice_name}")
            inv_data = inv_resp.get("data") or inv_resp
            pdf_bytes = generate_sales_invoice_pdf(inv_data)

    except ERPNextError as exc:
        logger.warning("Failed to get Sales Invoice data (%s): %s", invoice_name, exc)
        return
    except Exception as exc:
        logger.exception("Unexpected error generating PDF for %s: %s", invoice_name, exc)
        return

    filename = f"{invoice_name}.pdf"

    public_url = _upload_to_wasender(pdf_bytes, filename)
    if not public_url:
        return

    caption = f"Thank you for your purchase! Please find your invoice ({invoice_name}) attached."
    _send_document_wasender(phone, public_url, filename, caption)


def send_sales_invoice_pdf(*, phone: str, invoice_name: str) -> None:
    """Send the Sales Invoice PDF to the customer via WhatsApp.

    Called from the ERPNext webhook when a Sales Invoice is submitted.
    Runs in a background thread so the webhook response is not delayed.
    """
    if not settings.WHATSAPP_AUTOMATION_ENABLED:
        logger.info("WhatsApp automation disabled, skipping invoice PDF for %s", invoice_name)
        return

    normalized = _normalize_phone(phone)
    if not normalized:
        logger.warning("WhatsApp Invoice PDF skipped: invalid phone %s", phone)
        return

    thread = threading.Thread(
        target=_send_sales_invoice_pdf_task,
        args=(normalized, invoice_name),
        daemon=True,
    )
    thread.start()
