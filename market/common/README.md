# Common Module Documentation

## Overview

The Common module provides shared functionality, mixins, and utilities used across the market application.

## Models

### Abstract Mixins

The module provides abstract model mixins that can be reused across different models in the application:

#### TimeStampedMixin

Adds timestamp fields to track when records are created and updated.

**Fields:**
- `created_at`: Automatically set when a record is created
- `updated_at`: Automatically updated whenever a record is modified


#### ActivatableMixin

Adds a boolean field to indicate if a record is active or not, useful for soft deletion or temporarily disabling records.

**Fields:**
- `is_active`: Boolean field, defaults to True

## Tasks

The Common module includes Celery tasks for background processing:

### Exchange Rate Synchronization

**File:** `tasks/exchange.py`

**Task:** `sync_exchange_rates_task`

**Description:** Fetches the latest exchange rates from the ExchangeRate API and logs the USD to RUB conversion rate.

**Implementation Details:**
- Uses the ExchangeRate API (v6)
- Requires an API key configured in settings (`EXCHANGERATE_API_KEY`)
- Logs the USD to RUB exchange rate
- Handles exceptions and logs errors

## Management Commands

The Common module provides custom Django management commands:

### sync_exchange_rates

**File:** `management/commands/sync_exchange_rates.py`

**Description:** A Django management command to manually sync exchange rates from the ExchangeRate API.

**Usage:**
```bash
python manage.py sync_exchange_rates
```

**Implementation Details:**
- Fetches the latest USD to RUB exchange rate
- Displays the result in the console
- Uses the same API as the Celery task
