# Common Modules
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages



# Models
from Account.models import *



def add_to_cart(request, product_slug, quantity):
    user = request.user
    # product_slug = request.GET['product-slug']
    # quantity = request.GET['quantity']

    if user.is_authenticated:
        product = Product.objects.get(slug = product_slug)
        cart_item = CartItem.objects.filter(user = user, product = product)

        if cart_item.exists():
            messages.error(request, 'Item already exists in the cart')

        else:
            cart_item = CartItem.objects.create(user = user, product = product, quantity = quantity)
            messages.success(request, 'Item added to the cart')

        return redirect(request.META.get('HTTP_REFERER'))
    
    else:
        return redirect('LoginPage')



def remove_from_cart(request):
    if request.method == 'GET':
        user = request.user
        cart_item_unique_id = request.GET['cart-item-id']

        cart_item = CartItem.objects.get(unique_id = cart_item_unique_id)

        cart_item.delete()
        messages.success(request, 'Item removed from the cart')

        return redirect(request.META.get('HTTP_REFERER'))



def change_quantity(request):
    if request.method == 'GET':
        user = request.user
        req_type = str(request.GET['req-type'])
        cart_item_unique_id = request.GET['cart-item-id']
        
        if user.is_authenticated:
            cart_item = CartItem.objects.get(unique_id = cart_item_unique_id)

            if req_type == 'add' and cart_item.quantity < 9:
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()

            elif req_type == 'sub' and cart_item.quantity > 1:
                cart_item.quantity = cart_item.quantity - 1
                cart_item.save()

            return redirect(request.META.get('HTTP_REFERER'))
        

        else:
            return redirect('Error403')




def add_to_wishlist(request):
    if request.method == 'GET':
        user = request.user

        if user.is_authenticated:
            if 'add-to-selected-wishlist' in request.GET:
                product_slug = request.GET['product-slug']
                wishlist_id = request.GET['wishlist-id']

                product = Product.objects.get(slug = product_slug)
                wishlist = Wishlist.objects.get(unique_id = wishlist_id)
                wishlist_item = WishlistItem.objects.filter(wishlist = wishlist, product = product)

                if wishlist_item.exists():
                    messages.error(request, f'Item already exists in {wishlist.name} wishlist')

                else:
                    wishlist_item = WishlistItem.objects.create(wishlist = wishlist, product = product)
                    messages.success(request, f'Item added to {wishlist.name} wishlist')


            elif 'add-to-new-wishlist' in request.GET:
                product_slug = request.GET['product-slug']
                new_wishlist_name = request.GET['new-wishlist-name']
                
                product = Product.objects.get(slug = product_slug)
                wishlist = Wishlist.objects.filter(user = user, name = new_wishlist_name)
                
                if wishlist.exists():
                    messages.error(request, 'Wishlist with similar name already exists')

                else:
                    wishlist = Wishlist.objects.create(user = user, name = new_wishlist_name)
                    wishlist_item = WishlistItem.objects.filter(wishlist = wishlist, product = product)
                    
                    if wishlist_item.exists():
                        messages.error(request, 'Item already exists in that wishlist')
                    
                    else:
                        wishlist_item = WishlistItem.objects.create(wishlist = wishlist, product = product)
                        messages.success(request, f'Item added to {wishlist.name} wishlist')
        
        
        else:
            return redirect('LoginPage')


        return redirect(request.META.get('HTTP_REFERER'))



def remove_from_wishlist(request):
    if request.method == 'GET':
        user = request.user

        if user.is_authenticated:
            wishlist_item_id = request.GET['wishlist-item-id']

            wishlist_item = WishlistItem.objects.filter(unique_id = wishlist_item_id)

            if wishlist_item.exists():
                wishlist_item.delete()
                messages.success(request, f'Item removed from the wishlist')

            else:
                messages.error(request, f"Item doesn't exists in the wishlist")

            return redirect(request.META.get('HTTP_REFERER'))


        else:
            return redirect('LoginPage')

    


def create_new_wishlist(request):
    user = request.user

    if request.method == 'GET':
        wishlist_name = request.GET['wishlist-name']

        if user.is_authenticated:
            wishlist = Wishlist.objects.filter(user = user, name = wishlist_name)

            if wishlist.exists():
                messages.error(request, f'Wishlist with similar name already exists')

            else:
                wishlist = Wishlist.objects.create(user = user, name = wishlist_name)
                messages.success(request, f'{wishlist.name} wishlist created')
            
            return redirect(request.META.get('HTTP_REFERER'))
        

        else:
            return redirect('LoginPage')



def delete_wishlist(request):
    if request.method == 'GET':
        wishlist_id = request.GET['wishlist-id']

        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(unique_id = wishlist_id)

            if wishlist.exists():
                wishlist.delete()
                messages.success(request, f'Wishlist deleted')

            else:
                messages.error(request, f"Wishlist doesn't exists")
            
            return redirect('AllWishlists')
        

        else:
            return redirect('Error403')



def edit_wishlist(request):
    if request.method == 'GET':
        wishlist_id = request.GET['wishlist-id']
        wishlist_new_name = request.GET['wishlist-new-name']

        if request.user.is_authenticated:
            existing_wishlist = Wishlist.objects.filter(user = request.user, name = wishlist_new_name)
            wishlist = Wishlist.objects.get(unique_id = wishlist_id)

            if existing_wishlist.exists():
                messages.error(request, 'Wishlist with similar name already exists.')
            
            else:
                wishlist.name = wishlist_new_name
                wishlist.save()
        
            return redirect(request.META.get('HTTP_REFERER'))
        

        else:
            return redirect('Error403')
