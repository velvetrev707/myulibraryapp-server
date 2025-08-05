"""
URL configuration for myulibraryappserver project.

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
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from rest_framework.routers import DefaultRouter
from universitylibrary.views import UserViewSet, BookViewSet, CheckoutViewSet
from universitylibrary.serializers import CustomTokenObtainPairSerializer

# Book Views
book_list = BookViewSet.as_view({'get': 'list','post': 'create'})
book_detail = BookViewSet.as_view({'get': 'retrieve'})
book_checkout = BookViewSet.as_view({'post': 'checkout'})

# User Views
user_list_create = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# Checkout Views
checkout_list = CheckoutViewSet.as_view({'get': 'list'})
checkout_return = CheckoutViewSet.as_view({'post': 'return_book'})

urlpatterns = [
    # Admin URL
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Book endpoints
    path('books/', book_list, name='book-list'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
    path('books/<int:pk>/checkout/', book_checkout, name='book-checkout'),

    # User endpoints
    path('users/', user_list_create, name='user-list'),

    # Checkout endpoints
    path('checkouts/', checkout_list, name='checkout-list'),
    path('checkouts/<int:pk>/return_book/', checkout_return, name='checkout-return'),
]
