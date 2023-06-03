# Imports
from django.shortcuts import render, redirect



from Catalogue.models import *



# Create your views here.
def Index(request):
    categories = ProductCategory.objects.all()

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