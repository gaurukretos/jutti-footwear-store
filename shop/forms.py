from django import forms

from .models import Order, Product


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    size = forms.CharField(max_length=10, required=False)
    quantity = forms.IntegerField(min_value=1, initial=1)
    order_mode = forms.ChoiceField(
        choices=[("retail", "Retail"), ("wholesale", "Wholesale")],
        initial="retail",
        widget=forms.HiddenInput(),
    )


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer_name",
            "customer_email",
            "customer_phone",
            "company_name",
            "gst_number",
            "address",
            "city",
            "state",
            "pincode",
            "notes",
        ]
        labels = {
            "customer_name": "Full Name",
            "customer_email": "Email",
            "customer_phone": "Phone",
            "company_name": "Company / Shop Name",
            "gst_number": "GST Number",
            "address": "Delivery Address",
            "city": "City",
            "state": "State",
            "pincode": "PIN Code",
            "notes": "Order Notes",
        }
        widgets = {
            "customer_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Full name"}),
            "customer_email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "email@example.com"}),
            "customer_phone": forms.TextInput(attrs={"class": "form-input", "placeholder": "+91 98765 43210"}),
            "company_name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Business name (wholesale)"}),
            "gst_number": forms.TextInput(attrs={"class": "form-input", "placeholder": "GSTIN (optional)"}),
            "address": forms.Textarea(attrs={"class": "form-input", "rows": 3, "placeholder": "Street address"}),
            "city": forms.TextInput(attrs={"class": "form-input", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-input", "placeholder": "State"}),
            "pincode": forms.TextInput(attrs={"class": "form-input", "placeholder": "PIN code"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2, "placeholder": "Special instructions"}),
        }


class WholesaleInquiryForm(forms.Form):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Your name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": "Business email"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Phone number"}))
    company = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Company / Shop name"}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "City"}))
    product_interest = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True),
        required=False,
        empty_label="All products / General inquiry",
        widget=forms.Select(attrs={"class": "form-input"}),
    )
    estimated_quantity = forms.IntegerField(
        min_value=10,
        initial=50,
        widget=forms.NumberInput(attrs={"class": "form-input", "placeholder": "Min 10 pairs"}),
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-input", "rows": 4, "placeholder": "Tell us about your bulk order requirements..."}),
    )
