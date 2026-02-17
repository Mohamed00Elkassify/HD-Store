"""Context processors for the web app."""
from .cart import get_cart_count
from .translations import get_translations
# Note: cart now uses erp_services internally for product lookups


def cart_context(request):
    """Add cart item count to all templates."""
    return {
        "cart_count": get_cart_count(request.session),
    }


def translations_context(request):
    """Add translations and locale info to all templates."""
    lang = getattr(request, "LANGUAGE_CODE", "en")
    if lang not in ("en", "ar"):
        lang = "en"
    return {
        "t": get_translations(lang),
        "lang": lang,
        "is_rtl": lang == "ar",
        "dir": "rtl" if lang == "ar" else "ltr",
        "other_lang": "ar" if lang == "en" else "en",
        "other_lang_label": "العربية" if lang == "en" else "English",
    }
