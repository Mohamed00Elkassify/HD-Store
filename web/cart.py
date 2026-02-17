"""
Session-based shopping cart — no login required.
Cart data is stored in ``request.session["cart"]``.

Product look-ups now use ERPNext (via erp_services) instead of the
hard-coded PRODUCTS list.  The session stores ``item_code`` (the ERPNext
item identifier) rather than a numeric ``product_id``.
"""


def _get_cart(session):
    """Get cart items list from session.

    Also migrates any legacy entries that used ``product_id`` to ``item_code``.
    """
    if "cart" not in session:
        session["cart"] = []
    cart = session["cart"]
    migrated = False
    for entry in cart:
        if "item_code" not in entry and "product_id" in entry:
            entry["item_code"] = str(entry.pop("product_id"))
            migrated = True
    if migrated:
        session.modified = True
    return cart


def get_cart_items(session):
    """Return list of cart items with product data from ERPNext."""
    from .erp_services import get_all_products

    cart = _get_cart(session)
    if not cart:
        return []

    # Build a lookup from the cached products list
    products = get_all_products()
    product_map = {p["item_code"]: p for p in products}

    items = []
    for entry in cart:
        product = product_map.get(entry["item_code"])
        if product:
            items.append({
                "product": product,
                "quantity": entry["quantity"],
                "line_total": product["priceEGP"] * entry["quantity"],
            })
    return items


def get_cart_total(session):
    items = get_cart_items(session)
    return sum(item["line_total"] for item in items)


def get_cart_count(session):
    cart = _get_cart(session)
    return sum(entry["quantity"] for entry in cart)


def add_to_cart(session, item_code, quantity=1):
    """Add product to cart or increase quantity.

    ``item_code`` is the ERPNext Item Code string.
    """
    cart = _get_cart(session)
    for entry in cart:
        if entry["item_code"] == item_code:
            entry["quantity"] += quantity
            session.modified = True
            return
    cart.append({"item_code": item_code, "quantity": quantity})
    session.modified = True


def update_cart_quantity(session, item_code, quantity):
    """Set quantity for a cart item."""
    cart = _get_cart(session)
    for entry in cart:
        if entry["item_code"] == item_code:
            if quantity <= 0:
                cart.remove(entry)
            else:
                entry["quantity"] = quantity
            session.modified = True
            return


def remove_from_cart(session, item_code):
    """Remove a product from the cart."""
    cart = _get_cart(session)
    cart[:] = [e for e in cart if e["item_code"] != item_code]
    session.modified = True


def clear_cart(session):
    """Empty the cart."""
    session["cart"] = []
    session.modified = True
