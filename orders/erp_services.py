from typing import Dict, Any, List
from django.conf import settings
from integration.erp_client import get_erp_client


def create_erp_sales_order(
    *,
    customer: str,
    delivery_date: str,
    items: List[Dict[str, Any]],
    order_notes: str = "",
) -> Dict[str, Any]:
    client = get_erp_client()
    default_wh = getattr(settings, "ERPNEXT_DEFAULT_WAREHOUSE", "") or ""
    # Put warehouse on each item (safest) + set_warehouse on header (convenient)
    items_with_wh = []
    for it in items:
        row = dict(it)
        if default_wh and "warehouse" not in row:
            row["warehouse"] = default_wh
        items_with_wh.append(row)

    payload = {
        "doctype": "Sales Order",
        "customer": customer,
        "delivery_date": delivery_date,
        "items": items_with_wh,
        "po_no": "Online",  # Customer's Purchase Order - marks this as an online order
    }
    if default_wh:
        payload["set_warehouse"] = default_wh
    if order_notes:
        payload["remarks"] = order_notes

    return client.request("POST", "/api/resource/Sales Order", json={"data": payload})
