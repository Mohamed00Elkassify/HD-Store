"""
ERPNext-backed data services for the web frontend.

Replaces the static data.py.  All product / stock / order data now
comes from the live ERPNext instance via integration.erp_client.
"""

import json
import logging
import re
from datetime import date, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import quote

from django.conf import settings
from django.core.cache import cache

from integration.erp_client import (
    ERPNextAuthError,
    ERPNextError,
    ERPNextUnavailable,
    get_erp_client,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Cache TTLs (seconds)
# ---------------------------------------------------------------------------
PRODUCTS_CACHE_TTL = getattr(settings, "CATALOG_CACHE_SECONDS", 300)
STOCK_CACHE_TTL = getattr(settings, "STOCK_CACHE_SECONDS", 30)

# ---------------------------------------------------------------------------
# Store constants (kept here so templates/checkout can reference them)
# ---------------------------------------------------------------------------
ASSIUT_CENTERS = [
    {"value": "assiut-city", "label": {"ar": "مدينة أسيوط", "en": "Assiut City"}},
    {"value": "dayrout", "label": {"ar": "ديروط", "en": "Dayrout"}},
    {"value": "el-qusya", "label": {"ar": "القوصية", "en": "El Qusya"}},
    {"value": "manfalut", "label": {"ar": "منفلوط", "en": "Manfalut"}},
    {"value": "abnub", "label": {"ar": "أبنوب", "en": "Abnub"}},
    {"value": "el-fateh", "label": {"ar": "الفتح", "en": "El Fateh"}},
    {"value": "sahel-selim", "label": {"ar": "ساحل سليم", "en": "Sahel Selim"}},
    {"value": "abou-tig", "label": {"ar": "أبو تيج", "en": "Abou Tig"}},
    {"value": "el-ghanayem", "label": {"ar": "الغنايم", "en": "El Ghanayem"}},
    {"value": "sedfa", "label": {"ar": "صدفا", "en": "Sedfa"}},
    {"value": "el-badari", "label": {"ar": "البداري", "en": "El Badari"}},
]

WHATSAPP_NUMBER = "201066537666"
WHATSAPP_DISPLAY = "01066537666"
STORE_PHONE = "01066537666"
WORKING_HOURS = "12:00 PM – 12:00 AM"


def get_whatsapp_link(message=""):
    base = f"https://wa.me/{WHATSAPP_NUMBER}"
    if message:
        return f"{base}?text={quote(message)}"
    return base


def format_price(price):
    try:
        return f"{int(price):,}"
    except (ValueError, TypeError):
        return str(price)


# ---------------------------------------------------------------------------
# ERPNext → template product mapping
# ---------------------------------------------------------------------------

def _image_url(path: str) -> str:
    """Turn an ERPNext relative image path into an absolute URL."""
    if not path:
        return ""
    if path.startswith(("http://", "https://")):
        return path
    base = settings.ERPNEXT_BASE_URL.rstrip("/")
    return f"{base}{path}"


def _map_erp_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map an ERPNext Item dict → the product dict format templates expect.

    Works with ANY ERPNext item — laptops, clothing, electronics, etc.
    Only relies on standard ERPNext fields.  If custom fields happen to
    exist they are picked up as bonuses.
    """
    item_code = item.get("item_code", "")
    item_name = item.get("item_name") or item_code
    description = item.get("description") or ""
    image_raw = item.get("image") or ""
    brand = item.get("brand") or ""
    item_group = item.get("item_group") or ""
    standard_rate = item.get("standard_rate") or 0

    # Custom fields (optional — picked up if they exist on the doctype)
    name_ar = item.get("custom_name_ar") or item_name
    old_price = item.get("custom_old_price") or None
    raw_tags = item.get("custom_tags") or ""
    tags = [t.strip() for t in raw_tags.split(",") if t.strip()] if raw_tags else []

    # Clean description for short display
    desc_clean = re.sub(r"<[^>]+>", "", description).strip()
    short_desc = [desc_clean[:120]] if desc_clean else []

    image = _image_url(image_raw)

    return {
        "id": item_code,
        "item_code": item_code,
        "slug": item_code,
        "name": {"en": item_name, "ar": name_ar},
        "brand": brand or item_group,
        "priceEGP": float(standard_rate),
        "oldPriceEGP": float(old_price) if old_price else None,
        "images": [image] if image else [],
        "image_url": image,
        "inStock": not item.get("disabled", False),
        "condition": item.get("custom_condition") or "",
        "grade": item.get("custom_grade") or "",
        "includesCharger": bool(item.get("custom_includes_charger", False)),
        "keyboardLayout": item.get("custom_keyboard_layout") or "",
        "shortSpecs": {"en": short_desc, "ar": short_desc},
        "specs": {},
        "tags": tags,
        "item_group": item_group,
        "description": description,
        "stock_uom": item.get("stock_uom") or "Nos",
    }


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------

# Only standard ERPNext Item fields — custom fields are fetched on detail
# pages via single-item GET which returns ALL fields automatically.
_LIST_ITEM_FIELDS = [
    "item_code",
    "item_name",
    "description",
    "image",
    "item_group",
    "brand",
    "standard_rate",
    "is_stock_item",
    "disabled",
    "stock_uom",
]


def get_all_products(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch ALL non-disabled items from ERPNext in one call, cache them.
    Every view that needs product data calls this.
    """
    cache_key = "web:all_products"
    if not force_refresh:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    try:
        client = get_erp_client()
        params = {
            "fields": json.dumps(_LIST_ITEM_FIELDS),
            "filters": json.dumps([["disabled", "=", 0]]),
            "limit_page_length": "500",
            "order_by": "modified desc",
        }
        data = client.request("GET", "/api/resource/Item", params=params)
        items = data.get("data", [])
        products = [_map_erp_item(i) for i in items]
        cache.set(cache_key, products, timeout=PRODUCTS_CACHE_TTL)
        return products
    except ERPNextError as exc:
        logger.error("ERPNext get_all_products failed: %s", exc)
        return []


def get_product_by_code(item_code: str) -> Optional[Dict[str, Any]]:
    """Return a single product dict, trying cache first then single-item fetch."""
    # Try the all-products cache
    for p in get_all_products():
        if p["item_code"] == item_code:
            return p

    # Fallback: fresh single fetch
    cache_key = f"web:product:{item_code}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        client = get_erp_client()
        data = client.request("GET", f"/api/resource/Item/{item_code}")
        item = data.get("data")
        if not item:
            return None
        product = _map_erp_item(item)
        cache.set(cache_key, product, timeout=PRODUCTS_CACHE_TTL)
        return product
    except ERPNextError as exc:
        logger.error("ERPNext get_product_by_code(%s) failed: %s", item_code, exc)
        return None


def get_product_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    """slug == item_code for ERPNext items."""
    return get_product_by_code(slug)


def get_products_by_tag(tag: str) -> List[Dict[str, Any]]:
    return [p for p in get_all_products() if tag in (p.get("tags") or [])]


# ---------------------------------------------------------------------------
# Stock
# ---------------------------------------------------------------------------

def fetch_stock_qty(item_code: str) -> float:
    cache_key = f"web:stock:{item_code}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    try:
        client = get_erp_client()
        params = {
            "fields": json.dumps(["actual_qty"]),
            "filters": json.dumps([["item_code", "=", item_code]]),
            "limit_page_length": "500",
        }
        data = client.request("GET", "/api/resource/Bin", params=params)
        bins = data.get("data", [])
        total = sum((b.get("actual_qty") or 0) for b in bins)
        cache.set(cache_key, max(total, 0), timeout=STOCK_CACHE_TTL)
        return max(total, 0)
    except ERPNextError as exc:
        logger.error("ERPNext stock for %s: %s", item_code, exc)
        return 0


# ---------------------------------------------------------------------------
# Filtering (in-Python, same logic as old data.py but on ERPNext data)
# ---------------------------------------------------------------------------

def filter_products(
    products: Optional[List[Dict]] = None,
    brand=None,
    ram=None,
    cpu=None,
    screen=None,
    grade=None,
    keyboard=None,
    in_stock=None,
    charger=None,
    gpu_type=None,
    q=None,
    sort_by="newest",
) -> List[Dict[str, Any]]:
    """Filter and sort the product list (works on cached ERPNext items)."""
    results = list(products if products is not None else get_all_products())

    if q:
        q_lower = q.lower()
        results = [
            p for p in results
            if q_lower in p["name"]["en"].lower()
            or q_lower in p["name"]["ar"].lower()
            or q_lower in p["brand"].lower()
            or q_lower in p.get("item_code", "").lower()
            or q_lower in p.get("description", "").lower()
            or q_lower in p.get("item_group", "").lower()
        ]

    if brand:
        brands_list = brand if isinstance(brand, list) else [brand]
        results = [p for p in results if p["brand"] in brands_list]

    if ram:
        rams = ram if isinstance(ram, list) else [ram]
        results = [
            p for p in results
            if p.get("specs", {}).get("ram", "").startswith(tuple(rams))
        ]

    if cpu:
        cpus = cpu if isinstance(cpu, list) else [cpu]
        results = [
            p for p in results
            if any(c.lower() in p.get("specs", {}).get("cpu", "").lower() for c in cpus)
        ]

    if screen:
        screens = screen if isinstance(screen, list) else [screen]
        results = [
            p for p in results
            if any(s in p.get("specs", {}).get("screen", "") for s in screens)
        ]

    if grade:
        grades = grade if isinstance(grade, list) else [grade]
        results = [p for p in results if p["grade"] in grades]

    if keyboard:
        kbs = keyboard if isinstance(keyboard, list) else [keyboard]
        results = [p for p in results if p["keyboardLayout"] in kbs]

    if in_stock:
        results = [p for p in results if p["inStock"]]

    if charger:
        results = [p for p in results if p["includesCharger"]]

    if gpu_type:
        gpu_field = lambda p: p.get("specs", {}).get("gpu", "")
        if gpu_type == "Dedicated":
            results = [
                p for p in results
                if "NVIDIA" in gpu_field(p) or "Radeon" in gpu_field(p)
            ]
        elif gpu_type == "Integrated":
            results = [
                p for p in results
                if "Intel" in gpu_field(p) and "NVIDIA" not in gpu_field(p)
            ]

    # Sort
    if sort_by == "price_asc":
        results.sort(key=lambda p: p["priceEGP"])
    elif sort_by == "price_desc":
        results.sort(key=lambda p: p["priceEGP"], reverse=True)
    # newest = default order (ERPNext returns modified desc)

    return results


# ---------------------------------------------------------------------------
# Dynamic filter options (derived from whatever items ERPNext returns)
# ---------------------------------------------------------------------------

def get_filter_options() -> Dict[str, list]:
    """
    Build filter-option lists from the actual products so the sidebar
    always reflects what's in ERPNext rather than hard-coded lists.
    """
    cache_key = "web:filter_options"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    products = get_all_products()

    brands = sorted({p["brand"] for p in products if p["brand"] and p["brand"] != "—"})
    grades = sorted({p["grade"] for p in products if p["grade"]})
    keyboards = sorted({p["keyboardLayout"] for p in products if p["keyboardLayout"]})

    # RAM / CPU / Screen — pull from specs (may be empty for non-laptop items)
    rams = sorted({
        p["specs"]["ram"]
        for p in products
        if p.get("specs", {}).get("ram") and p["specs"]["ram"] != "—"
    })
    cpus: set = set()
    for p in products:
        c = p.get("specs", {}).get("cpu", "")
        if not c or c == "—":
            continue
        for fam in ("i3", "i5", "i7", "i9", "Ryzen 3", "Ryzen 5", "Ryzen 7", "Ryzen 9"):
            if fam.lower() in c.lower():
                cpus.add(fam)
    screens = sorted({
        p["specs"]["screen"]
        for p in products
        if p.get("specs", {}).get("screen") and p["specs"]["screen"] != "—"
    })

    opts = {
        "brands": brands,
        "grades": grades,
        "rams": rams,
        "cpus": sorted(cpus),
        "screens": screens,
        "keyboards": keyboards,
    }
    cache.set(cache_key, opts, timeout=PRODUCTS_CACHE_TTL)
    return opts


# ---------------------------------------------------------------------------
# Sales Order creation (ERPNext)
# ---------------------------------------------------------------------------

def create_sales_order(
    *,
    customer_name: str,
    phone: str,
    center: str,
    address: str,
    landmark: str,
    notes: str,
    cart_items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Create a Sales Order in ERPNext.

    ``cart_items`` is the list returned by ``web.cart.get_cart_items(session)``
    Each entry: {"product": {...}, "quantity": int, "line_total": float}

    Returns the ERPNext response dict (contains ``data.name`` on success).
    """
    client = get_erp_client()
    default_customer = getattr(settings, "ERPNEXT_DEFAULT_CUSTOMER", "Online Customer")
    default_customer_group = getattr(settings, "ERPNEXT_DEFAULT_CUSTOMER_GROUP", "All Customer Groups")
    default_territory = getattr(settings, "ERPNEXT_DEFAULT_TERRITORY", "All Territories")
    default_wh = getattr(settings, "ERPNEXT_DEFAULT_WAREHOUSE", "") or ""
    delivery_date = (date.today() + timedelta(days=2)).isoformat()

    address_display = "\n".join([
        f"Address: {address}",
        f"Center: {center}",
        f"Landmark: {landmark}" if landmark else "",
    ]).strip()

    address_name = ""
    contact_name = ""

    def _find_customer_by_name(name: str) -> str:
        try:
            params = {
                "fields": json.dumps(["name", "customer_name"]),
                "filters": json.dumps([["customer_name", "=", name]]),
                "limit_page_length": "1",
            }
            data = client.request("GET", "/api/resource/Customer", params=params)
            results = data.get("data") or []
            if results:
                return results[0].get("name", "")
        except ERPNextError as exc:
            logger.warning("ERPNext customer lookup failed: %s", exc)
        return ""

    def _create_customer(name: str) -> str:
        payload = {
            "doctype": "Customer",
            "customer_name": name,
            "customer_type": "Individual",
            "customer_group": default_customer_group,
            "territory": default_territory,
        }
        resp = client.request("POST", "/api/resource/Customer", json={"data": payload})
        return (resp.get("data") or {}).get("name", "")

    # Prefer a real Customer for each checkout so ERPNext shows the actual name.
    customer_ref = _find_customer_by_name(customer_name)
    if not customer_ref:
        try:
            customer_ref = _create_customer(customer_name)
        except ERPNextError as exc:
            logger.warning("ERPNext customer create failed: %s", exc)
            customer_ref = default_customer

    # Create Address + Contact so ERPNext shows customer details on the Sales Order.
    try:
        addr_payload = {
            "doctype": "Address",
            "address_title": customer_name[:100],
            "address_type": "Shipping",
            "address_line1": address,
            "address_line2": landmark,
            "city": center,
            "country": "Egypt",
            "links": [{"link_doctype": "Customer", "link_name": customer_ref}],
        }
        addr_resp = client.request("POST", "/api/resource/Address", json={"data": addr_payload})
        address_name = (addr_resp.get("data") or {}).get("name", "")
    except ERPNextError as exc:
        logger.warning("ERPNext address create failed: %s", exc)

    try:
        contact_payload = {
            "doctype": "Contact",
            "first_name": customer_name,
            "mobile_no": phone,
            "phone": phone,
            "links": [{"link_doctype": "Customer", "link_name": customer_ref}],
        }
        contact_resp = client.request("POST", "/api/resource/Contact", json={"data": contact_payload})
        contact_name = (contact_resp.get("data") or {}).get("name", "")
    except ERPNextError as exc:
        logger.warning("ERPNext contact create failed: %s", exc)

    so_items = []
    for ci in cart_items:
        row: Dict[str, Any] = {
            "item_code": ci["product"]["item_code"],
            "qty": ci["quantity"],
        }
        if default_wh:
            row["warehouse"] = default_wh
        so_items.append(row)

    remarks_parts = [
        f"Customer: {customer_name}",
        f"Phone: {phone}",
        f"Center: {center}",
        f"Address: {address}",
    ]
    if landmark:
        remarks_parts.append(f"Landmark: {landmark}")
    if notes:
        remarks_parts.append(f"Notes: {notes}")

    import uuid
    unique_po = f"WEB-{uuid.uuid4().hex[:8].upper()}"

    payload: Dict[str, Any] = {
        "doctype": "Sales Order",
        "customer": customer_ref or default_customer,
        "customer_name": customer_name,
        "delivery_date": delivery_date,
        "items": so_items,
        "po_no": unique_po,
        "remarks": "\n".join(remarks_parts),
    }
    if address_display:
        payload["address_display"] = address_display
    if address_name:
        payload["customer_address"] = address_name
        payload["shipping_address_name"] = address_name
    if contact_name:
        payload["contact_person"] = contact_name
    if phone:
        payload["contact_phone"] = phone
        payload["contact_mobile"] = phone
    if default_wh:
        payload["set_warehouse"] = default_wh

    resp = client.request("POST", "/api/resource/Sales Order", json={"data": payload})
    return resp


# ---------------------------------------------------------------------------
# Order model persistence (local DB tracking)
# ---------------------------------------------------------------------------

def create_local_order(
    *,
    customer_name: str,
    phone: str,
    center: str,
    address: str,
    landmark: str,
    notes: str,
    cart_items: List[Dict[str, Any]],
    erp_so_name: str = "",
) -> "Order":
    """Create a local Order record for tracking alongside the ERPNext SO."""
    from orders.models import Order, OrderItem

    order = Order.objects.create(
        user=None,
        payment_method=Order.PaymentMethod.COD,
        payment_status=Order.PaymentStatus.UNPAID,
        customer_name=customer_name,
        phone=phone,
        address_line1=address,
        address_line2=landmark,
        city=center,
        notes=notes,
        status=Order.Status.SYNCED if erp_so_name else Order.Status.CREATED,
        erp_sales_order_name=erp_so_name,
    )

    for ci in cart_items:
        OrderItem.objects.create(
            order=order,
            item_code=ci["product"]["item_code"],
            qty=ci["quantity"],
            item_name=ci["product"]["name"].get("en", ""),
            image=ci["product"].get("image_url") or "",
        )

    return order
