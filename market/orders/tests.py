import pytest
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

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


@pytest.mark.django_db
def test_order_list_api():
    user = get_user_model().objects.create_user(
        email='example@example.com',
        password='testpass',
    )
    client = APIClient()
    client.login(
        email='example@example.com',
        password='testpass',
    )
    category = Category.objects.create(name="API Test Category")

    product1 = Product.objects.create(
        name="API Product 1",
        price=Decimal("50.00"),
        category=category,
        slug="api-product-1"
    )
    product2 = Product.objects.create(
        name="API Product 2",
        price=Decimal("75.00"),
        category=category,
        slug="api-product-2"
    )

    order1 = Order.objects.create(status="confirmed")
    OrderItem.objects.create(
        order=order1,
        product=product1,
        quantity=2,
        price=product1.price
    )

    order2 = Order.objects.create(status="draft")
    OrderItem.objects.create(
        order=order2,
        product=product2,
        quantity=1,
        price=product2.price
    )

    url = reverse('api_order_list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

    # Verify order data is correct
    orders_data = response.data
    assert any(order['id'] == order1.id for order in orders_data)
    assert any(order['id'] == order2.id for order in orders_data)

    order1_data = next(order for order in orders_data
                       if order['id'] == order1.id)
    assert order1_data['status'] == 'confirmed'
    assert order1_data['total_sum'] == 100.0


@pytest.mark.django_db
def test_order_detail_api():
    client = APIClient()
    user = get_user_model().objects.create_user(
        email='example@example.com',
        password='testpass',
    )
    client.login(
        email='example@example.com',
        password='testpass',
    )
    category = Category.objects.create(name="Detail API Test Category")

    product1 = Product.objects.create(
        name="Detail API Product 1",
        price=Decimal("120.00"),
        category=category,
        slug="detail-api-product-1"
    )
    product2 = Product.objects.create(
        name="Detail API Product 2",
        price=Decimal("80.00"),
        category=category,
        slug="detail-api-product-2"
    )

    order = Order.objects.create(status="confirmed")
    item1 = OrderItem.objects.create(
        order=order,
        product=product1,
        quantity=1,
        price=product1.price
    )
    item2 = OrderItem.objects.create(
        order=order,
        product=product2,
        quantity=3,
        price=product2.price
    )

    url = reverse('api_order_detail', kwargs={'id': order.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    order_data = response.data
    assert order_data['id'] == order.id
    assert order_data['status'] == 'confirmed'
    assert order_data['total_sum'] == 360.0

    assert len(order_data['items']) == 2

    item1_data = next(item for item in order_data['items']
                      if item['id'] == item1.id)
    assert item1_data['product'] == product1.id
    assert item1_data['product_name'] == product1.name
    assert item1_data['quantity'] == 1
    assert float(item1_data['price']) == 120.0
    assert float(item1_data['total_price']) == 120.0

    item2_data = next(item for item in order_data['items']
                      if item['id'] == item2.id)
    assert item2_data['product'] == product2.id
    assert item2_data['product_name'] == product2.name
    assert item2_data['quantity'] == 3
    assert float(item2_data['price']) == 80.0
    assert float(item2_data['total_price']) == 240.0
