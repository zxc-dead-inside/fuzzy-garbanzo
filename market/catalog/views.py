from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from elasticsearch.dsl.query import MultiMatch, Q

from .documents import ProductDocument
from .models import Category, Product


class CategoryListView(ListView):
    """List of categories"""
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 12

    def get_queryset(self):
        return Category.get_root_categories().prefetch_related('children')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Catalog'
        return context


class CategoryDetailView(DetailView):
    """Details of the category"""
    model = Category
    template_name = 'catalog/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Category.objects.filter(is_active=True).prefetch_related(
            'children')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['children'] = category.get_children()
        context['breadcrumbs'] = category.get_breadcrumbs()
        context['title'] = category.name
        return context


# JSON Views (простые, без DRF)
def category_json_list(request):
    """JSON list of categories"""
    categories = Category.get_root_categories()
    data = []

    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug,
            'description': category.description,
            'level': category.get_level(),
            'children_count': category.children.filter(is_active=True).count()
        })

    return JsonResponse({'categories': data})


def category_json_detail(request, category_id):
    """JSON details of the category"""
    category = get_object_or_404(Category, id=category_id, is_active=True)

    data = {
        'id': category.id,
        'name': category.name,
        'slug': category.slug,
        'description': category.description,
        'full_path': category.get_full_path(),
        'level': category.get_level(),
        'is_root': category.is_root(),
        'is_leaf': category.is_leaf(),
        'children': [
            {
                'id': child.id,
                'name': child.name,
                'slug': child.slug
            }
            for child in category.get_children()
        ]
    }

    return JsonResponse(data)


class ProductListView(ListView):
    """List of products with optional search"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            search = ProductDocument.search().query(
                Q("multi_match", query=query, fields=[
                    "name^3",
                    "name.autocomplete^5",
                    "description",
                    "description.autocomplete",
                    "category_name"
                ], type="best_fields")
            )
            product_ids = [hit.meta.id for hit in search[:1000]]
            return Product.objects.filter(
                id__in=product_ids).select_related('category')

        return Product.objects.filter(
            is_active=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products'
        context['query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    """Product detail page"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related(
            'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['title'] = product.name
        return context
