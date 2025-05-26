from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product


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
                    'image_preview', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'price']
    readonly_fields = ['image_preview']
    ordering = ['name', 'price']

    fieldsets = (
        ('Main info', {
            'fields': ('name', 'slug', 'category', 'description', 'price')
        }),
        ('Media', {
            'fields': ('image', 'image_preview', 'spec_file')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>',
                               obj.image.url)
        return "—"
    image_preview.short_description = 'Preview image'
