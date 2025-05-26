from django.urls import path
from . import api_view as views

urlpatterns = [
    path('orders/',
         views.OrderListAPIView.as_view(),
         name='api_order_list'),
    path('orders/<int:id>/',
         views.OrderDetailAPIView.as_view(),
         name='api_order_detail'),
]
