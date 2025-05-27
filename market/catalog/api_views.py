from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter


class CategoryListAPIView(generics.ListAPIView):
    """API: List of root categories with children"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.get_root_categories().prefetch_related('children')


class CategoryDetailAPIView(generics.RetrieveAPIView):
    """API: Category detail by ID"""
    queryset = Category.objects.filter(
        is_active=True).prefetch_related('children')
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductListAPIView(generics.ListAPIView):
    """API: List of active products"""
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True).select_related('category')


class ProductDetailAPIView(generics.RetrieveAPIView):
    """API: Product detail by ID"""
    queryset = Product.objects.filter(
        is_active=True).select_related('category')
    serializer_class = ProductSerializer
    lookup_field = 'id'
