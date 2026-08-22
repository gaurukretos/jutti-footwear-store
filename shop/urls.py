from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/", views.category_view, name="category"),
    path("style/<slug:slug>/", views.style_view, name="style"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/", views.add_to_cart_view, name="add_to_cart"),
    path("cart/update/", views.update_cart_view, name="update_cart"),
    path("cart/remove/", views.remove_from_cart_view, name="remove_from_cart"),
    path("cart/mode/", views.set_mode_view, name="set_mode"),
    path("checkout/", views.checkout_view, name="checkout"),
    path("order/<int:order_id>/success/", views.order_success, name="order_success"),
    path("wholesale/", views.wholesale_page, name="wholesale"),
    path("about/", views.about_page, name="about"),
]
