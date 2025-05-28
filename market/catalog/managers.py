from django.db import models
from django.utils.timezone import now

class ProductQuerySet(models.QuerySet):
    def with_active_promos(self):
        today = now().date()
        return self.filter(
            promos__is_active=True,
        ).filter(
            models.Q(promos__start_date__isnull=True) |
            models.Q(promos__start_date__lte=today),
            models.Q(promos__end_date__isnull=True) |
            models.Q(promos__end_date__gte=today)
        ).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def with_active_promos(self):
        return self.get_queryset().with_active_promos()

    def best_in_category(self, category):
        """Return the cheapest product in a given category."""""
        return self.filter(
            is_active=True,
            category=category
        ).order_by('price').first()
