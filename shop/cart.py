from decimal import Decimal

from django.conf import settings

from .models import Product


def get_cart(session):
    return session.setdefault("cart", {"mode": "retail", "items": {}})


def cart_item_count(cart):
    return sum(item["quantity"] for item in cart.get("items", {}).values())


def cart_totals(cart):
    items = []
    subtotal = Decimal("0.00")
    mode = cart.get("mode", "retail")

    for key, item in cart.get("items", {}).items():
        try:
            product = Product.objects.get(pk=item["product_id"], is_active=True)
        except Product.DoesNotExist:
            continue

        unit_price = (
            product.wholesale_price if mode == "wholesale" else product.retail_price
        )
        line_total = unit_price * item["quantity"]
        subtotal += line_total
        items.append(
            {
                "key": key,
                "product": product,
                "size": item.get("size", ""),
                "quantity": item["quantity"],
                "unit_price": unit_price,
                "line_total": line_total,
            }
        )

    return {"items": items, "subtotal": subtotal, "mode": mode}


def add_to_cart(session, product_id, quantity, size="", mode="retail"):
    cart = get_cart(session)
    cart["mode"] = mode
    key = f"{product_id}:{size}"

    product = Product.objects.get(pk=product_id, is_active=True)
    if mode == "wholesale" and quantity < product.min_wholesale_qty:
        raise ValueError(
            f"Wholesale minimum is {product.min_wholesale_qty} pairs for {product.name}"
        )

    if key in cart["items"]:
        cart["items"][key]["quantity"] += quantity
    else:
        cart["items"][key] = {
            "product_id": product_id,
            "quantity": quantity,
            "size": size,
        }

    session["cart"] = cart
    session.modified = True


def update_cart_item(session, key, quantity):
    cart = get_cart(session)
    if key not in cart["items"]:
        return

    if quantity <= 0:
        del cart["items"][key]
    else:
        cart["items"][key]["quantity"] = quantity

    session["cart"] = cart
    session.modified = True


def remove_cart_item(session, key):
    cart = get_cart(session)
    cart["items"].pop(key, None)
    session["cart"] = cart
    session.modified = True


def clear_cart(session):
    session["cart"] = {"mode": "retail", "items": {}}
    session.modified = True


def set_cart_mode(session, mode):
    cart = get_cart(session)
    cart["mode"] = mode
    session["cart"] = cart
    session.modified = True
