from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry
from market.catalog.models import Product

product_index = Index('products')
product_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@registry.register_document
class ProductDocument(Document):
    category_name = fields.TextField(attr='category.name')

    class Index:
        name = 'products'

    class Django:
        model = Product
        fields = [
            'name',
            'description',
        ]
