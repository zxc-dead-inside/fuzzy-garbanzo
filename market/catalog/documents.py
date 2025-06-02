from django_elasticsearch_dsl import Document, fields, Index
from django_elasticsearch_dsl.registries import registry
from market.catalog.models import Product

product_index = Index('products')
product_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        "filter": {
            "ngram_filter": {
                "type": "edge_ngram",
                "min_gram": 2,
                "max_gram": 20
            },
            "english_stop": {
                "type": "stop",
                "stopwords": "_english_"
            },
            "english_stemmer": {
                "type": "stemmer",
                "language": "english"
            }
        },
        "analyzer": {
            "autocomplete": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase", "ngram_filter"]
            },
            "autocomplete_search": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase"]
            },
            "english_morphology": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase", "english_stop", "english_stemmer"]
            }
        }
    }
)



@registry.register_document
class ProductDocument(Document):
    category_name = fields.TextField(attr='category.name')

    name = fields.TextField(
        analyzer='english_morphology',
        fields={
            'autocomplete': fields.TextField(
                analyzer='autocomplete',
                search_analyzer='autocomplete_search'
            )
        }
    )

    description = fields.TextField(
        analyzer='english_morphology',
        fields={
            'autocomplete': fields.TextField(
                analyzer='autocomplete',
                search_analyzer='autocomplete_search'
            )
        }
    )

    class Index:
        name = 'products'
        settings = product_index._settings

    class Django:
        model = Product
        fields = []
