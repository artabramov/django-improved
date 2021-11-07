from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import response

import products
from products.models import Product
from baskets.models import Basket

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)

    else:
        basket = baskets.first()
        if basket.quantity < product.quantity:
            basket.quantity += 1
            basket.save()

    #return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return response.JsonResponse({'success': 'true'})


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_edit(request, basket_id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=basket_id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        #context = {'baskets': baskets}
        context = {}
        result = render_to_string('baskets/baskets.html', context)
        return response.JsonResponse({'result': result})
