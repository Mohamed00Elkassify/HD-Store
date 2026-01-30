from .models import Order


ALLOWED_TRANSITIONS = {
    Order.Status.CREATED: {Order.Status.SYNCED, Order.Status.CANCELLED},
    Order.Status.SYNCED: {Order.Status.PROCESSING, Order.Status.CANCELLED},
    Order.Status.PROCESSING: {Order.Status.SHIPPED, Order.Status.CANCELLED},
    Order.Status.SHIPPED: {Order.Status.DELIVERED},
    Order.Status.DELIVERED: set(),
    Order.Status.CANCELLED: set(),
}

def can_transition(old: str, new: str) -> bool:
    return new in ALLOWED_TRANSITIONS.get(old, set()) # type: ignore