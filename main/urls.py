# main/urls.py
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    # Pages (already implemented in your app)
    path("", views.show_main, name="show_main"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/<uuid:pk>/", views.product_detail, name="product_detail"),  # Changed from int to uuid

    # Assignment 3 data-delivery endpoints
    path("products/json/", views.product_list_json, name="product_list_json"),
    path("products/xml/", views.product_list_xml, name="product_list_xml"),
    path("products/json/<uuid:pk>/", views.product_detail_json, name="product_detail_json"),  # Changed from int to uuid
    path("products/xml/<uuid:pk>/", views.product_detail_xml, name="product_detail_xml"),  # Changed from int to uuid
]