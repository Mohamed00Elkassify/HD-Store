"""Custom template tags and filters for the web app."""
from django import template
from django.templatetags.static import static
from web.erp_services import format_price as _format_price

register = template.Library()


@register.filter
def price(value):
    """Format a number as price with commas."""
    try:
        return _format_price(int(value))
    except (ValueError, TypeError):
        return value


@register.filter
def loc(value, lang):
    """Get localized value from a dict like {'ar': '...', 'en': '...'}."""
    if isinstance(value, dict):
        return value.get(lang, value.get("en", ""))
    return value


@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary in templates."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, "")
    return ""


@register.filter
def multiply(value, arg):
    """Multiply two values."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def brand_logo(brand_name):
    """Return the static URL for a brand logo."""
    name = brand_name.lower() if brand_name else ""
    return static(f"web/images/brands/{name}.png")
