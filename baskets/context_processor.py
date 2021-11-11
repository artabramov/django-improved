from baskets.models import Basket

def basket(request):
    """
    Basket context processor.
    """
    if request.user.is_authenticated:
        result = {'baskets': Basket.objects.filter(user=request.user),}

    else:
        result = {'baskets': []}

    return result
