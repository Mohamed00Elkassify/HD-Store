"""URL configuration for the web app."""
from django.urls import path
from . import views

app_name = "web"

urlpatterns = [
    # Root redirect → /en/
    path("", views.root_redirect, name="root"),

    # ---------- Locale-prefixed pages ----------
    path("<str:lang>/", views.home_view, name="home"),
    path("<str:lang>/login/", views.login_view, name="login"),
    path("<str:lang>/register/", views.register_view, name="register"),
    path("<str:lang>/logout/", views.logout_view, name="logout"),
    path("<str:lang>/products/", views.products_view, name="products"),
    path("<str:lang>/products/<path:slug>/", views.product_detail_view, name="product_detail"),
    path("<str:lang>/cart/", views.cart_view, name="cart"),
    path("<str:lang>/cart/add/", views.cart_add_view, name="cart_add"),
    path("<str:lang>/cart/update/", views.cart_update_view, name="cart_update"),
    path("<str:lang>/cart/remove/", views.cart_remove_view, name="cart_remove"),
    path("<str:lang>/checkout/", views.checkout_view, name="checkout"),
    path("<str:lang>/search/", views.search_view, name="search"),
    path("<str:lang>/offers/", views.offers_view, name="offers"),
    path("<str:lang>/about/", views.about_view, name="about"),
    path("<str:lang>/contact/", views.contact_view, name="contact"),
    path("<str:lang>/faq/", views.faq_view, name="faq"),
    path("<str:lang>/policies/", views.policies_view, name="policies"),
    path("<str:lang>/warranty/", views.warranty_view, name="warranty"),
]
