#Common Modules
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied



# Models
from Account.models import *
from Order.models import *



from Account.views.UtilityFunctions import *




# Create New User :
def createNewUser(email, password, account_type, *data):
    NewUser = MyUser.objects.filter(email = email.lower())

    if NewUser.exists():
        return "User Already Exists"

    else:
        NewUser = MyUser.objects.create(email = email.lower(), account_type = account_type)
        NewUser.set_password(password)
        NewUser.save()

        if account_type == 'INDIVIDUAL':
            IndividualUserAccount.objects.create(user = NewUser, first_name = data[0].lower().capitalize(), last_name = data[1].lower().capitalize(), date_of_birth = data[2], gender = data[3])

        elif account_type == 'BUSINESS':
            BusinessUserAccount.objects.create(user = NewUser, organization_name = data[0], headquarters_address = data[1], date_of_establishment = data[2], gst_in_no = data[3])
        
        send_account_verification_mail(NewUser)
        return "Account Created Successfully"



def upgradeToBusinessAccount():
    pass




def AccountActivationRequest(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = MyUser.objects.get(email = email)
        send_account_verification_mail(user)
        messages.success(request, "An email has been sent to your registered email account")
        return redirect(request.META.get('HTTP_REFERER'))



def ForgotPasswordRequest(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = MyUser.objects.get(email = email)
            user.account_verification_token = None
            user.is_verified = False
            password_reset_mail(user)
            messages.success(request, "An email has been sent to your registered email account")
        
        except:
            user = None
            messages.warning(request, "No Such User Exists")

        return redirect(request.META.get('HTTP_REFERER'))

    
    elif request.method == 'GET':
        return redirect('Error400')



def ResetPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        token = request.POST['token']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']

        user = MyUser.objects.get(email = email)
        if user.reset_password_token ==  str(token):
            password_verification = isPasswordConfirmed(password, confirm_password)
            
            if password_verification == False:
                messages.warning(request, 'Password did not match!!!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            else:
                user.set_password(password)
                user.reset_password_token = None
                user.is_verified = True
                user.save()
                messages.success(request, 'Password Reset Successful')
                return redirect('LoginPage')

        else:
            return HttpResponse('Invalid Verification Token')
    

    elif request.method == 'GET':
        return redirect('Error400')



# Password Verification :
# 1. Strong Password
def isPasswordStrong(Password):
    if len(Password) < 8 or len(Password) > 16:
        # messages.warning(request, 'Password must be 8-16 characters long')
        return 2

    else:
        Upper = 0
        Lower = 0
        Digit = 0

        for char in Password:
            if char.isupper() == True:
                Upper = Upper + 1

            elif char.islower() == True:
                Lower = Lower + 1

            elif char.isdigit() == True:
                Digit = Digit + 1

        if Upper < 1 or Lower < 1 or Digit < 1:
            # messages.warning(request, 'Password must contain atleast a number, an uppercase and a lowercase character')
            return 1

        else:
            return 0



# 2. Password Confirmation
def isPasswordConfirmed(Password, ConfirmPassword):
    if Password != ConfirmPassword:
        # messages.warning(request, 'Password did not match!!!')
        return False

    else:
        return True


from datetime import date, datetime

def isAge16(date_of_birth):
    date_of_birth_converted = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    age = (date.today() - date_of_birth_converted).days / 365
    
    if age > 16:
        return True

    else:
        return False





# User Authentication
from django.contrib.auth import authenticate, login, logout



# User Authentication (Login / Logout Functionality):
def userAuthentication(request, email, password):
    NewUser = MyUser.objects.filter(email = email)

    if NewUser.exists():
        user = authenticate(email = email, password = password)

        if user is None:
            # messages.error(request, 'Invalid Credentials!')
            return 1

        else:
            if user.is_verified == True:
                login(request, user)
                # messages.success(request, 'Logged in Successfully.')
                return 0

            else:
                # messages.error(request, 'Account is Inactive')
                return 3

    else:
        # messages.warning(request, 'No such user exists!')
        return 2



def userLogout(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            logout(request)
            messages.success(request, 'Logged Out Successfully')
            return redirect('HomePage')

        elif request.method == 'GET':
            return redirect('Error400')
    
    else:
        return redirect('Error403')