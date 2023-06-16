# Imports
from django.shortcuts import render
from django.views.decorators.cache import cache_control



# Views
from Account.views.ViewHelperFunctions import *
from Account.models import *



# Create your views here
def LoginPage(request, EndPoint = None, EndURL = None):

    if request.method == 'POST':
        email = request.POST['login-email']
        password = request.POST['login-password']

        login_data = userAuthentication(request, email.lower(), password)
        
        if login_data == 1:
            messages.error(request, 'Invalid Credentials!')
            return HttpResponseRedirect(request.path_info)

        elif login_data == 2:
            messages.warning(request, 'No such user exists!')
            return HttpResponseRedirect(request.path_info)

        elif login_data == 0:
            messages.success(request, 'Logged in Successfully')
            
            if EndPoint == None:
                return redirect('HomePage')
            
            elif EndPoint == 'WebPage':
                return redirect(EndURL)

            elif EndPoint == 'WebURL':
                return redirect(EndURL)


        elif login_data == 3:
            request.session['email'] = email
            return redirect('AccountStatusPage')


    elif request.method == 'GET':
        data = {}
        return render(request, 'Account/Login/LoginPage.html', data)



def IndividualSignUpPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        date_of_birth = request.POST['date-of-birth']
        gender = request.POST['gender']

        strong_password_check = isPasswordStrong(password)
        password_verification = isPasswordConfirmed(password, confirm_password)
        age_validation = isAge16(date_of_birth)


        if strong_password_check == 2:
            messages.warning(request, 'Password must be 8-16 characters long')
            return HttpResponseRedirect(request.path_info)

        elif strong_password_check == 1:
            messages.warning(request, 'Password must contain atleast a number, an uppercase and a lowercase character')
            return HttpResponseRedirect(request.path_info)

        elif password_verification == False:
            messages.warning(request, "Password and Confirm Password didn't match!!!")
            return HttpResponseRedirect(request.path_info)

        elif age_validation == False:
            messages.warning(request, 'You are younger than 16 years')
            return HttpResponseRedirect(request.path_info)

        else:
            account_creation_status = createNewUser(email, password, "INDIVIDUAL", first_name, last_name, date_of_birth, gender)

            if account_creation_status == "User Already Exists":
                messages.warning(request, 'User Already Exists')
                return HttpResponseRedirect(request.path_info)

            elif account_creation_status == "Account Created Successfully":
                messages.success(request, "User Account Created. Please activate your account using the send email.")
                return HttpResponseRedirect(request.path_info)


    elif request.method == 'GET':
        data = {}
        return render(request, 'Account/SignUp/IndividualSignUp.html', data)




@cache_control(max_age = 0, no_cache = True, no_store = True, must_revalidate = True)
def MyUserAccountActivation(request, token):
    try:
        user = MyUser.objects.get(account_verification_token = token)
        token_verification_status = PasswordResetTokenGenerator().check_token(user, token)

        if token_verification_status == True:
            user.is_verified = True
            user.account_verification_token = None
            user.save()
            messages.success(request, "User Account Verified Successfully")
            return redirect('LoginPage')

        else:
            return HttpResponse('Invalid Verification Token')


    except Exception as e:
        print(e)
        return HttpResponse('Invalid Verification Token')




@cache_control(max_age = 0, no_cache = True, no_store = True, must_revalidate = True)
def ResetPasswordPage(request, token):
    try:
        user = MyUser.objects.get(reset_password_token = token)
        token_verification_status = PasswordResetTokenGenerator().check_token(user, token)
        
        data = {'user':user, 'token':token}

        if token_verification_status == True:
            return render(request, 'Account/Login/ResetPasswordPage.html', data)

        else:
            return HttpResponse('Invalid Verification Token')


    except Exception as e:
        print(e)
        return HttpResponse('Invalid Verification Token')




def ForgotPasswordPage(request):
    return render(request, 'Account/Login/ForgotPasswordPage.html')




@cache_control(max_age = 0, no_cache = True, no_store = True, must_revalidate = True)
def AccountStatusPage(request):
    user = MyUser.objects.get(email = request.session['email'])

    data = {'user':user}
    return render(request, 'Account/Login/AccountStatusPage.html', data)




# User Acoount Pages
# 1. Account Page
def AccountPage(request):
    user = request.user
    addresses = Address.objects.filter(user = user)

    if user.is_authenticated:
        data = {'user' : user, 'addresses': addresses}
        return render(request, 'Account/MyAccount.html', data)

    else:
        return LoginPage(request, EndPoint = 'WebPage', EndURL = 'AccountPage')



# Utility Functions for Account Related Changes
from django.contrib.auth import authenticate

def change_password(request):
    if user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email']
            old_password = request.POST['current-password']
            new_password = request.POST['new-password']
            confirm_password = request.POST['confirm-password']

            user = authenticate(email = email, password = old_password)
            strong_password_check = isPasswordStrong(new_password)
            password_verification = isPasswordConfirmed(new_password, confirm_password)
            
            if user == None:
                messages.error(request, 'Invalid Credentials!')
                return redirect(request.META.get('HTTP_REFERER'))
            
            else:
                if strong_password_check == 2:
                    messages.warning(request, 'Password must be 8-16 characters long')
                    return redirect(request.META.get('HTTP_REFERER'))

                elif strong_password_check == 1:
                    messages.warning(request, 'Password must contain atleast a number, an uppercase and a lowercase character')
                    return redirect(request.META.get('HTTP_REFERER'))

                elif password_verification == False:
                    messages.warning(request, "Password and Confirm Password doesn't match")
                    return redirect(request.META.get('HTTP_REFERER'))

                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password Changed Successfully')
                    return redirect(request.META.get('HTTP_REFERER'))
        

        elif request.method == 'GET':
            return redirect('Error400')
    

    else:
        return redirect('Error403')



def change_account_details(request):
    user = request.user
        
    if user.is_authenticated:
        if request.method == 'POST':
            if user.account_type == 'INDIVIDUAL' and user.is_seller == False:
                first_name = request.POST['first-name']
                last_name = request.POST['last-name']
                date_of_birth = request.POST['date-of-birth']
                gender = request.POST['gender']

                age_validation = isAge16(date_of_birth)
                if age_validation == False:
                    messages.warning(request, "Your age shouldn't be less than 16 years")
                    return redirect(request.META.get('HTTP_REFERER'))

                else:
                    UserAccount = IndividualUserAccount.objects.get(user = user)
                    UserAccount.first_name = first_name.lower().capitalize()
                    UserAccount.last_name = last_name.lower().capitalize()
                    UserAccount.date_of_birth = date_of_birth
                    UserAccount.gender = gender
                    UserAccount.save()
                    messages.success(request, 'Account Details Updated')


            elif user.account_type == 'INDIVIDUAL' and user.is_seller == True:
                pass

            elif user.account_type == 'BUSINESS' and user.is_seller == False:
                pass

            elif user.account_type == 'BUSINESS' and user.is_seller == True:
                pass

            return redirect(request.META.get('HTTP_REFERER'))
        
        
        elif request.method == 'GET':
                return redirect('Error400')
    

    else:
        return redirect('Error403')



# 2. Cart
@cache_control(max_age = 0, no_cache = True, no_store = True, must_revalidate = True)
def CartPage(request):
    user = request.user

    if user.is_authenticated:
        cart_items = CartItem.objects.filter(user = user)
        addresses = Address.objects.filter(user = user)
        wishlists = Wishlist.objects.filter(user = user)

        data = {
            'cart_items': cart_items,
            'addresses': addresses,
            'wishlists' : wishlists,
        }

        return render(request, 'Account/MyCart.html', data)


    else:
        return LoginPage(request, EndPoint = 'WebPage', EndURL = 'CartPage')




# 3. Wishlist
def AllWishlists(request):
    user = request.user

    if user.is_authenticated:
        wishlists = Wishlist.objects.filter(user = user)

        data = {
            'wishlists': wishlists
        }

        return render(request, 'Account/AllWishlists.html', data)


    else:
        return LoginPage(request, EndPoint = 'WebPage', EndURL = 'AllWishlists')


def MyWishlist(request, id):
    user = request.user

    if user.is_authenticated:
        wishlist = Wishlist.objects.get(unique_id = id)
        wishlist_items = WishlistItem.objects.filter(wishlist = wishlist)


        data = {
            'wishlist':wishlist,
            'wishlist_items':wishlist_items,
        }


        return render(request, 'Account/MyWishlist.html', data)

    else:
        return LoginPage(request, EndPoint = 'WebPage', EndURL = 'MyWishlist')




def Orders(request):
    user = request.user

    if user.is_authenticated:
        orders = Order.objects.filter(user = user)
        order_items = OrderItem.objects.filter(user = user)


        data = {
            'orders':orders,
            'order_items':order_items,
        }


        return render(request, 'Account/MyOrders.html', data)

    else:
        return LoginPage(request, EndPoint = 'WebPage', EndURL = 'Orders')
