import pytest

from market.catalog.models import Product, Category
from market.orders.models import Order, OrderItem


@pytest.mark.django_db
def test_order_total_sum():
    category = Category.objects.create(name="Test Category")
    product1 = Product.objects.create(name="Product 1", price=100,
                                      category=category, slug="product-1")
    product2 = Product.objects.create(name="Product 2", price=200,
                                      category=category, slug="product-2")

    order = Order.objects.create()
    OrderItem.objects.create(order=order, product=product1, quantity=2,
                             price=100)
    OrderItem.objects.create(order=order, product=product2, quantity=1,
                             price=200)

    assert order.total_sum() == 400
