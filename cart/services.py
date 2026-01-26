from typing import Tuple
from catalog.services import get_stock


def get_available_qty(item_code: str) -> float:
    """
    Company decision: availability depends ONLY on ERPNext actual_qty totals.
    """
    stock = get_stock(item_code=item_code)
    actual = stock.get("total_actual_qty") or 0
    return max(actual, 0)

def validate_qty_available(item_code: str, requested_qty: int) -> Tuple[bool, float]:
    available = get_available_qty(item_code=item_code)
    return (requested_qty <= available), available
