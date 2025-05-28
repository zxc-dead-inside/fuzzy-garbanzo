import requests
from celery import shared_task
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def sync_exchange_rates_task():
    api_key = settings.EXCHANGERATE_API_KEY
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        rate_rub = data["conversion_rates"].get("RUB")

        if rate_rub:
            logger.info(f"[USD → RUB] {rate_rub:.2f}")
        else:
            logger.warning("RUB rate not found in conversion_rates")

    except Exception as e:
        logger.error(f"Exchange rate fetch failed: {e}")
