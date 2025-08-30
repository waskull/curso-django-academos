from rest_framework import serializers
from .models import Product, Category
import uuid
def formatDate():
    return serializers.DateTimeField(format="%Y/%m/%d %H:%M")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    created_at = formatDate()
    updated_at = formatDate()
    
class CategoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'desc')

class ProductSerializer(serializers.ModelSerializer):
    cat = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Product
        fields = ('id','created_at', 'updated_at', 'uuid', 'cat','name')

    created_at = formatDate()
    updated_at = formatDate()
    uuid = serializers.SerializerMethodField()

    def get_uuid(self, objj):
        return uuid.uuid4()
    
def formatDate():
    return serializers.DateTimeField(format="%Y/%m/%d %H:%M")

class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('price','name', 'qty', 'cat')