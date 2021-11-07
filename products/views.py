from django.core import paginator
from django.shortcuts import render
from products.models import ProductCategory, Product
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    context = {
        'title': 'Geekshop - Главная страница',
        'description': 'Описание главное страницы'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):

    if category_id:
        category = ProductCategory.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 3) # arg 2 - items per page

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'Geekshop - Каталог товаров',
        'description': 'Описание каталога товаров',
        'products': products_paginator,
        'categories': ProductCategory.objects.all(),
    }

    return render(request, 'products/products.html', context)
