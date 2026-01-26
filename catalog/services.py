from typing import Any, Dict, List, Optional
from django.conf import settings
from django.core.cache import cache
from integration.erp_client import get_erp_client


def _map_item_to_product(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map ERPNext Item fields -> API product fields.
    Keep it stable for frontend.
    """
    return {
        "item_code": item.get("item_code"),
        "name": item.get("item_name"),
        "description": item.get("description"),
        "image": item.get("image"),
        "item_group": item.get("item_group"),
        "is_stock_item": item.get("is_stock_item"),
        "disabled": item.get("disabled"),
    }


def list_products(limit: int = 20, offset: int = 0, q: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch products from ERPNext Item.
    Pagination:
      - limit_page_length = limit
      - limit_start = offset
    Search:
      - or_filters on item_name and item_code (LIKE)
    """
    q_norm = (q or "").strip()
    cache_key = f"catalog:products:limit={limit}:offset={offset}:q={q_norm.lower()}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    client = get_erp_client()

    params = {
        "fields": '["item_code","item_name","description","image","item_group","is_stock_item","disabled"]',
        "limit_page_length": str(limit),
        "limit_start": str(offset),
    }

    # ERPNext search using or_filters
    if q_norm:
        # LIKE search (contains)
        params["or_filters"] = (
            f'[["Item","item_name","like","%{q_norm}%"],'
            f'["Item","item_code","like","%{q_norm}%"]]'
        )

    data = client.request("GET", "/api/resource/Item", params=params)
    items = data.get("data", [])
    products = [_map_item_to_product(i) for i in items]

    cache.set(cache_key, products, timeout=settings.CATALOG_CACHE_SECONDS)
    return products


def get_product(item_code: str) -> Dict[str, Any]:
    cache_key = f"catalog:product:{item_code}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    client = get_erp_client()
    data = client.request("GET", f"/api/resource/Item/{item_code}")
    item = data.get("data", {})
    product = _map_item_to_product(item)

    cache.set(cache_key, product, timeout=settings.CATALOG_CACHE_SECONDS)
    return product


def get_stock(item_code: str) -> Dict[str, Any]:
    """
    Stock is per warehouse in ERPNext's Bin.
    We'll return totals + per warehouse breakdown.
    """
    cache_key = f"catalog:stock:{item_code}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    client = get_erp_client()
    params = {
        "fields": '["item_code","warehouse","actual_qty","projected_qty","reserved_qty"]',
        "filters": f'[["item_code","=","{item_code}"]]',
        "limit_page_length": "500",
    }
    data = client.request("GET", "/api/resource/Bin", params=params)
    bins = data.get("data", [])

    total_actual = sum((b.get("actual_qty") or 0) for b in bins)
    total_reserved = sum((b.get("reserved_qty") or 0) for b in bins)
    total_projected = sum((b.get("projected_qty") or 0) for b in bins)

    payload = {
        "item_code": item_code,
        "total_actual_qty": total_actual,
        "total_reserved_qty": total_reserved,
        "total_projected_qty": total_projected,
        "bins": bins,
        # company decision: available = actual only
        "available_qty": total_actual,
    }

    cache.set(cache_key, payload, timeout=settings.STOCK_CACHE_SECONDS)
    return payload
