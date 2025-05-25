from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer


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
