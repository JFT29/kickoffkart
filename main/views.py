from django.shortcuts import render
from .models import Product

def show_main(request):
    products = Product.objects.all().order_by("-is_featured", "name")
    context = {
        "app_name": "KickoffKart",
        "your_name": "Juansao Fortunio Tandi",
        "your_class": "KKI",
        "your_npm": "2406365345",
        "total_products": products.count(),
        "products": products,
    }
    return render(request, "main.html", context)
