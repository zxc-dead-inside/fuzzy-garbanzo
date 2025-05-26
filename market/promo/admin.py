from django.contrib import admin
from .models import PercentPromo, NForMPromo, FixedPricePromo


@admin.register(PercentPromo)
class PercentPromoAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_percent', 'is_active',
                    'start_date', 'end_date']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    filter_horizontal = ['products']
    fields = ['name', 'description', 'discount_percent', 'products',
              'start_date', 'end_date', 'is_active']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(promo_type='percent')


@admin.register(NForMPromo)
class NForMPromoAdmin(admin.ModelAdmin):
    list_display = ['name', 'n', 'm', 'is_active', 'start_date', 'end_date']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    filter_horizontal = ['products']
    fields = ['name', 'description', 'n', 'm', 'products', 'start_date',
              'end_date', 'is_active']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(promo_type='n_for_m')


@admin.register(FixedPricePromo)
class FixedPricePromoAdmin(admin.ModelAdmin):
    list_display = ['name', 'fixed_price', 'is_active',
                    'start_date', 'end_date']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    filter_horizontal = ['products']
    fields = ['name', 'description', 'fixed_price', 'products', 'start_date',
              'end_date', 'is_active']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(promo_type='fixed_price')
