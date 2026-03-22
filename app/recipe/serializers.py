'''
Docstring for app.recipe.serializers
'''
from rest_framework import serializers
from core.models import Recipe, Tag,Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    '''Serializer for Ingredient objects'''

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    '''Serializer for Tag objects'''

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    '''Serializer for Recipe objects'''
    tags = TagSerializer(many=True, required=False)  # Add tags field
    ingredients = IngredientSerializer(many=True, required=False)  # Add ingredients field
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags','description', 'ingredients']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags_data, recipe):
        '''Handle getting or creating tags as needed'''
        auth_user = self.context['request'].user  # Get the authenticated user
        for tag in tags_data:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user, **tag)  # Get or create the tag
            recipe.tags.add(tag_obj)  # Add the tag to the recipe

    def _get_or_create_ingredients(self, ingredients_data, recipe):
        '''Handle getting or creating ingredients as needed'''
        auth_user = self.context['request'].user  # Get the authenticated user
        for ingredient in ingredients_data:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user, **ingredient)  # Get or create the ingredient
            recipe.ingredients.add(ingredient_obj)  # Add the ingredient to the recipe

    def create(self, validated_data):
        '''Create a recipe'''
        tags_data = validated_data.pop('tags', [])  # Get tags data if it exists
        ingerdients = validated_data.pop('ingredients', [])  # Get ingredients data if it exists
        recipe = Recipe.objects.create(**validated_data)  # Create the recipe
        self._get_or_create_tags(tags_data, recipe)  # Handle tags
        self._get_or_create_ingredients(ingerdients, recipe)  # Handle ingredients
        return recipe

    def update(self, instance, validated_data):
        '''Update a recipe'''
        tags_data = validated_data.pop('tags', None)  # Get tags data if it exists
        ingredients_data = validated_data.pop('ingredients', None)  # Get ingredients data if it exists
        if tags_data is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags_data, instance)

        if ingredients_data is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients_data, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class RecipeDetailSerializer(RecipeSerializer):
    '''Serializer for Recipe detail view'''

    class Meta(RecipeSerializer.Meta):
        # Now includes all fields from RecipeSerializer (including description)
        fields = RecipeSerializer.Meta.fields




