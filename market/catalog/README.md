# Catalog Module Documentation

## Overview

The Catalog module manages product categories and products for the market application.

## Models

### Category

The `Category` model represents a hierarchical tree of catalog categories.

#### Fields:
- `name`: The name of the category
- `slug`: URL-friendly unique identifier
- `parent`: Reference to parent category (optional)
- `description`: Detailed description of the category
- `image`: Category image
- `sort_order`: Position for ordering categories
- `is_active`: Flag to enable/disable the category (inherited from ActivatableMixin)
- `created`: Creation timestamp (inherited from TimeStampedMixin)
- `modified`: Last modification timestamp (inherited from TimeStampedMixin)

#### Key Methods:
- `get_children()`: Returns active child categories
- `get_all_children()`: Returns all child categories recursively
- `get_full_path()`: Returns the full hierarchical path of the category
- `get_level()`: Returns the nesting level of the category
- `is_root()`: Checks if the category is a root category
- `is_leaf()`: Checks if the category has no children
- `get_root()`: Returns the root category
- `get_siblings()`: Returns categories at the same level
- `get_breadcrumbs()`: Returns the breadcrumb navigation path
- `get_root_categories()`: Class method to get all root categories

### Product

The `Product` model represents items available for purchase.

#### Fields:
- `name`: The name of the product
- `slug`: URL-friendly unique identifier
- `category`: Reference to the product's category
- `description`: Detailed description of the product
- `price`: Product price
- `image`: Product image
- `spec_file`: Product specification file (optional)
- `image_preview`: Auto-generated thumbnail of the product image
- `is_active`: Flag to enable/disable the product (inherited from ActivatableMixin)
- `created`: Creation timestamp (inherited from TimeStampedMixin)
- `modified`: Last modification timestamp (inherited from TimeStampedMixin)

## Views

### Category Views

- `CategoryListView`: Displays a list of root categories
- `CategoryDetailView`: Displays details of a specific category including its children

### Product Views

- `ProductListView`: Displays a list of products with optional search functionality
- `ProductDetailView`: Displays detailed information about a specific product

### JSON Views

- `category_json_list`: Returns a JSON list of root categories
- `category_json_detail`: Returns detailed JSON data for a specific category

## Search Functionality

The catalog module includes Elasticsearch integration for product search:

- Products are indexed using the `ProductDocument` class
- Search is performed across product name, description, and category name
- The search functionality is integrated into the `ProductListView`

## URL Patterns

The catalog module provides the following URL patterns for web interfaces:

- `''` → `CategoryListView` (name: `category_list`): Displays the root categories list page
- `'category/<slug:slug>/'` → `CategoryDetailView` (name: `category_detail`): Displays a specific category and its children
- `'products/'` → `ProductListView` (name: `product_list`): Displays all products with search functionality
- `'products/<slug:slug>/'` → `ProductDetailView` (name: `product_detail`): Displays details of a specific product

## API Endpoints

The catalog module provides RESTful API endpoints for programmatic access:

### Category API Endpoints

- `'api/categories/'` → `CategoryListAPIView` (name: `api_category_list`): 
  - **Method**: GET
  - **Description**: Returns a list of all root categories with their children
  - **Response**: JSON array of category objects

- `'api/categories/<int:id>/'` → `CategoryDetailAPIView` (name: `api_category_detail`):
  - **Method**: GET
  - **Description**: Returns detailed information about a specific category by ID
  - **Response**: JSON object with category details

### Product API Endpoints

- `'api/products/'` → `ProductListAPIView` (name: `api_product_list`):
  - **Method**: GET
  - **Description**: Returns a list of all active products
  - **Filters**: Supports filtering through the `ProductFilter` class
  - **Response**: JSON array of product objects

- `'api/products/<int:id>/'` → `ProductDetailAPIView` (name: `api_product_detail`):
  - **Method**: GET
  - **Description**: Returns detailed information about a specific product by ID
  - **Response**: JSON object with product details

- `'api/products/export/'` → `ProductExportXLSAPIView` (name: `api_product_export`):
  - **Method**: POST
  - **Description**: Triggers an asynchronous task to export products to an Excel file
  - **Response**: JSON object with task_id for tracking the export process
  - **Implementation**: Uses Celery for background processing

## Templates

The module includes templates for:

- Category listing
- Category details
- Product listing
- Product details

## Integration with Other Modules

The catalog module integrates with:

- Orders module: Products can be added to orders
- Promotions module: Products can be part of promotional offers

## Admin Interface

The catalog module includes admin interfaces for managing:

- Categories (with hierarchical display)
- Products (with image previews)
