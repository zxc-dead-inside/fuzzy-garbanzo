# Promo Module Documentation

## Overview

The Promo module manages promotional offers and discounts for products in the market application.

## Models

### Promo

The base `Promo` model represents different types of promotional offers.

**Fields:**
- `name`: Name of the promotion
- `description`: Detailed description of the promotion
- `promo_type`: Type of promotion (percent, n_for_m, fixed_price)
- `products`: Many-to-many relationship with Product model
- `discount_percent`: Percentage discount for percent type promos
- `n`: Number of items to buy in n_for_m type promos
- `m`: Number of items to pay for in n_for_m type promos
- `fixed_price`: Fixed price for a set of products in fixed_price type promos
- `start_date`: Optional start date for the promotion
- `end_date`: Optional end date for the promotion
- `created_at`: Timestamp when the promotion was created
- `is_active`: Flag to enable/disable the promotion (from ActivatableMixin)

**Methods:**
- `is_current()`: Checks if the promotion is currently active based on dates and active status

### Proxy Models

The module uses proxy models to specialize different types of promotions:

#### PercentPromo

A proxy model for percentage-based discounts.

#### NForMPromo

A proxy model for "Buy N, Pay for M" promotions (e.g., buy 3, pay for 2).

#### FixedPricePromo

A proxy model for fixed-price promotions for a set of products.

## Services

### PromoEvaluator

The `PromoEvaluator` class applies promotions to order items:

**Methods:**
- `apply()`: Applies all active promotions to order items
- `_apply_percent()`: Applies percentage discount promotions
- `_apply_n_for_m()`: Applies "Buy N, Pay for M" promotions
- `_apply_fixed_price()`: Applies fixed price promotions

## Views

### Web Views

- `PromoListView`: Displays a list of active promotions
- `PromoDetailView`: Shows detailed information about a specific promotion

### API Views

- `PromoListAPIView`: Returns a list of active promotions
- `PromoDetailAPIView`: Returns detailed information about a specific promotion

## URL Patterns

### Web URLs

- `''` → `PromoListView` (name: `promo_list`): Displays the list of active promotions
- `'<int:pk>/'` → `PromoDetailView` (name: `promo_detail`): Shows details of a specific promotion

### API URLs

- `'api/promos/'` → `PromoListAPIView` (name: `promo_list`): 
  - **Method**: GET
  - **Description**: Returns a list of all active promotions
  - **Response**: JSON array of promotion objects

- `'api/promos/<int:id>/'` → `PromoDetailAPIView` (name: `promo_detail`):
  - **Method**: GET
  - **Description**: Returns detailed information about a specific promotion
  - **Response**: JSON object with promotion details

## Promotion Types

### Percentage Discount

Applies a percentage discount to the product price.

**Example:** 20% off all selected products

### N-for-M Promotion

Customer buys N items but only pays for M items (where M < N).

**Example:** Buy 3, pay for 2

### Fixed Price Promotion

Sets a fixed price for a specific set of products when purchased together.

**Example:** Buy product A and product B together for a fixed price of $50

## Integration with Other Modules

- **Catalog Module**: References Product model for promotions
- **Orders Module**: Applies promotions to order items through the OrderService
