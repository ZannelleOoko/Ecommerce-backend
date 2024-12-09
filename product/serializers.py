from rest_framework import serializers
from .models import Product, Category

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=(
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail"

        )

class CategorySerializer(serializers.ModelSerializer):
    products=ProductSerializer(many=True)  #this is used to get all the products from ProductSerializer, then stored in the product variable
    class Meta:
        model= Category
        fields=(
            "id",
            "name",
            "get_absolute_url",
            "products"
        )

        