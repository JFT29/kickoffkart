from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.core import serializers
from .models import Product
from .forms import ProductForm

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

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect("main:show_main")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

# Data delivery: list (JSON/XML)
def product_list_json(request):
    data = serializers.serialize("json", Product.objects.all())
    return HttpResponse(data, content_type="application/json")

def product_list_xml(request):
    data = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(data, content_type="application/xml")

# Data delivery: by id (JSON/XML)
def product_detail_json(request, pk):
    qs = Product.objects.filter(pk=pk)
    if not qs.exists():
        raise Http404("Product not found")
    data = serializers.serialize("json", qs)
    return HttpResponse(data, content_type="application/json")

def product_detail_xml(request, pk):
    qs = Product.objects.filter(pk=pk)
    if not qs.exists():
        raise Http404("Product not found")
    data = serializers.serialize("xml", qs)
    return HttpResponse(data, content_type="application/xml")