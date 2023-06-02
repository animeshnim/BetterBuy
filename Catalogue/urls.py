"""Catalogue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



# Modules Import
from django.urls import path



# Import from Apps
from Catalogue.views import MyViews
from Catalogue.views import UtilityFunctions



# URL Patterns
urlpatterns = [
    # Public Pages
    # path('', MyViews.Catalogue, name='Catalogue'),
    path('search-results', MyViews.SearchedCatalogue, name='SearchedCatalogue'),
    path('products/category/<slug:category_slug>', MyViews.CategoryPage, name='CategoryPage'),
    path('product/<slug:slug>', MyViews.ProductPage, name='ProductPage'),
    

    # Utilities
    path('add-to-cart/<slug:product_slug>/<int:quantity>', UtilityFunctions.add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart', UtilityFunctions.remove_from_cart, name = 'remove-from-cart'),
    path('change-quantity', UtilityFunctions.change_quantity, name = 'change-quantity'),

    path('create-new-wishlist', UtilityFunctions.create_new_wishlist, name='create-new-wishlist'),
    path('delete-wishlist', UtilityFunctions.delete_wishlist, name='delete-wishlist'),
    path('edit-wishlist', UtilityFunctions.edit_wishlist, name='edit-wishlist'),

    path('add-to-wishlist', UtilityFunctions.add_to_wishlist, name = 'add-to-wishlist'),
    path('remove-from-wishlist', UtilityFunctions.remove_from_wishlist, name = 'remove-from-wishlist'),
]