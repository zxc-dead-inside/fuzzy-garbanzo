from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filters import ProductFilter
from .tasks.export import generate_product_xls


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


class ProductExportXLSAPIView(APIView):
    """API: Trigers product export to Excel file"""

    def post(self, request):
        task = generate_product_xls.delay()
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
