from django.contrib import admin
from django.urls import include, path

from .views import ProductCategoryListView, MakerListView, ProductListView

app_name = "products"

urlpatterns = [
    path("categories/", ProductCategoryListView.as_view(), name="categories-list"),
    path("makers/", MakerListView.as_view(), name = "makers-list"),
    path("", ProductListView.as_view(), name = "products-list")
]
