from cart.models import Cart
from rest_framework import status
from django.db.models import Case, When, IntegerField, Value
from cart.serializers.carts import *

class ListCartsUseCase:
    def execute(self, request):
        status = request.query_params.get('status', None)

        # Query the Cart model directly
        queryset = Cart.objects.all()
        print(f'listagem dentro de usecase{queryset}')
        if request.query_params.get('session'):
            queryset = queryset.filter(session_token=request.query_params.get('session'))

        if status:
            queryset = queryset.filter(status=status)

        # Apply custom Carting
        return queryset

 