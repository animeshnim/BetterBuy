# Imports
from django.shortcuts import render, redirect



# Model Imports
from Catalogue.models import *
from Account.models import *



# Create your views here.
def Index(request):
    user = request.user
    categories = ProductCategory.objects.all()

    if user.is_authenticated:
        wishlists = Wishlist.objects.filter(user = user)

        data = {
            'categories' : categories,
            'wishlists': wishlists,
        }

    else:
        data = {
            'categories' : categories,
        }
        
    return render(request, 'BetterBuy/HomePage.html', data)




# Error Pages :
# 4xx Errors:
def Error400(request, exception):
    return render(request, 'Error/400BadRequest.html', status=400)


def Error403(request, exception):
    return render(request, 'Error/403Forbidden.html', status=403)


def Error404(request, exception):
    return render(request, 'Error/404NotFound.html', status=404)



# 5xx Errors:
def Error500(request):
    return render(request, 'Error/500InternalServerError.html', status=500)