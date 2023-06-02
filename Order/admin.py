# Modules
from django.contrib import admin



# Models
from Order.models import *



# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['amount_payable', 'is_paid', 'razorpay_order_id', 'user']
admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'address', 'is_a_replacement', 'order']
admin.site.register(OrderItem, OrderItemAdmin)