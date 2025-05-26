from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    path('', views.CategoryListView.as_view(),
         name='category_list'),
    path('category/<slug:slug>/',
         views.CategoryDetailView.as_view(),
         name='category_detail'),
    path('products/', views.ProductListView.as_view(),
         name='product_list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(),
         name='product_detail'),
]
