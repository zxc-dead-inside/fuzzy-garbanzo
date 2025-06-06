from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now
from django.db import models


from .models import Category, Product


class HasActivePromoFilter(admin.SimpleListFilter):
    title = 'Active promos'
    parameter_name = 'has_active_promo'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'With promo'),
            ('no', 'Withouth promo'),
        ]

    def queryset(self, request, queryset):
        today = now().date()
        if self.value() == 'yes':
            return queryset.filter(
                promos__is_active=True,
            ).filter(
                models.Q(promos__start_date__isnull=True) | models.Q(
                    promos__start_date__lte=today),
                models.Q(promos__end_date__isnull=True) | models.Q(
                    promos__end_date__gte=today)
            ).distinct()
        elif self.value() == 'no':
            return queryset.exclude(
                promos__is_active=True,
            ).distinct()
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'sort_order', 'created_at',
                    'products_count']
    list_filter = ['is_active', 'created_at', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'sort_order']
    ordering = ['sort_order', 'name']

    fieldsets = (
        ('Info', {
            'fields': ('name', 'slug', 'parent', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Options', {
            'fields': ('is_active', 'sort_order')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')

    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = 'Products count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active',
                    'admin_image_preview', 'created_at']
    list_filter = [HasActivePromoFilter, 'is_active', 'category', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'price']
    readonly_fields = ['admin_image_preview']
    ordering = ['name', 'price']

    fieldsets = (
        ('Main info', {
            'fields': ('name', 'slug', 'category', 'description', 'price')
        }),
        ('Media', {
            'fields': ('image', 'admin_image_preview', 'spec_file')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def admin_image_preview(self, obj):
        if obj.image_preview:
            return format_html(
                '<img src="{}" style="max-height: 50px;" />',
                obj.image_preview.url
            )
        return "—"

    admin_image_preview.short_description = 'Preview image'
