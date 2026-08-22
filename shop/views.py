from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import (
    add_to_cart,
    cart_totals,
    clear_cart,
    get_cart,
    remove_cart_item,
    set_cart_mode,
    update_cart_item,
)
from .forms import AddToCartForm, CheckoutForm, WholesaleInquiryForm
from .models import FootwearStyle, GenderCategory, Order, OrderItem, Product


def home(request):
    featured = Product.objects.filter(is_active=True, is_featured=True)[:8]
    categories = GenderCategory.objects.all()
    styles = FootwearStyle.objects.all()[:6]
    return render(
        request,
        "shop/home.html",
        {"featured_products": featured, "categories": categories, "styles": styles},
    )


def product_list(request):
    products = Product.objects.filter(is_active=True)
    gender_slug = request.GET.get("gender")
    style_slug = request.GET.get("style")
    search = request.GET.get("q", "").strip()
    mode = request.GET.get("mode", "retail")

    if gender_slug:
        products = products.filter(gender__slug=gender_slug)
    if style_slug:
        products = products.filter(style__slug=style_slug)
    if search:
        products = products.filter(
            Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(style__name__icontains=search)
        )

    return render(
        request,
        "shop/product_list.html",
        {
            "products": products,
            "categories": GenderCategory.objects.all(),
            "styles": FootwearStyle.objects.all(),
            "active_gender": gender_slug,
            "active_style": style_slug,
            "search_query": search,
            "shop_mode": mode,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related = (
        Product.objects.filter(is_active=True, style=product.style)
        .exclude(pk=product.pk)[:4]
    )
    mode = request.GET.get("mode", request.session.get("cart", {}).get("mode", "retail"))
    return render(
        request,
        "shop/product_detail.html",
        {"product": product, "related_products": related, "shop_mode": mode},
    )


def category_view(request, slug):
    category = get_object_or_404(GenderCategory, slug=slug)
    products = Product.objects.filter(is_active=True, gender=category)
    mode = request.GET.get("mode", "retail")
    return render(
        request,
        "shop/category.html",
        {
            "category": category,
            "products": products,
            "styles": FootwearStyle.objects.all(),
            "shop_mode": mode,
        },
    )


def style_view(request, slug):
    style = get_object_or_404(FootwearStyle, slug=slug)
    products = Product.objects.filter(is_active=True, style=style)
    return render(
        request,
        "shop/style.html",
        {"style": style, "products": products, "shop_mode": request.GET.get("mode", "retail")},
    )


@require_POST
def add_to_cart_view(request):
    form = AddToCartForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid cart request.")
        return redirect("shop:product_list")

    try:
        add_to_cart(
            request.session,
            form.cleaned_data["product_id"],
            form.cleaned_data["quantity"],
            form.cleaned_data.get("size", ""),
            form.cleaned_data.get("order_mode", "retail"),
        )
        messages.success(request, "Added to cart successfully!")
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
    except ValueError as exc:
        messages.error(request, str(exc))

    product = Product.objects.filter(pk=form.cleaned_data["product_id"]).first()
    if product:
        return redirect("shop:product_detail", slug=product.slug)
    return redirect("shop:product_list")


def cart_view(request):
    cart = get_cart(request.session)
    totals = cart_totals(cart)
    return render(request, "shop/cart.html", {"cart_data": totals})


@require_POST
def update_cart_view(request):
    key = request.POST.get("key")
    quantity = int(request.POST.get("quantity", 1))
    update_cart_item(request.session, key, quantity)
    return redirect("shop:cart")


@require_POST
def remove_from_cart_view(request):
    key = request.POST.get("key")
    remove_cart_item(request.session, key)
    messages.info(request, "Item removed from cart.")
    return redirect("shop:cart")


@require_POST
def set_mode_view(request):
    mode = request.POST.get("mode", "retail")
    if mode in ("retail", "wholesale"):
        set_cart_mode(request.session, mode)
        messages.success(
            request,
            "Switched to wholesale pricing." if mode == "wholesale" else "Switched to retail pricing.",
        )
    return redirect(request.POST.get("next", "shop:cart"))


def checkout_view(request):
    cart = get_cart(request.session)
    totals = cart_totals(cart)

    if not totals["items"]:
        messages.warning(request, "Your cart is empty.")
        return redirect("shop:product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_type = totals["mode"]
            order.total_amount = totals["subtotal"]
            order.save()

            for item in totals["items"]:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    size=item["size"],
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                    line_total=item["line_total"],
                )

            clear_cart(request.session)
            messages.success(request, f"Order #{order.pk} placed successfully!")
            return redirect("shop:order_success", order_id=order.pk)
    else:
        form = CheckoutForm()

    return render(
        request,
        "shop/checkout.html",
        {"form": form, "cart_data": totals},
    )


def order_success(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "shop/order_success.html", {"order": order})


def wholesale_page(request):
    products = Product.objects.filter(is_active=True).order_by("name")
    form = WholesaleInquiryForm(request.POST or None, initial={"estimated_quantity": 50})

    if request.method == "POST" and form.is_valid():
        messages.success(
            request,
            "Thank you! Our wholesale team will contact you within 24 hours.",
        )
        return redirect("shop:wholesale")

    return render(
        request,
        "shop/wholesale.html",
        {"form": form, "products": products},
    )


def about_page(request):
    return render(request, "shop/about.html")
