from django.contrib import admin
from baskets.models import Basket

# Register your models here.
class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    #readonly_fields = ('created_timestamp',)
    extra = 0
