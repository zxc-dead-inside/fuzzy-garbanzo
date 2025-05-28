import requests
from django.core.management.base import BaseCommand

from django.conf import settings


class Command(BaseCommand):
    help = "Sync exchange rates from open API"

    def handle(self, *args, **kwargs):
        url = (f"https://v6.exchangerate-api.com/v6/"
               f"{settings.EXCHANGERATE_API_KEY}/latest/USD")
        response = requests.get(url)
        data = response.json()
        rate_rub = data["conversion_rates"].get("RUB")

        if rate_rub:
            self.stdout.write(self.style.SUCCESS(f"USD → RUB: {rate_rub:.2f}"))
        else:
            self.stdout.write(self.style.ERROR("RUB rate not found"))
