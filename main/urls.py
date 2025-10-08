# main/urls.py
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # Pages
    path("", views.show_main, name="show_main"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/<uuid:pk>/", views.product_detail, name="product_detail"),
    path("products/<uuid:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<uuid:pk>/delete/", views.product_delete, name="product_delete"),

    # Data-delivery endpoints (JSON/XML)
    path("products/json/", views.product_list_json, name="product_list_json"),
    path("products/xml/", views.product_list_xml, name="product_list_xml"),
    path("products/json/<uuid:pk>/", views.product_detail_json, name="product_detail_json"),
    path("products/xml/<uuid:pk>/", views.product_detail_xml, name="product_detail_xml"),

    # API (JSON) endpoints
    path("api/products/", views.api_product_list, name="api_product_list"),
    path("api/products/<uuid:pk>/", views.api_product_detail, name="api_product_detail"),

    # Auth
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]