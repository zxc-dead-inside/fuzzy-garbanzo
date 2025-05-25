from rest_framework import serializers
from .models import Category


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
