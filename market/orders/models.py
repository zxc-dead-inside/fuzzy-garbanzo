from django.db import models

from market.catalog.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField('Status', max_length=20,
                              choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)
    is_finalized = models.BooleanField('Finished', default=False)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order #{self.pk} ({self.status})'

    def total_sum(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items', verbose_name='Order')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                verbose_name='Product')
    quantity = models.PositiveIntegerField('Quantity', default=1)
    price = models.DecimalField('Price', max_digits=10,
                                decimal_places=2, blank=True)
    promo_price = models.DecimalField('Promo Price', max_digits=10,
                                      decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Product in order'
        verbose_name_plural = 'Products in order'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    def save(self, *args, **kwargs):
        if self.product and self.price is None:
            self.price = self.product.price
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        price = self.promo_price if self.promo_price is not None else self.price
        if price is None or self.quantity is None:
            return 0
        return self.quantity * price
