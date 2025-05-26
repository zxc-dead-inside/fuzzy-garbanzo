from django.db import models
from market.catalog.models import Product


class Promo(models.Model):
    """Base class for proxy promo models."""
    PROMO_TYPE_CHOICES = [
        ('percent', 'Percentage discount'),
        ('n_for_m', 'Buy N — Pay for M'),
        ('fixed_price', 'Fixed price for product set'),
    ]

    name = models.CharField('Promo name', max_length=255)
    description = models.TextField('Description', blank=True)
    promo_type = models.CharField(
        'Promo type',
        max_length=20,
        choices=PROMO_TYPE_CHOICES,
        default='percent'
    )

    products = models.ManyToManyField(
        Product,
        related_name='promos',
        verbose_name='Products in promo'
    )

    # Percentage type
    discount_percent = models.DecimalField(
        'Discount (%)',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='E.g., 10 for 10% off'
    )

    # "Buy N - pay for M" type
    n = models.PositiveIntegerField('Buy N', null=True, blank=True)
    m = models.PositiveIntegerField('Pay for M', null=True, blank=True)

    # Fixed price type
    fixed_price = models.DecimalField(
        'Fixed price',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_active = models.BooleanField('Active', default=True)
    start_date = models.DateField('Start date', null=True, blank=True)
    end_date = models.DateField('End date', null=True, blank=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Promo'
        verbose_name_plural = 'Promos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'start_date', 'end_date']),
        ]

    def __str__(self):
        return self.name

    def is_current(self):
        from django.utils.timezone import now
        today = now().date()
        if self.start_date and today < self.start_date:
            return False
        if self.end_date and today > self.end_date:
            return False
        return self.is_active


class PercentPromo(Promo):
    class Meta:
        proxy = True
        verbose_name = 'Percent Promo'
        verbose_name_plural = 'Percent Promos'

    def save(self, *args, **kwargs):
        self.promo_type = 'percent'
        super().save(*args, **kwargs)


class NForMPromo(Promo):
    class Meta:
        proxy = True
        verbose_name = 'N-for-M Promo'
        verbose_name_plural = 'N-for-M Promos'

    def save(self, *args, **kwargs):
        self.promo_type = 'n_for_m'
        super().save(*args, **kwargs)


class FixedPricePromo(Promo):
    class Meta:
        proxy = True
        verbose_name = 'Fixed Price Promo'
        verbose_name_plural = 'Fixed Price Promos'

    def save(self, *args, **kwargs):
        self.promo_type = 'fixed_price'
        super().save(*args, **kwargs)
