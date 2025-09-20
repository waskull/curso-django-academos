from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category
#from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, CategorySerializer, ProductPostSerializer, CategoryPostSerializer
# Create your views here.

class ProductList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        products = Product.objects.all()
        name = request.query_params.get('name', None)
        if name:
            products = products.filter(name__icontains=name)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def post(self, request):
        serializer = ProductPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cats = Category.objects.all()
        serializer = CategorySerializer(cats, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CategoryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        print(dir(product))
        if product is None:
            return Response(
                {"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product)
        #print(dir(serializer))
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(
                {"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductPostSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(
                {"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response({"message":"El producto fue eliminado"})
    
class CategoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(
                {"error": "Categoria no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(
                {"error": "Categoria no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategoryPostSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(
                {"error": "Categoria no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response({"message":"La categoria fue eliminada"})