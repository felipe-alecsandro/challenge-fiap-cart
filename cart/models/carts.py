from django.db import models
import os
import re
from cart.models.products import Product

class Cart(models.Model):
    session_token = models.CharField(max_length=255, blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name="criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="atualizado em", null=True, blank=True,)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

    def __str__(self):
        return f"{self.id}"

 
    def save(self,*args,**kwargs):
        kwargs['using'] = 'default'
        return super().save(*args,**kwargs)


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='pedido',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='produto',
                             on_delete=models.CASCADE)
    quantity = models.IntegerField()
    changes = models.TextField(max_length=300,verbose_name="alteracoes", null=True, blank=True,)


    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'

    def __str__(self):
        return f"{self.cart}"

 
    def save(self,*args,**kwargs):
        kwargs['using'] = 'default'
        return super().save(*args,**kwargs)


