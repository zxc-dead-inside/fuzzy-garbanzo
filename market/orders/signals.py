from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_created_handler(sender, instance, created, **kwargs):
    if created:
        # imitation of sending an emai
        logger.info(
            f"Your order {instance.id} has been created. "
            f"Please check your email for further instructions."
        )
