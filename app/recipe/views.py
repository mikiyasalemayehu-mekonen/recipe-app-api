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

class TagViewSet(
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    '''Manage tags in the database'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        '''Return objects for the current authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''Create a new tag'''
        serializer.save(user=self.request.user)
class IngredientViewSet(
    mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    '''Manage ingredients in the database'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        '''Return objects for the current authenticated user only'''
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        '''Create a new ingredient'''
        serializer.save(user=self.request.user)