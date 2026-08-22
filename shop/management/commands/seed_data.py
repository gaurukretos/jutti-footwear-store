from decimal import Decimal

from django.core.management.base import BaseCommand

from shop.models import FootwearStyle, GenderCategory, Product


class Command(BaseCommand):
    help = "Seed database with dummy footwear data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        GenderCategory.objects.all().delete()
        FootwearStyle.objects.all().delete()
        Product.objects.all().delete()

        categories = {
            "men": GenderCategory.objects.create(
                slug="men", name="Men", icon="👞",
                description="Premium footwear for men — juttis, mojaris, sandals & more.",
            ),
            "women": GenderCategory.objects.create(
                slug="women", name="Women", icon="👡",
                description="Elegant ethnic & contemporary footwear for women.",
            ),
            "child": GenderCategory.objects.create(
                slug="child", name="Child", icon="👟",
                description="Comfortable, colorful footwear for kids of all ages.",
            ),
        }

        styles_data = [
            ("rajasthani-jutti", "Rajasthani Jutti", "Rajasthan", "Handcrafted leather juttis with traditional Rajasthani embroidery."),
            ("punjabi-jutti", "Punjabi Jutti", "Punjab", "Classic Punjabi juttis with phulkari and mirror work."),
            ("mojari", "Mojari", "Rajasthan", "Traditional closed-toe mojaris with intricate stitching."),
            ("kolhapuri", "Kolhapuri Chappal", "Maharashtra", "Authentic Kolhapuri leather chappals."),
            ("leather-sandal", "Leather Sandal", "India", "Premium handcrafted leather sandals."),
            ("wedding-jutti", "Wedding Jutti", "Rajasthan", "Bridal and wedding special juttis with heavy embellishment."),
            ("casual-slipper", "Casual Slipper", "India", "Everyday comfortable slippers and flip-flops."),
            ("sports-shoe", "Sports Shoe", "India", "Lightweight sports and running shoes."),
        ]

        styles = {}
        for slug, name, origin, desc in styles_data:
            styles[slug] = FootwearStyle.objects.create(
                slug=slug, name=name, origin=origin, description=desc,
            )

        products_data = [
            # Men - Rajasthani Jutti
            ("Royal Maroon Rajasthani Jutti", "royal-maroon-rajasthani-jutti-men", "men", "rajasthani-jutti",
             "Handcrafted maroon leather jutti with golden zari embroidery. Perfect for weddings and festivals.",
             1299, 899, 12, True, "https://images.unsplash.com/photo-1608256246200-53bd35f301f4?w=600&h=600&fit=crop"),
            ("Jaipur Blue Mirror Jutti", "jaipur-blue-mirror-jutti-men", "men", "rajasthani-jutti",
             "Vibrant blue jutti adorned with traditional mirror work from Jaipur artisans.",
             1499, 999, 10, True, "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&h=600&fit=crop"),
            ("Desert Sand Embroidered Jutti", "desert-sand-embroidered-jutti-men", "men", "rajasthani-jutti",
             "Beige-toned jutti with desert-inspired thread embroidery.",
             1199, 799, 10, False, "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&h=600&fit=crop"),
            # Men - Mojari
            ("Heritage Black Mojari", "heritage-black-mojari-men", "men", "mojari",
             "Classic black mojari with curved toe and fine leather craftsmanship.",
             1599, 1099, 10, True, "https://images.unsplash.com/photo-1533867617855-e8b583a4a7a4?w=600&h=600&fit=crop"),
            ("Jodhpuri Tan Mojari", "jodhpuri-tan-mojari-men", "men", "mojari",
             "Tan leather mojari inspired by Jodhpur royal footwear traditions.",
             1399, 949, 10, False, "https://images.unsplash.com/photo-1543163521-1bf539c55dd1?w=600&h=600&fit=crop"),
            # Men - Kolhapuri
            ("Classic Brown Kolhapuri", "classic-brown-kolhapuri-men", "men", "kolhapuri",
             "Authentic Kolhapuri chappal made from vegetable-tanned leather.",
             899, 599, 15, False, "https://images.unsplash.com/photo-1525966220537-0d35b5475682?w=600&h=600&fit=crop"),
            # Men - Sandals
            ("Premium Tan Leather Sandal", "premium-tan-leather-sandal-men", "men", "leather-sandal",
             "Open-toe leather sandal with cushioned sole for daily wear.",
             999, 699, 12, False, "https://images.unsplash.com/photo-1603487742131-4160ec966093?w=600&h=600&fit=crop"),
            # Women - Rajasthani Jutti
            ("Peacock Green Bridal Jutti", "peacock-green-bridal-jutti-women", "women", "wedding-jutti",
             "Stunning peacock green bridal jutti with kundan and pearl embellishments.",
             2499, 1699, 8, True, "https://images.unsplash.com/photo-1543163521-1bf539c55dd1?w=600&h=600&fit=crop"),
            ("Pink Phulkari Jutti", "pink-phulkari-jutti-women", "women", "punjabi-jutti",
             "Soft pink jutti with vibrant phulkari embroidery from Punjab.",
             1799, 1199, 10, True, "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&h=600&fit=crop"),
            ("Gold Zari Wedding Jutti", "gold-zari-wedding-jutti-women", "women", "wedding-jutti",
             "Luxurious gold-thread wedding jutti for the special day.",
             2999, 1999, 6, True, "https://images.unsplash.com/photo-1608256246200-53bd35f301f4?w=600&h=600&fit=crop"),
            ("Red Velvet Mojari", "red-velvet-mojari-women", "women", "mojari",
             "Rich red velvet mojari with golden border and comfortable padding.",
             1899, 1299, 10, False, "https://images.unsplash.com/photo-1533867617855-e8b583a4a7a4?w=600&h=600&fit=crop"),
            ("Mehndi Green Ethnic Jutti", "mehndi-green-ethnic-jutti-women", "women", "rajasthani-jutti",
             "Mehndi green jutti with traditional gota patti work.",
             1599, 1099, 10, False, "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&h=600&fit=crop"),
            ("Silver Kolhapuri Women", "silver-kolhapuri-women", "women", "kolhapuri",
             "Stylish Kolhapuri chappal with silver-toned buckle detail.",
             799, 549, 15, False, "https://images.unsplash.com/photo-1525966220537-0d35b5475682?w=600&h=600&fit=crop"),
            ("Block Heel Ethnic Sandal", "block-heel-ethnic-sandal-women", "women", "leather-sandal",
             "Comfortable block heel sandal with ethnic print straps.",
             1299, 899, 10, False, "https://images.unsplash.com/photo-1603487742131-4160ec966093?w=600&h=600&fit=crop"),
            # Child
            ("Kids Rainbow Jutti", "kids-rainbow-jutti-child", "child", "rajasthani-jutti",
             "Colorful mini jutti for kids with soft inner lining.",
             599, 399, 20, True, "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&h=600&fit=crop"),
            ("Boys Mojari Classic", "boys-mojari-classic-child", "child", "mojari",
             "Durable mojari for boys with anti-slip sole.",
             699, 449, 20, False, "https://images.unsplash.com/photo-1533867617855-e8b583a4a7a4?w=600&h=600&fit=crop"),
            ("Girls Pink Sparkle Jutti", "girls-pink-sparkle-jutti-child", "child", "punjabi-jutti",
             "Adorable pink jutti with sparkle details for little princesses.",
             649, 429, 20, True, "https://images.unsplash.com/photo-1608256246200-53bd35f301f4?w=600&h=600&fit=crop"),
            ("Kids Kolhapuri Mini", "kids-kolhapuri-mini-child", "child", "kolhapuri",
             "Mini Kolhapuri chappals — lightweight and easy to wear.",
             449, 299, 25, False, "https://images.unsplash.com/photo-1525966220537-0d35b5475682?w=600&h=600&fit=crop"),
            ("Kids Sports Runner", "kids-sports-runner-child", "child", "sports-shoe",
             "Breathable sports shoes for active kids.",
             899, 599, 15, False, "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&h=600&fit=crop"),
            ("Kids Casual Slipper", "kids-casual-slipper-child", "child", "casual-slipper",
             "Soft EVA slippers for everyday home and outdoor use.",
             299, 199, 30, False, "https://images.unsplash.com/photo-1603487742131-4160ec966093?w=600&h=600&fit=crop"),
            # More men products
            ("Navy Formal Mojari", "navy-formal-mojari-men", "men", "mojari",
             "Navy blue formal mojari for ethnic occasions.",
             1699, 1149, 10, False, "https://images.unsplash.com/photo-1543163521-1bf539c55dd1?w=600&h=600&fit=crop"),
            ("White Wedding Mojari", "white-wedding-mojari-men", "men", "wedding-jutti",
             "Pristine white wedding mojari with subtle silver embroidery.",
             2199, 1499, 8, True, "https://images.unsplash.com/photo-1608256246200-53bd35f301f4?w=600&h=600&fit=crop"),
            ("Men Sports Flex", "men-sports-flex-men", "men", "sports-shoe",
             "Flexible running shoes with mesh upper.",
             1499, 999, 12, False, "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&h=600&fit=crop"),
        ]

        for name, slug, gender, style, desc, retail, wholesale, min_qty, featured, img in products_data:
            Product.objects.create(
                name=name,
                slug=slug,
                gender=categories[gender],
                style=styles[style],
                description=desc,
                retail_price=Decimal(retail),
                wholesale_price=Decimal(wholesale),
                min_wholesale_qty=min_qty,
                stock=150,
                image_url=img,
                is_featured=featured,
                is_active=True,
                sizes_available="4,5,6,7,8,9,10" if gender != "child" else "1,2,3,4,5,6",
            )

        self.stdout.write(self.style.SUCCESS(
            f"Done! Created {GenderCategory.objects.count()} categories, "
            f"{FootwearStyle.objects.count()} styles, {Product.objects.count()} products."
        ))
