from django.db.models import fields
from rest_framework import serializers
from cart.serializers.products import ProductSerializer
from cart.models.carts import CartItems, Cart

class CartItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)   

    class Meta:
        model = CartItems
        fields = ('id', 'cart', 'product', 'quantity', 'changes')  

class CartItemsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'      

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


  

class CartInlineItemsSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()  # Use SerializerMethodField for custom serialization
    
    class Meta:
        model = Cart
        fields = [
            'id',
            'session_token',
            'cpf',
            'created_at',
            'updated_at',
            'item'
        ]

    def get_item(self, obj):
        # Define custom method to serialize related CartItem objects
        cart_items = CartItems.objects.filter(cart=obj)  # Fetch related CartItem objects
        serializer = CartItemsSerializer(cart_items, many=True)  # Serialize related CartItem objects
        return serializer.data  # Return serialized data