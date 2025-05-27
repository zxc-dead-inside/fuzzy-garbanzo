import pytest
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

from market.promo.models import Promo
from market.promo.services import PromoEvaluator
from market.catalog.models import Product, Category
from market.orders.models import Order, OrderItem


@pytest.mark.django_db
def test_is_current_active_promo():
    today = timezone.now().date()

    promo = Promo.objects.create(
        name="Black Friday",
        is_active=True,
        start_date=today - timedelta(days=1),
        end_date=today + timedelta(days=1)
    )

    assert promo.is_current() is True


@pytest.mark.django_db
def test_is_current_inactive_flag():
    today = timezone.now().date()

    promo = Promo.objects.create(
        name="Inactive promo",
        is_active=False,
        start_date=today - timedelta(days=1),
        end_date=today + timedelta(days=1)
    )

    assert promo.is_current() is False


@pytest.mark.django_db
def test_is_current_before_start():
    future_date = timezone.now().date() + timedelta(days=3)

    promo = Promo.objects.create(
        name="Feature promo",
        is_active=True,
        start_date=future_date,
        end_date=future_date + timedelta(days=5)
    )

    assert promo.is_current() is False


@pytest.mark.django_db
def test_is_current_after_end():
    past_date = timezone.now().date() - timedelta(days=5)

    promo = Promo.objects.create(
        name="Finished promo",
        is_active=True,
        start_date=past_date,
        end_date=past_date + timedelta(days=2)
    )

    assert promo.is_current() is False


@pytest.mark.django_db
def test_promo_evaluator_percent_discount():
    category = Category.objects.create(name="Test Category")
    product1 = Product.objects.create(
        name="Test Product 1",
        slug="test-product-1",
        price=Decimal("100.00"),
        category=category
    )
    product2 = Product.objects.create(
        name="Test Product 2",
        slug="test-product-2",
        price=Decimal("50.00"),
        category=category
    )

    # Create a percentage discount promo (20% off)
    promo = Promo.objects.create(
        name="20% Off Promo",
        promo_type="percent",
        discount_percent=Decimal("20.00"),
        is_active=True
    )
    promo.products.add(product1)  # Only apply to product1

    # Create an order with items
    order = Order.objects.create(status="draft")
    order_item1 = OrderItem.objects.create(
        order=order,
        product=product1,
        quantity=2,
        price=product1.price
    )
    order_item2 = OrderItem.objects.create(
        order=order,
        product=product2,
        quantity=1,
        price=product2.price
    )

    # Apply promotions
    evaluator = PromoEvaluator(
        promos=[promo], order_items=[order_item1, order_item2])
    evaluator.apply()

    order_item1.refresh_from_db()
    order_item2.refresh_from_db()

    assert order_item1.promo_price == Decimal("80.00")
    assert order_item2.promo_price is None


@pytest.mark.django_db
def test_promo_evaluator_n_for_m():
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(
        name="Test Product",
        slug="test-product",
        price=Decimal("10.00"),
        category=category
    )

    # Create a "Buy 3 Pay for 2" promo
    promo = Promo.objects.create(
        name="Buy 3 Pay for 2",
        promo_type="n_for_m",
        n=3,  # Buy 3
        m=2,  # Pay for 2
        is_active=True
    )
    promo.products.add(product)

    order = Order.objects.create(status="draft")

    # Case 1: Quantity exactly matches n (3)
    order_item1 = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=3,
        price=product.price
    )

    # Case 2: Quantity more than n with remainder
    # (7 = 2 sets of 3 + 1 remainder)
    order_item2 = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=7,
        price=product.price
    )

    # Apply promotions
    evaluator = PromoEvaluator(promos=[promo],
                               order_items=[order_item1, order_item2])
    evaluator.apply()

    order_item1.refresh_from_db()
    order_item2.refresh_from_db()

    # Verify results
    # For order_item1 (qty=3): Pay for 2 out of 3 items
    # Effective price per unit: (2 * 10) / 3 = 6.67
    assert order_item1.promo_price == Decimal("6.67")

    # For order_item2 (qty=7):
    # 2 complete sets (3+3=6) where we pay for 2+2=4 items
    # Plus 1 remainder item we pay full price for
    # Total paid: (4 * 10) + (1 * 10) = 50
    # Effective price per unit: 50 / 7 = 7.14
    assert order_item2.promo_price == Decimal("7.14")


@pytest.mark.django_db
def test_promo_evaluator_fixed_price():
    category = Category.objects.create(name="Test Category")
    product1 = Product.objects.create(
        name="Test Product 1",
        slug="test-product-1",
        price=Decimal("100.00"),
        category=category
    )
    product2 = Product.objects.create(
        name="Test Product 2",
        slug="test-product-2",
        price=Decimal("50.00"),
        category=category
    )
    product3 = Product.objects.create(
        name="Test Product 3",
        slug="test-product-3",
        price=Decimal("75.00"),
        category=category
    )

    # Create a fixed price promo (bundle of products for a fixed price)
    promo = Promo.objects.create(
        name="Bundle Deal",
        promo_type="fixed_price",
        fixed_price=Decimal("120.00"),  # Bundle price
        is_active=True
    )
    promo.products.add(product1, product2)

    # Create an order with all products
    order = Order.objects.create(status="draft")

    # Create order items - all with quantity 1 for simplicity
    order_item1 = OrderItem.objects.create(
        order=order,
        product=product1,
        quantity=1,
        price=product1.price
    )
    order_item2 = OrderItem.objects.create(
        order=order,
        product=product2,
        quantity=1,
        price=product2.price
    )
    order_item3 = OrderItem.objects.create(
        order=order,
        product=product3,
        quantity=1,
        price=product3.price
    )

    # Apply promotions
    evaluator = PromoEvaluator(
        promos=[promo], order_items=[order_item1, order_item2, order_item3]
    )
    evaluator.apply()

    # Refresh from database
    order_item1.refresh_from_db()
    order_item2.refresh_from_db()
    order_item3.refresh_from_db()

    # Verify results
    # The fixed price (120) should be distributed evenly between the items in
    # the promo
    # Total quantity of bundle items: 1 + 1 = 2
    # Price per item: 120 / 2 = 60
    assert order_item1.promo_price == Decimal("60.00")
    assert order_item2.promo_price == Decimal("60.00")
    # Product3 is not part of the bundle, so no discount
    assert order_item3.promo_price is None
