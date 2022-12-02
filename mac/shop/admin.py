from django.contrib import admin
# Register your models here.
from .models import Product, Contact, Cart, Order, Customer

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(Order)


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city',
                    'zipcode', 'state']
