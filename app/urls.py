"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chatbot.views import ChatbotView,ConversationHistoryView, ConversationDetailView
from inventario.views import ProductList, CategoryList, ProductDetailView, CategoryDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
     path('chat/', ChatbotView.as_view(), name='chatbot'),
    path('conversations/', ConversationHistoryView.as_view(), name='conversation-history'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('api/product/', ProductList.as_view(), name="product-list"),
    path('api/product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/category/', CategoryList.as_view(), name="category-list"),
    path('api/category/<int:pk>/', CategoryDetailView.as_view(), name='product-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
