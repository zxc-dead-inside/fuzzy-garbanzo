from django.db import models


class TimeStampedMixin(models.Model):
    """Add timestamps to the model"""
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        abstract = True


class ActivatableMixin(models.Model):
    """Add a boolean field to indicate if the object is active"""
    is_active = models.BooleanField('Active', default=True)

    class Meta:
        abstract = True
