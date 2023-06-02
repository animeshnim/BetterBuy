# Imports
from django.shortcuts import render



# Views
from Catalogue.views.UtilityFunctions import *



# Models:
from Catalogue.models import *
from Account.models import *



# Create your views here
def Catalogue(request):
    user = request.user
    products = Product.objects.all()

    if user.is_authenticated:
        wishlists = Wishlist.objects.filter(user = user)

        data = {
            'products': products,
            'wishlists':wishlists,
        }


    else:
        data = {
            'products': products,
        }

    return render(request, 'Catalogue/CataloguePage.html', data)



def ProductPage(request, slug):
    user = request.user
    product = Product.objects.get(slug = slug)
    colour_variants = ColourVariant.objects.filter(product_structure = product.product_structure)
    specs_variants = SpecsVariant.objects.filter(product_structure = product.product_structure)
    other_products = Product.objects.filter(product_structure = product.product_structure)
    product_images = ProductImage.objects.filter(product_structure = product.product_structure, colour = product.colour)

    
    if user.is_authenticated:
        wishlists = Wishlist.objects.filter(user = user)
        addresses = Address.objects.filter(user = user)

        data = {
            'product': product,
            'colour_variants': colour_variants, 
            'specs_variants': specs_variants, 
            'other_products': other_products,
            'product_images': product_images,
            'wishlists': wishlists,
            'addresses' : addresses,
        }

    else:
        data = {
            'product':product, 
            'colour_variants':colour_variants, 
            'specs_variants':specs_variants, 
            'other_products':other_products,
            'product_images':product_images,
        }
    

    return render(request, 'Catalogue/ProductPage.html', data)



from django.db.models import Q

def SearchedCatalogue(request):
    search_query = request.GET['query']
    searched_categories = ProductCategory.objects.filter(category_name__icontains = search_query)
    searched_product_structures = ProductStructure.objects.filter(Q(product_description__icontains = search_query) | Q(category__in = searched_categories))
    searched_products = Product.objects.filter(Q(product_name__icontains = search_query) | Q(product_structure__in = searched_product_structures))
    
    user = request.user
    if user.is_authenticated:
        wishlists = Wishlist.objects.filter(user = user)

        data = {
            'products' : searched_products,
            'your_query' : search_query,
            'wishlists': wishlists,
        }

    else:
        data = {
            'products' : searched_products,
            'your_query' : search_query,
        }

    return render(request, 'Catalogue/SearchedCatalogue.html', data)



def CategoryPage(request, category_slug):
    user = request.user

    try:
        category = ProductCategory.objects.get(slug = category_slug)
        product_structures = ProductStructure.objects.filter(category = category)
        products = Product.objects.filter(product_structure__in = product_structures)

        if user.is_authenticated:
            wishlists = Wishlist.objects.filter(user = user)

            data = {
                'category' : category,
                'products' : products,
                'wishlists': wishlists,
            }
        
        else:
            data = {
                'category' : category,
                'products' : products,
            }

        return render(request, 'Catalogue/CategoryPage.html', data)
    
    
    except Exception as e:
        print(e)
        return HttpResponse('An unexpected error has occurred')