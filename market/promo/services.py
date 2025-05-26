class PromoEvaluator:
    def __init__(self, promos, order_items):
        self.promos = promos
        self.order_items = order_items

    def apply(self):
        for item in self.order_items:
            item.promo_price = None

        for promo in self.promos:
            if promo.promo_type == 'percent':
                self._apply_percent(promo)
            elif promo.promo_type == 'n_for_m':
                self._apply_n_for_m(promo)
            elif promo.promo_type == 'fixed_price':
                self._apply_fixed_price(promo)

        for item in self.order_items:
            item.save()

    def _apply_percent(self, promo):
        for item in self.order_items:
            if item.product in promo.products.all():
                discount = item.price * (promo.discount_percent / 100)
                item.promo_price = item.price - discount

    def _apply_n_for_m(self, promo):
        for item in self.order_items:
            if item.product in promo.products.all():
                n = promo.n
                m = promo.m
                if n and m and item.quantity >= n:
                    sets = item.quantity // n
                    paid_units = sets * m + item.quantity % n
                    item.promo_price = (item.price * paid_units)/item.quantity

    def _apply_fixed_price(self, promo):
        promo_products = set(promo.products.all())
        order_products = set(item.product for item in self.order_items)
        if promo_products.issubset(order_products):
            total_qty = sum(
                item.quantity
                for item in self.order_items
                if item.product in promo_products
            )
            for item in self.order_items:
                if item.product in promo_products:
                    item.promo_price = promo.fixed_price / total_qty
