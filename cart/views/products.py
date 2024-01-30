from rest_framework.permissions import AllowAny
from rest_framework import viewsets, mixins
from cart.models.products import Product
from cart.serializers.products import *
from cart.use_cases.products import ListProductsUseCase

class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.using('default').all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    
    
    def get_queryset(self):
        list_products_use_case = ListProductsUseCase()
        return list_products_use_case.execute(self.request.query_params)
