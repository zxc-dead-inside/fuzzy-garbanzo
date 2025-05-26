from django.contrib import admin

from .forms import OrderItemInlineForm
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemInlineForm
    extra = 0
    readonly_fields = ['total_price']
    autocomplete_fields = ['product']
    fields = ['product', 'quantity', 'price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'is_finalized', 'created_at',
                    'updated_at', 'total_sum_display']
    list_filter = ['status', 'is_finalized', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'total_sum_display']
    inlines = [OrderItemInline]
    ordering = ['-created_at']

    fieldsets = (
        ('Main info', {
            'fields': ('status', 'is_finalized')
        }),
        ('System fields', {
            'fields': ('created_at', 'updated_at', 'total_sum_display')
        }),
    )

    def total_sum_display(self, obj):
        return f"{obj.total_sum():.2f} ₽"
    total_sum_display.short_description = 'Total amount'
