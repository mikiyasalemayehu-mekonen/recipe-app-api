'''
Docstring for app.recipe.views
'''
from rest_framework import (
        viewsets,
        mixins,
        permissions)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import (
    Recipe,
    Tag,
    Ingredient
)
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    '''ViewSet for managing Recipe APIs'''
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''Return recipes for the authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        '''Return appropriate serializer class'''
        if self.action == 'retrieve':  # Changed from 'list' to 'retrieve'
            return serializers.RecipeDetailSerializer
        return self.serializer_class
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BaseRecipeAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    '''Base view set for managing recipe attributes'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        '''Return objects for the current authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

class TagViewSet(BaseRecipeAttrViewSet):
    '''Manage tags in the database'''

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer



    def perform_create(self, serializer):
        '''Create a new tag'''
        serializer.save(user=self.request.user)
class IngredientViewSet(BaseRecipeAttrViewSet):
    '''Manage ingredients in the database'''

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer



    def perform_create(self, serializer):
        '''Create a new ingredient'''
        serializer.save(user=self.request.user)