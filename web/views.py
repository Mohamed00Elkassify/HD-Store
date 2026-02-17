"""Views for the web (Django templates) frontend.

All product data now comes from ERPNext via ``web.erp_services``.
Checkout creates a real Sales Order in ERPNext + a local Order record.
Payment: **Cash on Delivery only**.
"""

import json
import logging
from urllib.parse import quote

from allauth.account.views import LoginView, SignupView
from django.contrib.auth import logout as auth_logout
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .cart import (
    add_to_cart,
    clear_cart,
    get_cart_count,
    get_cart_items,
    get_cart_total,
    remove_from_cart,
    update_cart_quantity,
)
from .erp_services import (
    ASSIUT_CENTERS,
    STORE_PHONE,
    WHATSAPP_DISPLAY,
    WHATSAPP_NUMBER,
    WORKING_HOURS,
    create_local_order,
    create_sales_order,
    filter_products,
    format_price,
    get_all_products,
    get_filter_options,
    get_product_by_slug,
    get_products_by_tag,
    get_whatsapp_link,
)
from .forms import CheckoutForm
from .translations import get_translations
from .whatsapp import send_welcome_message

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _base_context(request, lang):
    """Build context variables available on every page."""
    t = get_translations(lang)
    all_products = get_all_products()

    # Lightweight list for header search autosuggest
    search_data = [
        {
            "name": p["name"][lang] if lang in p["name"] else p["name"]["en"],
            "slug": p["slug"],
            "brand": p["brand"],
            "item_group": p.get("item_group", ""),
        }
        for p in all_products
    ]
    return {
        "lang": lang,
        "is_rtl": lang == "ar",
        "dir": "rtl" if lang == "ar" else "ltr",
        "dir_start": "right" if lang == "ar" else "left",
        "dir_end": "left" if lang == "ar" else "right",
        "other_lang": "ar" if lang == "en" else "en",
        "other_lang_label": "العربية" if lang == "en" else "English",
        "t": t,
        "search_products_json": json.dumps(search_data, ensure_ascii=False),
        "whatsapp_link": get_whatsapp_link(),
        "whatsapp_display": WHATSAPP_DISPLAY,
        "working_hours": WORKING_HOURS,
        "store_phone": STORE_PHONE,
        "products_url": reverse("web:products", kwargs={"lang": lang}),
    }


def _set_lang(request, lang):
    """Store language on request for context processors."""
    request.LANGUAGE_CODE = lang


def _redirect_login(request, lang):
    next_url = quote(request.get_full_path())
    return redirect(f"{reverse('web:login', kwargs={'lang': lang})}?next={next_url}")


# ---------------------------------------------------------------------------
# Root redirect
# ---------------------------------------------------------------------------


def root_redirect(request):
    """Redirect / to /en/."""
    return redirect("web:home", lang="en")


# ---------------------------------------------------------------------------
# Auth (web)
# ---------------------------------------------------------------------------


def login_view(request, lang="en"):
    _set_lang(request, lang)
    view = LoginView.as_view(template_name="web/auth/login.html")
    return view(request)


def register_view(request, lang="en"):
    _set_lang(request, lang)
    view = SignupView.as_view(template_name="web/auth/register.html")
    return view(request)


def logout_view(request, lang="en"):
    _set_lang(request, lang)
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("web:home", lang=lang)


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------


def home_view(request, lang="en"):
    _set_lang(request, lang)
    t = get_translations(lang)

    categories_data = [
        {
            "key": "laptops",
            "icon": "laptop",
            "iconColor": "text-blue-500",
            "title": str(t.home.catLaptops),
            "desc": str(t.home.catLaptopsDesc),
            "url": reverse("web:products", kwargs={"lang": lang}),
        },
        {
            "key": "workstations",
            "icon": "monitor",
            "iconColor": "text-purple-500",
            "title": str(t.home.catWorkstations),
            "desc": str(t.home.catWorkstationsDesc),
            "url": reverse("web:products", kwargs={"lang": lang}) + "?cpu=i7&cpu=Ryzen+7",
        },
        {
            "key": "gaming",
            "icon": "gamepad-2",
            "iconColor": "text-red-500",
            "title": str(t.home.catGaming),
            "desc": str(t.home.catGamingDesc),
            "url": reverse("web:products", kwargs={"lang": lang}) + "?gpu_type=Dedicated",
        },
        {
            "key": "business",
            "icon": "briefcase",
            "iconColor": "text-emerald-500",
            "title": str(t.home.catBusiness),
            "desc": str(t.home.catBusinessDesc),
            "url": reverse("web:products", kwargs={"lang": lang}),
        },
        {
            "key": "budget",
            "icon": "dollar-sign",
            "iconColor": "text-amber-500",
            "title": str(t.home.catBudget),
            "desc": str(t.home.catBudgetDesc),
            "url": reverse("web:products", kwargs={"lang": lang}) + "?sort=price_asc",
        },
        {
            "key": "accessories",
            "icon": "cable",
            "iconColor": "text-cyan-500",
            "title": str(t.home.catAccessories),
            "desc": str(t.home.catAccessoriesDesc),
            "url": reverse("web:products", kwargs={"lang": lang}),
        },
    ]

    why_us = [
        {"icon": "shield-check", "title": t.home.whyInspected, "desc": t.home.whyInspectedDesc},
        {"icon": "truck", "title": t.home.whyDelivery, "desc": t.home.whyDeliveryDesc},
        {"icon": "badge-check", "title": t.home.whyWarranty, "desc": t.home.whyWarrantyDesc},
        {"icon": "banknote", "title": t.home.whyCod, "desc": t.home.whyCodDesc},
    ]

    all_products = get_all_products()
    hot_deals = get_products_by_tag("Hot Deal")[:6]
    best_sellers = get_products_by_tag("Best Seller")[:6]

    # If no tags exist in ERPNext items, show newest products instead
    if not hot_deals:
        hot_deals = all_products[:6]
    if not best_sellers:
        best_sellers = all_products[:6]

    # Dynamic brand links
    filter_opts = get_filter_options()
    
    # Mapping of brand names to their logo images
    brand_logos = {
        "Dell": "web/images/brands/dell.png",
        "HP": "web/images/brands/hp.png",
        "Lenovo": "web/images/brands/lenovo.png",
    }
    
    brands = [
        {
            "name": b,
            "url": reverse("web:products", kwargs={"lang": lang}) + f"?brand={b}",
            "initial": b[0].upper(),
            "logo": brand_logos.get(b, ""),
        }
        for b in filter_opts.get("brands", [])[:6]
    ]

    ctx = _base_context(request, lang)
    ctx.update({
        "categories_data": categories_data,
        "why_us": why_us,
        "hot_deals": hot_deals,
        "best_sellers": best_sellers,
        "brands": brands,
    })
    return render(request, "web/home.html", ctx)


# ---------------------------------------------------------------------------
# Products listing
# ---------------------------------------------------------------------------

PER_PAGE = 12


def products_view(request, lang="en"):
    _set_lang(request, lang)

    # Collect filter params
    active_brands = request.GET.getlist("brand")
    active_grades = request.GET.getlist("grade")
    active_rams = request.GET.getlist("ram")
    active_cpus = request.GET.getlist("cpu")
    active_screens = request.GET.getlist("screen")
    active_keyboards = request.GET.getlist("keyboard")
    active_in_stock = request.GET.get("in_stock") == "1"
    active_charger = request.GET.get("charger") == "1"
    active_gpu_type = request.GET.get("gpu_type", "")
    active_sort = request.GET.get("sort", "newest")
    search_q = request.GET.get("q", "").strip()
    page = int(request.GET.get("page", "1"))

    all_filtered = filter_products(
        brand=active_brands or None,
        ram=active_rams or None,
        cpu=active_cpus or None,
        screen=active_screens or None,
        grade=active_grades or None,
        keyboard=active_keyboards or None,
        in_stock=active_in_stock or None,
        charger=active_charger or None,
        gpu_type=active_gpu_type or None,
        q=search_q or None,
        sort_by=active_sort,
    )

    total_count = len(all_filtered)
    products = all_filtered[: page * PER_PAGE]
    has_more = len(products) < total_count

    # Build next page params
    next_page_params = request.GET.copy()
    next_page_params["page"] = str(page + 1)
    next_page_qs = next_page_params.urlencode()

    has_active_filters = bool(
        active_brands or active_grades or active_rams or active_cpus
        or active_screens or active_keyboards or active_in_stock
        or active_charger or active_gpu_type or search_q
    )

    # Dynamic filter options from ERPNext data
    filter_opts = get_filter_options()

    ctx = _base_context(request, lang)
    ctx.update({
        "products": products,
        "total_count": total_count,
        "has_more": has_more,
        "next_page_params": next_page_qs,
        # Filter option lists (dynamic from ERPNext)
        "filter_brands": filter_opts.get("brands", []),
        "filter_grades": filter_opts.get("grades", []),
        "filter_rams": filter_opts.get("rams", []),
        "filter_cpus": filter_opts.get("cpus", []),
        "filter_screens": filter_opts.get("screens", []),
        "filter_keyboards": filter_opts.get("keyboards", []),
        # Active selections
        "active_brands": active_brands,
        "active_grades": active_grades,
        "active_rams": active_rams,
        "active_cpus": active_cpus,
        "active_screens": active_screens,
        "active_keyboards": active_keyboards,
        "active_in_stock": active_in_stock,
        "active_charger": active_charger,
        "active_gpu_type": active_gpu_type,
        "active_sort": active_sort,
        "search_q": search_q,
        "has_active_filters": has_active_filters,
    })
    return render(request, "web/products/list.html", ctx)


# ---------------------------------------------------------------------------
# Product detail
# ---------------------------------------------------------------------------


def product_detail_view(request, lang="en", slug=""):
    _set_lang(request, lang)
    product = get_product_by_slug(slug)
    if not product:
        raise Http404("Product not found")

    t = get_translations(lang)

    # Only show spec labels for specs that actually exist on this product
    all_spec_labels = {
        "cpu": str(t.product.cpu),
        "ram": str(t.product.ram),
        "storage": str(t.product.storage),
        "gpu": str(t.product.gpu),
        "screen": str(t.product.screen),
        "battery": str(t.product.battery),
        "warranty": str(t.product.warranty),
    }
    spec_labels = {
        k: v for k, v in all_spec_labels.items()
        if product.get("specs", {}).get(k) and product["specs"][k] not in ("", "—")
    }

    # Related products: same brand, exclude self, max 4
    all_products = get_all_products()
    related = [
        p for p in all_products
        if p["brand"] == product["brand"] and p["item_code"] != product["item_code"]
    ][:4]

    ctx = _base_context(request, lang)
    ctx.update({
        "product": product,
        "spec_labels": spec_labels,
        "related_products": related,
    })
    return render(request, "web/products/detail.html", ctx)


# ---------------------------------------------------------------------------
# Cart views
# ---------------------------------------------------------------------------


def cart_view(request, lang="en"):
    _set_lang(request, lang)
    ctx = _base_context(request, lang)
    ctx.update({
        "cart_items": get_cart_items(request.session),
        "cart_total": get_cart_total(request.session),
    })
    return render(request, "web/cart.html", ctx)


@require_POST
def cart_add_view(request, lang="en"):
    item_code = request.POST.get("item_code", "")
    quantity = int(request.POST.get("quantity", "1"))
    add_to_cart(request.session, item_code, quantity)
    # If "buy_now" flag is set, go straight to checkout
    if request.POST.get("buy_now"):
        return redirect("web:checkout", lang=lang)
    next_url = request.POST.get("next", "")
    if next_url:
        return redirect(next_url)
    return redirect("web:cart", lang=lang)


@require_POST
def cart_update_view(request, lang="en"):
    item_code = request.POST.get("item_code", "")
    quantity = int(request.POST.get("quantity", "1"))
    update_cart_quantity(request.session, item_code, quantity)
    return redirect("web:cart", lang=lang)


@require_POST
def cart_remove_view(request, lang="en"):
    item_code = request.POST.get("item_code", "")
    remove_from_cart(request.session, item_code)
    return redirect("web:cart", lang=lang)


# ---------------------------------------------------------------------------
# Checkout  (Cash on Delivery only)
# ---------------------------------------------------------------------------


def checkout_view(request, lang="en"):
    _set_lang(request, lang)
    if not request.user.is_authenticated:
        return _redirect_login(request, lang)
    t = get_translations(lang)
    cart_items = get_cart_items(request.session)
    cart_total = get_cart_total(request.session)

    ctx = _base_context(request, lang)

    if request.method == "POST" and cart_items:
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Find center label
            center_label = cd["assiut_center"]
            for c in ASSIUT_CENTERS:
                if c["value"] == cd["assiut_center"]:
                    center_label = c["label"].get(lang, c["label"]["en"])
                    break

            # --- 1) Create Sales Order in ERPNext ---
            erp_so_name = ""
            erp_error = ""
            try:
                erp_resp = create_sales_order(
                    customer_name=cd["full_name"],
                    phone=cd["phone"],
                    center=center_label,
                    address=cd["address_details"],
                    landmark=cd.get("landmark", ""),
                    notes=cd.get("notes", ""),
                    cart_items=cart_items,
                )
                erp_so_name = (erp_resp.get("data") or {}).get("name", "")
            except Exception as exc:
                logger.error("ERPNext Sales Order creation failed: %s", exc)
                erp_error = str(exc)

            # --- 2) Create local Order record ---
            local_order = None
            try:
                local_order = create_local_order(
                    customer_name=cd["full_name"],
                    phone=cd["phone"],
                    center=center_label,
                    address=cd["address_details"],
                    landmark=cd.get("landmark", ""),
                    notes=cd.get("notes", ""),
                    cart_items=cart_items,
                    erp_so_name=erp_so_name,
                )
            except Exception as exc:
                logger.error("Local order creation failed: %s", exc)

            # --- 3) Build WhatsApp message ---
            order_message = _build_order_message(
                cd, cart_items, cart_total, lang, t,
                erp_so_name=erp_so_name,
            )
            wa_link = get_whatsapp_link(order_message)

            # Optional automation (pywhatkit - local only)
            send_welcome_message(
                message=order_message,
                phone=cd["phone"],
            )

            ctx.update({
                "order_submitted": True,
                "order_message": order_message,
                "whatsapp_link": wa_link,
                "erp_so_name": erp_so_name,
                "erp_error": erp_error,
                "local_order": local_order,
                "cart_items": cart_items,
                "cart_total": cart_total,
                "form": form,
            })
            clear_cart(request.session)
            return render(request, "web/checkout.html", ctx)
        # Form invalid — fall through to render with errors
    else:
        form = CheckoutForm()

    ctx.update({
        "form": form,
        "cart_items": cart_items,
        "cart_total": cart_total,
        "centers": ASSIUT_CENTERS,
        "order_submitted": False,
    })
    return render(request, "web/checkout.html", ctx)


def _build_order_message(cleaned, cart_items, cart_total, lang, t, erp_so_name=""):
    """Build the WhatsApp order message text."""
    lines = ["🛒 *New Order from HD Store Website*", ""]
    lines.append(f"Welcome {cleaned['full_name']}! Your order details are below.")
    lines.append("")
    if erp_so_name:
        lines.append(f"📋 *Sales Order:* {erp_so_name}")
    lines.append(f"👤 *Name:* {cleaned['full_name']}")
    lines.append(f"📞 *Phone:* {cleaned['phone']}")

    # Find center label
    center_label = cleaned["assiut_center"]
    for c in ASSIUT_CENTERS:
        if c["value"] == cleaned["assiut_center"]:
            center_label = c["label"].get(lang, c["label"]["en"])
            break
    lines.append(f"📍 *Center:* {center_label}")
    lines.append(f"🏠 *Address:* {cleaned['address_details']}")
    if cleaned.get("landmark"):
        lines.append(f"🔖 *Landmark:* {cleaned['landmark']}")
    lines.append("")
    lines.append("📦 *Order Items:*")
    for item in cart_items:
        name = item["product"]["name"].get(lang, item["product"]["name"]["en"])
        qty = item["quantity"]
        total = item["line_total"]
        lines.append(f"  • {name} × {qty} — {format_price(total)} EGP")
    lines.append("")
    lines.append(f"💰 *Total:* {format_price(cart_total)} EGP")
    lines.append("💳 *Payment:* Cash on Delivery")
    if cleaned.get("notes"):
        lines.append(f"📝 *Notes:* {cleaned['notes']}")

    lines.append("")
    lines.append(f"✅ Thanks {cleaned['full_name']}! Your order is received. We will contact you soon.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


def search_view(request, lang="en"):
    _set_lang(request, lang)
    query = request.GET.get("q", "").strip()
    products = []
    if query:
        products = filter_products(q=query)

    ctx = _base_context(request, lang)
    ctx.update({
        "query": query,
        "products": products,
    })
    return render(request, "web/search.html", ctx)


# ---------------------------------------------------------------------------
# Offers
# ---------------------------------------------------------------------------


def offers_view(request, lang="en"):
    _set_lang(request, lang)
    all_products = get_all_products()
    # Products that have old prices (on sale) or tagged Hot Deal
    products = [
        p for p in all_products
        if p.get("oldPriceEGP") or "Hot Deal" in (p.get("tags") or [])
    ]
    # If nothing qualifies, show all products
    if not products:
        products = all_products

    ctx = _base_context(request, lang)
    ctx.update({
        "products": products,
    })
    return render(request, "web/offers.html", ctx)


# ---------------------------------------------------------------------------
# Static / info pages
# ---------------------------------------------------------------------------


def about_view(request, lang="en"):
    _set_lang(request, lang)
    ctx = _base_context(request, lang)
    return render(request, "web/about.html", ctx)


def contact_view(request, lang="en"):
    _set_lang(request, lang)
    ctx = _base_context(request, lang)
    return render(request, "web/contact.html", ctx)


def faq_view(request, lang="en"):
    _set_lang(request, lang)
    t = get_translations(lang)

    faq_items = []
    for i in range(1, 20):
        q_key = f"q{i}"
        a_key = f"a{i}"
        q_text = t.faq[q_key]
        a_text = t.faq[a_key]
        if q_text and a_text:
            faq_items.append({"q": q_text, "a": a_text})
        else:
            break

    ctx = _base_context(request, lang)
    ctx.update({"faq_items": faq_items})
    return render(request, "web/faq.html", ctx)


def policies_view(request, lang="en"):
    _set_lang(request, lang)
    t = get_translations(lang)

    policy_sections = [
        {
            "icon": "lock",
            "title": str(t.policies.privacy),
            "points": [str(t.policies.privacyText)],
        },
        {
            "icon": "file-text",
            "title": str(t.policies.terms),
            "points": [str(t.policies.termsText)],
        },
        {
            "icon": "truck",
            "title": str(t.policies.shippingPolicy),
            "points": [str(t.policies.shippingText)],
        },
        {
            "icon": "scale",
            "title": str(t.policies.legal),
            "points": [str(t.policies.legalText)],
        },
    ]

    ctx = _base_context(request, lang)
    ctx.update({"policy_sections": policy_sections})
    return render(request, "web/policies.html", ctx)


def warranty_view(request, lang="en"):
    _set_lang(request, lang)
    t = get_translations(lang)

    warranty_sections = [
        {
            "icon": "shield-check",
            "title": str(t.warranty.warrantyTitle),
            "points": [
                str(t.warranty.warrantyText1),
                str(t.warranty.warrantyText2),
                str(t.warranty.warrantyText3),
            ],
        },
        {
            "icon": "refresh-cw",
            "title": str(t.warranty.returnsTitle),
            "points": [str(t.warranty.returnsText1)],
        },
        {
            "icon": "list-checks",
            "title": str(t.warranty.returnsConditions),
            "points": [
                str(t.warranty.returnsCond1),
                str(t.warranty.returnsCond2),
                str(t.warranty.returnsCond3),
                str(t.warranty.returnsCond4),
                str(t.warranty.returnsCond5),
                str(t.warranty.returnsCond6),
            ],
        },
        {
            "icon": "repeat",
            "title": str(t.warranty.returnsProcess),
            "points": [str(t.warranty.returnsProcessText)],
        },
    ]

    warranty_exclusions = [
        str(t.warranty.noteText),
    ]

    ctx = _base_context(request, lang)
    ctx.update({
        "warranty_sections": warranty_sections,
        "warranty_exclusions": warranty_exclusions,
    })
    return render(request, "web/warranty.html", ctx)
