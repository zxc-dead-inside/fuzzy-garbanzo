from django.urls import path
from .views import PromoListView, PromoDetailView

app_name = 'promo'

urlpatterns = [
    path('', PromoListView.as_view(), name='promo_list'),
    path('<int:pk>/', PromoDetailView.as_view(), name='promo_detail'),
]
