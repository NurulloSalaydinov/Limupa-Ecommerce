import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Cart, CartProduct



def get_request_cart(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
    except:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart


def add_to_cart(request):
    d = request.body
    data = json.loads(d)
    product_id = int(data.get('product_id'))
    quantity = int(data.get('qty'))
    cart = get_request_cart(request)
    for product in cart.products.all():
        if product.product.id == product_id:
            cost = product.product.get_cost() * quantity
            product.quantity += quantity
            product.cost += cost
            cart.total_quantity += quantity
            cart.total_cost += cost
            product.save()
            cart.save()
            return JsonResponse({'status': 200})
        # print(product.product.id)
        # print('fetched', product_id)
    cart.add_product(product_id, quantity)
    return JsonResponse({'status': 200})



