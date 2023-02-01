from django.db import models
from main.models import Product
from django.shortcuts import get_object_or_404


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cost = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.title}"


class Cart(models.Model):
    products = models.ManyToManyField(CartProduct, blank=True)
    total_quantity = models.IntegerField(default=0)
    total_cost = models.IntegerField(default=0)
    
    def add_product(self, product_id: int, qty: int):
        product_id = int(product_id)
        qty = int(qty)
        product = get_object_or_404(Product, id=product_id)
        if qty < 1:
            qty = 1
        cost = qty * product.get_cost()
        self.total_quantity += qty
        self.total_cost += cost
        self.products.create(product=product, quantity=qty, cost=cost)
        self.save()
        return True
    
    def __str__(self):
        return f"CARD ID: {self.id}"