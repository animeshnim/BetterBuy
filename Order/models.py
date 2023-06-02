# Import Models
from email import message
from django.db import models
from Base.models import *
from Account.models import *
from Catalogue.models import Product




# Choices
ORDER_ITEM_STATUS_TYPE_CHOICES = (
    ('Order Placed', 'Order Placed'),
    ('Shipped', 'Shipped'),
    ('Out For Delivery', 'Out For Delivery'),
    ('Delivered', 'Delivered'),
)


# Create your models here.
class Order(BaseModel):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=False, null=False)
    total_amount = models.PositiveIntegerField(blank=False, null=False)
    discount_amount = models.PositiveIntegerField(blank=False, null=False, default = 0)
    amount_payable = models.PositiveIntegerField(blank=False, null=False)

    is_paid = models.BooleanField(blank=False, null=False, default=False)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=False)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=False)
    razorpay_payment_signature = models.CharField(max_length=100, blank=True, null=False)


    def getAmountPayable(self):
        final_price = self.total_amount - self.discount_amount
        return final_price


class OrderItem(BaseModel):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=False, null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False, null=False)
    address = models.TextField(blank=False, null=False)
    item_amount = models.PositiveIntegerField(blank=False, null=False)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    is_a_replacement = models.BooleanField(blank=False, null=False, default=False)
    # expected_delivery_date = models.DateField(blank=False, null=False)


    def __str__(self):
        return f'{self.product} ({self.address} - {self.order})'

    
    def get_order_item_total(self):
        return self.item_amount * self.quantity



# class OrderItemStatus(BaseModel):
#     order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, blank=False, null=False)
#     seller = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=False, null=False)
#     status_type = models.CharField(max_length=20, choices=ORDER_ITEM_STATUS_TYPE_CHOICES, blank=False, null=False)
#     status_description = models.TextField(blank=False, null=False)
    # expected_date = models.DateTimeField(blank=False, null=False)


#     def __str__(self):
#         return f'{self.status_type} ({self.order_item} - {self.seller}'
