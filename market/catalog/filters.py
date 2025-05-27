import django_filters
from django.db import models
from django.utils.timezone import now
from .models import Product


class HasActivePromoAPIFilter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        if value is None:
            return qs

        today = now().date()
        if value:
            return qs.filter(
                promos__is_active=True,
            ).filter(
                models.Q(promos__start_date__isnull=True) |
                models.Q(promos__start_date__lte=today),
                models.Q(promos__end_date__isnull=True) |
                models.Q(promos__end_date__gte=today)
            ).distinct()
        return qs.exclude(
            promos__is_active=True,
        ).distinct()


class ProductFilter(django_filters.FilterSet):
    has_active_promo = HasActivePromoAPIFilter(
        field_name='promos',
        label='Has active promotion'
    )

    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'category': ['exact'],
            'is_active': ['exact'],
            'price': ['gt', 'gte', 'lt', 'lte', 'exact'],
        }
