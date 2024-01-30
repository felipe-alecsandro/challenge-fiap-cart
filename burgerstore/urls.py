"""
URL configuration for burgerstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import routers
from cart.views import CartViewSet, ProductViewSet, CartItemsViewSet

router = routers.DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('products', ProductViewSet, basename='products')
router.register('items', CartItemsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('cart_retrieve/<int:pk>/', CartViewSet.retrieve, name='cart_retrieve'),
    # path('cart_create/', cart_create, name='cart_create'),
    # path('cart_retrieve/<int:pk>/', cart_retrieve, name='cart_retrieve'),
]
