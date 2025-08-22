from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Category
# Create your views here.

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = [
            {
                "id": p.id,
                "name": p.name,
                "quantity": p.qty,
                "category": p.cat.name
            } for p in products
        ]
        return Response(data)

class CategoryList(APIView):
    def get(self, request):
        cats = Category.objects.all()
        data = [
            {
                "id": c.id,
                "name": c.name,
                "description": c.desc
            } for c in cats
        ]
        return Response(data)