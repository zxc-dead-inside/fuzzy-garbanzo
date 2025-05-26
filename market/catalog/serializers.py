from rest_framework import serializers
from .models import Category, Product


class CategoryChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    children = CategoryChildSerializer(
        many=True, read_only=True, source='get_children'
    )
    level = serializers.SerializerMethodField()
    is_root = serializers.SerializerMethodField()
    is_leaf = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'description',
            'level', 'is_root', 'is_leaf', 'children'
        )

    def get_level(self, obj):
        return obj.get_level()

    def get_is_root(self, obj):
        return obj.is_root()

    def get_is_leaf(self, obj):
        return obj.is_leaf()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name', read_only=True
    )
    image_url = serializers.SerializerMethodField()
    spec_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_name',
            'description', 'price', 'image_url', 'spec_file_url',
            'is_active', 'created_at', 'updated_at'
        ]

    def get_image_url(self, obj):
        return obj.image.url if obj.image else None

    def get_spec_file_url(self, obj):
        return obj.spec_file.url if obj.spec_file else None
