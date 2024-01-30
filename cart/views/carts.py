from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.sessions.backends.db import SessionStore
from cart.models.carts import CartItems, Cart
from cart.serializers.carts import *
from cart.use_cases.carts import ListCartsUseCase

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    serializer_action_classes = {
        'create': CartSerializer,
        'create_item': CartItemsSerializer,
        'list': CartInlineItemsSerializer,
        'retrieve': CartInlineItemsSerializer,
        'update': CartSerializer,
    }

    def create(self, request, *args, **kwargs):
        session = SessionStore()
        session.create()
        session_token = session.session_key

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()
        mutable_data['cpf'] = str(mutable_data.get('cpf'))
        
        serializer = CartSerializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(session_token=session_token)

        Cart_serializer = CartInlineItemsSerializer(instance)
        return Response(Cart_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='cancel', permission_classes=[AllowAny])
    def cancel(self, request, pk=None):
        cart= self.get_object()

        if Cart.status == 'em aberto':
            Cart.status = 'cancelado'
            Cart.save()
            return Response({'message': 'cartstatus updated to "cancelado".'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Esse pedido não pode ser finalizado.'}, status=status.HTTP_400_BAD_REQUEST)

        
    def get_queryset(self):
        use_case = ListCartsUseCase()
        return use_case.execute(self.request)

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        cart = get_object_or_404(Cart, pk=pk)
        serializer = CartInlineItemsSerializer(cart)
        return Response(serializer.data)


    def partial_update(self, request, pk=None):
        instance = get_object_or_404(Cart, pk=pk, session_token=request.query_params.get('session'))
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CartInlineItemsSerializer
        return super().get_serializer_class()
    
    @action(detail=True, methods=['post'], url_path='checkout', permission_classes=[AllowAny])
    def checkout(self, request, pk=None):
        cart = Cart.objects.get(id=pk)
        print(cart)
        # Retrieve cart_items associated with the given cart_id
        cart_items = CartItems.objects.filter(cart=cart)
        print(cart_items)
        # Calculate the total amount by multiplying quantity by amount for each item
        total_amount = cart_items.aggregate(
            total=Sum(F('quantity') * F('product__amount'))
        )['total'] or 0

        return Response({'total_amount': total_amount , 'cart': cart.id}, status=status.HTTP_200_OK)
    

class CartItemsViewSet(viewsets.ModelViewSet):
    queryset = CartItems.objects.all()
    serializer_class = CartItemsSerializer
    permission_classes = (AllowAny,)

    serializer_action_classes = {
        'create': CartItemsWriteSerializer,
        'create_item': CartItemsSerializer,
        'list': CartInlineItemsSerializer,
        'retrieve': CartItemsSerializer,
        'update': CartItemsSerializer,

    }

    def create(self, request, *args, **kwargs):
        serializer_class = CartItemsWriteSerializer
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = serializer.validated_data['cart']
        cart_id = cart.id
       
        session = self.request.query_params.get('session')
        try:
            cart_check = Cart.objects.get(id=cart.id, session_token=session)
        except Cart.DoesNotExist:
            return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)

        instance = serializer.save(cart=cart)
        return Response(serializer.data, status=201)



    def delete(self, request, pk=None):

        return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)

    def retrieve(self, request, pk=None, *args, **kwargs):
        cart = get_object_or_404(cart, pk=pk)

        session = request.query_params.get('session')
        if cart.session_token != session:
            return Response({'error': 'Você não tem permissão para visualizar esse carrinho'}, status=403)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        cart = instance.cart

        session = request.query_params.get('session')
        if cart.session_token != session:
            return Response({'error': 'Você não tem permissão para editar esse carrinho'}, status=403)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)