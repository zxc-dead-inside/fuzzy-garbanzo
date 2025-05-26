from django.urls import path
from .api_views import (
    CategoryListAPIView, CategoryDetailAPIView,
    ProductListAPIView, ProductDetailAPIView
)

urlpatterns = [
    path('categories/',
         CategoryListAPIView.as_view(),
         name='api_category_list'),
    path('categories/<int:id>/',
         CategoryDetailAPIView.as_view(),
         name='api_category_detail'),
    path('products/',
         ProductListAPIView.as_view(),
         name='api_product_list'),
    path('products/<int:id>/',
         ProductDetailAPIView.as_view(),
         name='api_product_detail'),
]
