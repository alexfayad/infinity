from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, ProductType, Link, MapSubcategory, FAQContent,Wishlist


class ProductSerializer(serializers.ModelSerializer):
    sex = serializers.CharField(source="link.sex")

    class Meta:
        model = Product
        fields = "__all__"


class ProductTypeSerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField(many=True)

    class Meta:
        model = ProductType
        fields = ('name', 'subcategories')


class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'url', 'link_type', 'shop_name', 'sex')


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class MapSubcategoriesSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="subcategory.id")

    class Meta:
        model = MapSubcategory
        fields = ("name", "category_id")


class FAQContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQContent
        exclude = ['id']

class WishListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Wishlist
        fields = ['id','product']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


