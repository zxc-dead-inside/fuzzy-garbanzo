# Orders Module Documentation

## Overview

The Orders module manages the creation, tracking, and processing of customer orders in the market application.

## Models

### Order

The `Order` model represents a customer order with its status and related items.

**Fields:**
- `status`: Current order status (draft, confirmed, shipped, completed, cancelled)
- `is_finalized`: Boolean flag indicating if the order is completed
- `created_at`: Timestamp when the order was created (from TimeStampedMixin)
- `updated_at`: Timestamp when the order was last updated (from TimeStampedMixin)

**Methods:**
- `total_sum()`: Calculates the total sum of all order items

### OrderItem

The `OrderItem` model represents individual products within an order.

**Fields:**
- `order`: Reference to the parent order
- `product`: Reference to the product being ordered
- `quantity`: Number of product units ordered
- `price`: Original price of the product (automatically set from product price)
- `promo_price`: Discounted price after applying promotions (optional)

**Methods:**
- `total_price`: Property that calculates the total price for the item (quantity × price)

## Views

### Web Views

- `OrderListView`: Displays a list of all orders, sorted by creation date
- `OrderDetailView`: Shows detailed information about a specific order
- `OrderCreateView`: Handles the creation of new orders with their items

### API Views

- `OrderListAPIView`: Returns a list of all orders with their items
- `OrderDetailAPIView`: Returns detailed information about a specific order

## Forms

- `OrderCreateForm`: Form for creating a new order
- `OrderItemInlineForm`: Form for adding items to an order
- `OrderItemFormSet`: Formset for handling multiple order items in a single form

## Services

### OrderService

The `OrderService` class provides business logic for order processing:

**Methods:**
- `create_order()`: Creates a new order with the specified items
- `apply_promos()`: Applies active promotions to order items
- `update_order_status()`: Updates the order status and handles finalization

## URL Patterns

### Web URLs

- `''` → `OrderListView` (name: `order_list`): Displays the list of all orders
- `'<int:pk>/'` → `OrderDetailView` (name: `order_detail`): Shows details of a specific order
- `'create/'` → `OrderCreateView` (name: `order_create`): Form for creating a new order

### API URLs

- `'api/orders/'` → `OrderListAPIView` (name: `api_order_list`): 
  - **Method**: GET
  - **Description**: Returns a list of all orders with their items
  - **Response**: JSON array of order objects

- `'api/orders/<int:id>/'` → `OrderDetailAPIView` (name: `api_order_detail`):
  - **Method**: GET
  - **Description**: Returns detailed information about a specific order
  - **Response**: JSON object with order details including items

## Order Creation Process

1. User fills out the order creation form with order items
2. The system validates the form data
3. A new order is created with status 'confirmed'
4. Order items are created with prices from the associated products
5. Promotions are applied to eligible items using `OrderService.apply_promos()`
6. The user is redirected to the order detail page

## Integration with Other Modules

- **Catalog Module**: Uses Product model for order items
- **Promo Module**: Applies promotions to order items through PromoEvaluator
