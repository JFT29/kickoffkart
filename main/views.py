# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseForbidden
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Product
from .forms import ProductForm


def product_to_dict(p, request):
    """Convert a Product instance to a dictionary with URLs."""
    return {
        "id": str(p.pk),
        "name": p.name,
        "price": p.price,
        "description": p.description,
        "thumbnail": p.thumbnail,  # external URL or static path
        "category": p.category,
        "is_featured": p.is_featured,
        "urls": {
            "detail": reverse("main:product_detail", kwargs={"pk": p.pk}),
            "edit": reverse("main:product_edit", kwargs={"pk": p.pk}) if hasattr(p, "user") and p.user_id == request.user.id else None,
            "delete": reverse("main:product_delete", kwargs={"pk": p.pk}) if hasattr(p, "user") and p.user_id == request.user.id else None,
        }
    }


@login_required(login_url="main:login")
def show_main(request):
    products_qs = Product.objects.filter(user=request.user).order_by("-is_featured", "name")

    category = request.GET.get("category")
    if category:
        products_qs = products_qs.filter(category=category)

    # If ajax=1 (or any truthy value), return JSON instead of HTML (lightweight reuse)
    if request.GET.get("ajax"):
        data = list(
            products_qs.values(
                "id",
                "name",
                "price",
                "category",
                "description",
                "thumbnail",
                "is_featured",
            )
        )
        return JsonResponse(
            {
                "count": len(data),
                "category": category,
                "products": data,
            },
            safe=False,
        )

    last_login = request.COOKIES.get("last_login")

    context = {
        "app_name": "KickoffKart",
        "your_name": "Juansao Fortunio Tandi",
        "your_class": "KKI",
        "your_npm": "2406365345",
        "total_products": products_qs.count(),
        "products": products_qs,
        "last_login": last_login,
        "selected_category": category,
    }
    return render(request, "main.html", context)


@login_required(login_url="main:login")
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Product created.")
            return redirect("main:show_main")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})


@login_required(login_url="main:login")
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


@login_required(login_url="main:login")
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user != request.user:
        messages.error(request, "You are not allowed to edit this item.")
        return HttpResponseForbidden("Forbidden")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES or None, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("main:product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "product_edit.html", {"form": form, "product": product})


@login_required(login_url="main:login")
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user != request.user:
        messages.error(request, "You are not allowed to delete this item.")
        return HttpResponseForbidden("Forbidden")

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("main:show_main")

    messages.warning(request, "Delete must be submitted as POST.")
    return redirect("main:product_detail", pk=pk)


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


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect("main:login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get("next")
            if next_url:
                response = redirect(next_url)
            else:
                response = redirect("main:show_main")

            response.set_cookie(
                "last_login",
                timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                httponly=True,
                samesite="Lax",
            )
            return response
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    response = redirect("main:login")
    response.delete_cookie("last_login")
    return response


# API endpoints
@login_required
def api_product_list(request):
    qs = Product.objects.filter(user=request.user).order_by("-is_featured", "name")
    category = request.GET.get("category")
    if category:
        qs = qs.filter(category=category)
    data = [product_to_dict(p, request) for p in qs]
    return JsonResponse({"products": data}, status=200)


@login_required
def api_product_detail(request, pk):
    p = get_object_or_404(Product, pk=pk, user=request.user)
    return JsonResponse(product_to_dict(p, request), status=200)