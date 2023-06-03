"""
Account URL Configuration

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
from Account.views import MyViews
from Account.views import ViewHelperFunctions
from Account.views import UtilityFunctions




# URL Patterns
urlpatterns = [
    # Public Pages
    path('signup', MyViews.IndividualSignUpPage, name='IndividualSignUpPage'),
    path('login', MyViews.LoginPage, name='LoginPage'),
    path('login/<str:EndURL>', MyViews.LoginPage, name='LoginPageFtRedirect'),


    # Account Specific Pages
    # Account Verification
    path('account-status/inactive', MyViews.AccountStatusPage, name='AccountStatusPage'),
    path('account-activation-request', ViewHelperFunctions.AccountActivationRequest, name='account_activation_request'),


    # Password Reset Pages
    path('forgot-password', MyViews.ForgotPasswordPage, name='ForgotPasswordPage'),
    path('forgot-password/request', ViewHelperFunctions.ForgotPasswordRequest, name='forgot_password_request'),
    path('reset-password/<str:token>', MyViews.ResetPasswordPage, name='ResetPasswordPage'),
    path('reset-password', ViewHelperFunctions.ResetPassword, name='ResetPassword'),
    


    # User Specific Pages
    path('my-account', MyViews.AccountPage, name='AccountPage'),
    path('my-cart', MyViews.CartPage, name = 'CartPage'),
    path('my-wishlists', MyViews.Wishlists, name = 'Wishlists'),
    path('my-wishlists/wishlist/<str:id>', MyViews.WishlistPage, name = 'WishlistPage'),
    path('my-orders', MyViews.Orders, name = 'Orders'),



    # Utilities
    path('logout', ViewHelperFunctions.userLogout, name='Logout'),
    path('activate/<str:token>', MyViews.MyUserAccountActivation, name='MyUserAccountActivation'),
    
    path('add-new-address', UtilityFunctions.add_new_address, name='add-new-address'),
    path('edit-address', UtilityFunctions.edit_address, name='edit-address'),
    path('delete-address/<str:address_id>', UtilityFunctions.delete_address, name='delete-address'),
    path('change-password', MyViews.change_password, name='change-password'),
    path('change-account-details', MyViews.change_account_details, name='change-account-details'),
]