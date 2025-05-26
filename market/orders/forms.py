from django import forms
from django.forms import inlineformset_factory

from .models import OrderItem, Order


class OrderItemInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemInlineForm,
    fields=('product', 'quantity'),
    extra=1,
    can_delete=False
)
