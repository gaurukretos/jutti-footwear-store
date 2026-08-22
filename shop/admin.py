from django.contrib import admin

from .models import FootwearStyle, GenderCategory, Order, OrderItem, Product


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("line_total",)


@admin.register(GenderCategory)
class GenderCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(FootwearStyle)
class FootwearStyleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "origin")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "gender",
        "style",
        "retail_price",
        "wholesale_price",
        "stock",
        "is_featured",
        "is_active",
    )
    list_filter = ("gender", "style", "is_featured", "is_active")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "order_type",
        "status",
        "total_amount",
        "created_at",
    )
    list_filter = ("order_type", "status", "created_at")
    search_fields = ("customer_name", "customer_email", "customer_phone", "company_name")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at",)
