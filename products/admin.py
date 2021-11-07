from django.contrib import admin
from products.models import ProductCategory, Product

# Register your models here.
admin.site.register(ProductCategory)
#admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category') # список полей для таблицы товаров 
    fields = ('name', ('price', 'quantity'), 'category', 'description', 'image') # список полей доступных для редактирования
    readonly_fields = ('quantity',) # редактирование запрещено
    ordering = ('name',) # порядок сортировки списка
    search_fields = ('name',)
