# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    JsonResponse,
    Http404,
    HttpResponseForbidden,
)
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.forms import ModelForm
from django.middleware.csrf import get_token

from .models import Product
from .forms import ProductForm


# Simple login page redirect (if you still link to a dedicated page)
def login_page(request):
    return render(request, "login.html")


# ------------------------------------------------------------------
# Helper for unified product JSON shape
# ------------------------------------------------------------------
def product_to_dict(p):
    return {
        "pk": str(p.pk),
        "name": p.name,
        "price": p.price,
        "description": p.description,
        "thumbnail": p.thumbnail,
        "category": p.category,
        "is_featured": p.is_featured,
        "detail_url": reverse("main:product_detail", kwargs={"pk": p.pk}),
    }


class ProductAjaxForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "thumbnail", "category", "is_featured"]


@login_required(login_url="main:login")
def show_main(request):
    category = request.GET.get("category")
    qs = Product.objects.filter(user=request.user).order_by("-is_featured", "name")
    if category:
        qs = qs.filter(category=category)
    # AJAX lightweight list?
    if request.GET.get("ajax"):
        data = [product_to_dict(p) for p in qs]
        return JsonResponse({"count": len(data), "category": category, "products": data})
    context = {
        "app_name": "KickoffKart",
        "your_name": "Juansao Fortunio Tandi",
        "your_class": "KKI",
        "your_npm": "2406365345",
        "products": list(qs),
        "total_products": qs.count(),
        "active_category": category or "",
        "selected_category": category,
        "last_login": request.COOKIES.get("last_login"),
    }
    return render(request, "main.html", context)


@login_required(login_url="main:login")
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST or None, request.FILES or None)
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

        if is_ajax and not request.user.is_authenticated:
            return JsonResponse({"ok": False, "error": "auth_required"}, status=401)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            if is_ajax:
                return JsonResponse({"ok": True, "product": product_to_dict(obj)})
            messages.success(request, "Product created.")
            return redirect("main:show_main")
        else:
            if is_ajax:
                return JsonResponse({"ok": False, "errors": form.errors}, status=400)
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
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
        if is_ajax:
            return JsonResponse({"ok": False, "error": "forbidden"}, status=403)
        return HttpResponseForbidden("Forbidden")
    if request.method == "POST":
        form = ProductForm(request.POST or None, request.FILES or None, instance=product)
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"

        if is_ajax and not request.user.is_authenticated:
            return JsonResponse({"ok": False, "error": "auth_required"}, status=401)

        if form.is_valid():
            updated = form.save()
            if is_ajax:
                return JsonResponse({"ok": True, "product": product_to_dict(updated)})
            messages.success(request, "Product updated successfully.")
            return redirect("main:product_detail", pk=product.pk)
        else:
            if is_ajax:
                return JsonResponse({"ok": False, "errors": form.errors}, status=400)
    else:
        form = ProductForm(instance=product)
    return render(request, "product_edit.html", {"form": form, "product": product})


@login_required(login_url="main:login")
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user != request.user:
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
        if is_ajax:
            return JsonResponse({"ok": False, "error": "forbidden"}, status=403)
        return HttpResponseForbidden("Forbidden")
    if request.method == "POST":
        is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
        if is_ajax and not request.user.is_authenticated:
            return JsonResponse({"ok": False, "error": "auth_required"}, status=401)
        pk_str = str(product.pk)
        product.delete()
        if is_ajax:
            return JsonResponse({"ok": True, "deleted": pk_str})
        messages.success(request, "Product deleted successfully.")
        return redirect("main:show_main")
    messages.warning(request, "Delete must be submitted as POST.")
    return redirect("main:product_detail", pk=pk)


# Legacy data delivery
def product_list_json(request):
    data = serializers.serialize("json", Product.objects.all())
    return HttpResponse(data, content_type="application/json")


def product_list_xml(request):
    data = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(data, content_type="application/xml")


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


# Standard HTML auth views
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
            nxt = request.GET.get("next") or None
            response = redirect(nxt) if nxt else redirect("main:show_main")
            response.set_cookie(
                "last_login",
                timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                httponly=True,
                samesite="Lax",
            )
            return response
    else:
        form = AuthenticationForm()
    get_token(request)
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    response = redirect("main:login")
    response.delete_cookie("last_login")
    return response


# API (read)
@login_required
def api_product_list(request):
    qs = Product.objects.filter(user=request.user).order_by("-is_featured", "name")
    category = request.GET.get("category")
    if category:
        qs = qs.filter(category=category)
    data = [product_to_dict(p) for p in qs]
    return JsonResponse({"products": data}, status=200)


@login_required
def api_product_detail(request, pk):
    p = get_object_or_404(Product, pk=pk, user=request.user)
    return JsonResponse(product_to_dict(p), status=200)


# API (write)
@login_required
@require_POST
def api_product_create(request):
    form = ProductAjaxForm(request.POST)
    if form.is_valid():
        p = form.save(commit=False)
        p.user = request.user
        p.save()
        return JsonResponse({"ok": True, "product": product_to_dict(p)}, status=201)
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def api_product_update(request, pk):
    p = get_object_or_404(Product, pk=pk, user=request.user)
    form = ProductAjaxForm(request.POST, instance=p)
    if form.is_valid():
        p = form.save()
        return JsonResponse({"ok": True, "product": product_to_dict(p)}, status=200)
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def api_product_delete(request, pk):
    p = get_object_or_404(Product, pk=pk, user=request.user)
    pk_str = str(p.pk)
    p.delete()
    return JsonResponse({"ok": True, "deleted": pk_str}, status=200)


# API auth (form-encoded)
@require_POST
def api_login(request):
    username = request.POST.get("username", "").strip()
    password = request.POST.get("password", "")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        next_url = request.GET.get("next") or request.POST.get("next") or reverse("main:show_main")
        return JsonResponse({"ok": True, "redirect": next_url})
    return JsonResponse({"ok": False, "error": "Invalid credentials."}, status=400)


@require_POST
def api_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({"ok": True}, status=200)


@require_POST
def api_register(request):
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "")
    if not username or not password:
        return JsonResponse({"ok": False, "errors": {"__all__": ["Username and password are required."]}}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"ok": False, "errors": {"username": ["Username already taken."]}}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    return JsonResponse({"ok": True, "redirect": reverse("main:show_main"), "user": {"username": user.username}}, status=201)