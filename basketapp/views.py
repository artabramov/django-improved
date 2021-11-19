from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import F
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.urls.base import reverse
from mainapp.models import Product

from basketapp.models import Basket


@login_required
def basket(request):
    title = "корзина"
    basket_items = Basket.objects.filter(user=request.user).order_by("product__category")
    content = {"title": title, "basket_items": basket_items, "media_url": settings.MEDIA_URL}
    return render(request, "basketapp/basket.html", content)


@login_required
def basket_add(request, pk):
    if "login" in request.META.get("HTTP_REFERER"):
        return HttpResponseRedirect(reverse("products:product", args=[pk]))
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    if product.quantity != 0:
        basket.quantity = F("quantity") + 1
        basket.save()
    else:
        print('Превышено количество на складе')

    # update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
    # print(f'query basket_add: {update_queries}')

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        try:
            pk = int(pk)
            quantity = int(quantity)
        except Exception as exp:
            print(f"Wrong input numbers! {exp}")
            raise exp
        new_basket_item = Basket.objects.get(pk=pk)
        product = get_object_or_404(Product, pk=new_basket_item.product_id)

        # Проверяем что товар еще есть на складе, или что уменьшаем количество.
        if product.quantity > 0 or new_basket_item.quantity > quantity:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            print('превышено количество на складе')
        if quantity == 0:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by("product__category")

        content = {
            "basket_items": basket_items,
            "media_url": settings.MEDIA_URL,
        }

        result = render_to_string("basketapp/includes/inc_basket_list.html", content)

        return JsonResponse({"result": result})