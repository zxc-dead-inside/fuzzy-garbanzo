from rest_framework import generics
from .models import Promo
from .serializers import PromoSerializer


class PromoListAPIView(generics.ListAPIView):
    serializer_class = PromoSerializer

    def get_queryset(self):
        return Promo.objects.filter(is_active=True).order_by('-created_at')


class PromoDetailAPIView(generics.RetrieveAPIView):
    serializer_class = PromoSerializer
    queryset = Promo.objects.filter(is_active=True)
    lookup_field = 'id'
