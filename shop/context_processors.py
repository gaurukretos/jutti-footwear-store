from django.conf import settings

from .cart import cart_item_count, get_cart


def cart_context(request):
    cart = get_cart(request.session)
    return {
        "cart_count": cart_item_count(cart),
        "cart_mode": cart.get("mode", "retail"),
        "min_wholesale_qty": getattr(settings, "MIN_WHOLESALE_QUANTITY", 10),
    }
