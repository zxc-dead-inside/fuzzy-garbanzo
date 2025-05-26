from market.promo.services import PromoEvaluator
from market.promo.models import Promo
from .models import Order, OrderItem
from django.db import transaction


class OrderService:
    def __init__(self, order=None):
        self.order = order or Order()

    @transaction.atomic
    def create_order(self, items_data, status='draft'):
        """
        items_data — list of dict with keys: product (instance), quantity (int)
        """
        self.order.status = status
        self.order.save()

        self.order.items.all().delete()

        for item_data in items_data:
            OrderItem.objects.create(
                order=self.order,
                product=item_data['product'],
                quantity=item_data.get('quantity', 1)
            )

        self.apply_promos()

        return self.order

    def apply_promos(self):
        active_promos = Promo.objects.filter(is_active=True)
        order_items = self.order.items.select_related('product').all()
        evaluator = PromoEvaluator(active_promos, order_items)
        evaluator.apply()

    @transaction.atomic
    def update_order_status(self, status):
        self.order.status = status
        if status == 'completed':
            self.order.is_finalized = True
        self.order.save()
