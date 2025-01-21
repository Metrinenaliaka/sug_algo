from rest_framework import serializers
from .models import Product, Interaction, UserPreferences


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'description', 'image', 'created_at', 'updated_at']


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['user', 'product', 'interaction_type', 'interaction_count', 'created_at']


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['user', 'preferred_product_type', 'preferred_description', 'interaction_count', 'created_at', 'updated_at']
