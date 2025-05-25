from django.urls import path
from .api_views import CategoryListAPIView, CategoryDetailAPIView

urlpatterns = [
    path('categories/',
         CategoryListAPIView.as_view(),
         name='api_category_list'),
    path('categories/<int:id>/',
         CategoryDetailAPIView.as_view(),
         name='api_category_detail'),
]
