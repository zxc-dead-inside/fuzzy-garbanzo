from django.views.generic import ListView, DetailView
from .models import Promo


class PromoListView(ListView):
    """Active promos list view."""
    model = Promo
    template_name = 'promo/promo_list.html'
    context_object_name = 'promos'

    def get_queryset(self):
        return Promo.objects.filter(is_active=True).order_by('-created_at')


class PromoDetailView(DetailView):
    model = Promo
    template_name = 'promo/promo_detail.html'
    context_object_name = 'promo'

    def get_queryset(self):
        return Promo.objects.filter(is_active=True)
