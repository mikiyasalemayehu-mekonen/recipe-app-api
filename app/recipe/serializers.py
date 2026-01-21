'''
Docstring for app.recipe.serializers
'''
from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    '''Serializer for Recipe objects'''

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'description']  # Add description here
        read_only_fields = ['id']

class RecipeDetailSerializer(RecipeSerializer):
    '''Serializer for Recipe detail view'''

    class Meta(RecipeSerializer.Meta):
        # Now includes all fields from RecipeSerializer (including description)
        fields = RecipeSerializer.Meta.fields