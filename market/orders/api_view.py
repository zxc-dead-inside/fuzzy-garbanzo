from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all().prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all().prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer
    lookup_field = 'id'
