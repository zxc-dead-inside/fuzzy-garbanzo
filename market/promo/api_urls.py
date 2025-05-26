from django.urls import path
from .api_views import PromoListAPIView, PromoDetailAPIView

urlpatterns = [
    path('', PromoListAPIView.as_view(), name='promo_list'),
    path('<int:id>/', PromoDetailAPIView.as_view(), name='promo_detail'),
]
