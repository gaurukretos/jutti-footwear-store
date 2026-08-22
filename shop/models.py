from django.db import models


class GenderCategory(models.Model):
    class Gender(models.TextChoices):
        MEN = "men", "Men"
        WOMEN = "women", "Women"
        CHILD = "child", "Child"

    slug = models.SlugField(unique=True, choices=Gender.choices)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True, help_text="Emoji icon")

    class Meta:
        verbose_name_plural = "Gender categories"
        ordering = ["slug"]

    def __str__(self):
        return self.name


class FootwearStyle(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    origin = models.CharField(max_length=100, blank=True, help_text="e.g. Rajasthan, Punjab")

    class Meta:
        verbose_name = "Footwear style"
        verbose_name_plural = "Footwear styles"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    gender = models.ForeignKey(GenderCategory, on_delete=models.CASCADE, related_name="products")
    style = models.ForeignKey(FootwearStyle, on_delete=models.CASCADE, related_name="products")
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_wholesale_qty = models.PositiveIntegerField(default=10)
    stock = models.PositiveIntegerField(default=100)
    image_url = models.URLField(max_length=500, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sizes_available = models.CharField(
        max_length=100,
        default="6,7,8,9,10",
        help_text="Comma-separated sizes",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "name"]

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "https://images.unsplash.com/photo-1543163521-1bf539c55dd1?w=600&h=600&fit=crop"

    @property
    def size_list(self):
        return [s.strip() for s in self.sizes_available.split(",") if s.strip()]


class Order(models.Model):
    class OrderType(models.TextChoices):
        RETAIL = "retail", "Retail"
        WHOLESALE = "wholesale", "Wholesale"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    order_type = models.CharField(max_length=20, choices=OrderType.choices, default=OrderType.RETAIL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200, blank=True)
    gst_number = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="Rajasthan")
    pincode = models.CharField(max_length=10)
    notes = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.customer_name} ({self.order_type})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    size = models.CharField(max_length=10, blank=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
