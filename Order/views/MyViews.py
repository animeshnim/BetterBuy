# Imports
from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.cache import cache_control



# Views
from Order.views.UtilityFunctions import *



# Models:
from Order.models import *


@cache_control(max_age = 0, no_cache = True, no_store = True, must_revalidate = True)
def OrderSummary(request):
    if request.method == 'POST':
        user = request.user
        shipping_address_slug = request.POST['shipping-address-slug']

        if user.is_authenticated:
            address = Address.objects.get(slug = shipping_address_slug)
            cart_items = CartItem.objects.filter(user = user)

            if cart_items.count() == 0:
                messages.warning(request, "No items in your cart. Please add something to cart")
                return redirect('CartPage')

            all_addresses = Address.objects.filter(user = user)
            for add in all_addresses:
                if add == address:
                    add.default = True
                    add.save()
                else:
                    add.default = False
                    add.save()

            data = {
                'address':address,
                'cart_items':cart_items
            }

            return render(request, 'Order/OrderSummary.html', data)



@cache_control(max_age = 0, no_cache = True, no_store = True, must_revalidate = True)
def PendingOrderSummaryPage(request):
    if request.method == 'POST':
        user = request.user
        order_id = request.POST['order-id']
        addresses = Address.objects.filter(user = user)

        if user.is_authenticated:
            MyOrder = Order.objects.get(unique_id = order_id)
            
            if MyOrder.is_paid == True:
                messages.error(request, 'You have already paid for this order')
                return redirect(request.META.get('HTTP_REFERER'))
            
            else:
                order_items = OrderItem.objects.filter(order = MyOrder)

                data = {
                    'order': MyOrder,
                    'order_items': order_items,
                    'addresses': addresses,
                }

                return render(request, 'Order/PendingOrderSummary.html', data)



# Razorpay Integration:
import razorpay
from django.conf import settings

@cache_control(max_age = 0, no_cache = True, no_store = True, must_revalidate = True)
def PaymentPage(request):
    if request.method == 'POST':
        user = request.user
        order_type = request.POST['order-type']
        shipping_address_slug = request.POST['shipping-address-slug']

        if user.is_authenticated:
            address = Address.objects.get(slug = shipping_address_slug)
            
            if order_type == 'New':
                cart_items = CartItem.objects.filter(user = user)
                discount_amount = 0

                if cart_items.count() == 0:
                    return redirect('CartPage')


                # Order Creation
                MyOrder = Order.objects.create(user = user, total_amount = user.get_cart_total(), amount_payable = user.get_cart_total() - discount_amount)

                for cart_item in cart_items:
                    MyOrderItem = OrderItem.objects.create(user = user, order = MyOrder, address = address.address, product = cart_item.product, item_amount = cart_item.product.selling_price, quantity = cart_item.quantity)
                    cart_item.delete()
            

            elif order_type == 'Pending':
                order_id = request.POST['order-id']

                MyOrder = Order.objects.get(unique_id = order_id)
                order_items = OrderItem.objects.filter(order = MyOrder)

                for order_item in order_items:
                    order_item.address = address.address


            # Razorpay Order Creation
            client = razorpay.Client(auth = (settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
            
            payment_data = {
                "amount": MyOrder.amount_payable * 100,
                "currency": "INR",
            }
            
            # Payment Capture
            payment = client.order.create(data=payment_data)
            
            MyOrder.razorpay_order_id = payment['id']
            MyOrder.save()

            data = {
                'payment': payment,
                'address': address,
                'Order': MyOrder,
                'Key': settings.RAZORPAY_KEY,
            }
            
            return render(request, 'Order/PaymentPage.html', data)



# Order Processing Pages
@cache_control(max_age = 0, no_cache = True, no_store = True, must_revalidate = True)
def OrderPending(request):
    return render(request, 'Order/OrderPending.html')



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def OrderPaymentSuccess(request):
    if request.method == "POST":
        razorpay_order_id = request.POST['razorpay_order_id']
        razorpay_payment_id = request.POST['razorpay_payment_id']
        razorpay_payment_signature = request.POST['razorpay_signature']

        MyOrder = Order.objects.get(razorpay_order_id = razorpay_order_id)
        MyOrder.razorpay_payment_id = razorpay_payment_id
        MyOrder.razorpay_payment_signature = razorpay_payment_signature
        MyOrder.is_paid = True
        MyOrder.save()

        data = {
            'Order': MyOrder,
        }

        return render(request, 'Order/PaymentSuccess.html', data)