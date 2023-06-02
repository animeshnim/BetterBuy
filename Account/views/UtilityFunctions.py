from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings



# Models
from Account.models import *



# Utility Functions for Account
def generate_unique_token(user):
    return PasswordResetTokenGenerator().make_token(user)



def send_account_verification_mail(user):
    unique_token = generate_unique_token(user)
    user.account_verification_token = unique_token
    user.save()

    mail_subject = 'Verify your Account | BetterBuy Store'
    html_message = render_to_string('Account/mail_templates/account_verification_mail.html', {'token': f"https://betterbuy.vercel.app/account/activate/{user.account_verification_token}"})
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    email_to = [user.email]

    message = EmailMultiAlternatives(mail_subject, html_message, email_from, email_to)
    message.content_subtype = "html"
    message.send()


def password_reset_mail(user):
    unique_token = generate_unique_token(user)
    user.reset_password_token = unique_token
    user.save()
    
    mail_subject = 'Reset Your Password | BetterBuy Store'
    html_message = render_to_string('Account/mail_templates/password_reset_mail.html', {'token': f"https://betterbuy.vercel.app/account/reset-password/{user.reset_password_token}"})
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    email_to = [user.email]

    message = EmailMultiAlternatives(mail_subject, html_message, email_from, email_to)
    message.content_subtype = "html"
    message.send()



# Utility Functions for Account Details:
def add_new_address(request):
    user = request.user

    if request.method == 'POST':
        address_type = request.POST['address-type']
        name = request.POST['name']
        house_and_building = request.POST['house-no']
        street_or_colony = request.POST['street-or-colony']
        landmark = request.POST['landmark']
        pincode = request.POST['pincode']
        area = request.POST['area']
        district = request.POST['district']
        city = request.POST['city']
        state = request.POST['state']
        contact_no = request.POST['contact-no']

        if user.is_authenticated:
            if len(contact_no) != 10:
                messages.warning(request, 'Incomplete Contact Number')
                return redirect(request.path_info)

            for char in contact_no:
                if char.isdigit() == False:
                    messages.error(request, 'Invalid Characters in Contact Number')
                    return redirect(request.path_info)

            address = Address.objects.filter(user = user, name = name, house_and_building = house_and_building, street_or_colony = street_or_colony, pincode = pincode, area = area, contact_no = contact_no)
            
            if address.exists():
                messages.error(request, f'Address already exists')

            else:
                address = Address.objects.create(user = user, address_type = address_type, name = name, house_and_building = house_and_building, street_or_colony = street_or_colony, landmark = landmark, area = area, pincode = pincode, district = district, city = city, state = state, contact_no = contact_no, default = True)
                all_addresses = Address.objects.filter(user = user)
                for add in all_addresses:
                    if add == address:
                        pass
                    else:
                        add.default = False
                        add.save()
                
                messages.success(request, 'New address added')

    return redirect(request.META.get('HTTP_REFERER'))



def delete_address(request, address_id):
    if request.user.is_authenticated:
        address = Address.objects.filter(unique_id = address_id)

        if address.exists():
            address.delete()
            messages.success(request, f'Address deleted')

        else:
            messages.error(request, f"Address doesn't exists")
        
        return redirect(request.META.get('HTTP_REFERER'))
    

    else:
        return redirect('LoginPage')



def edit_address(request):
    user = request.user

    if request.method == 'POST':
        address_id = request.POST['address-unique-id']

        address_type = request.POST['address-type']
        name = request.POST['name']
        house_and_building = request.POST['house-no']
        street_or_colony = request.POST['street-or-colony']
        landmark = request.POST['landmark']
        pincode = request.POST['pincode']
        area = request.POST['area']
        district = request.POST['district']
        city = request.POST['city']
        state = request.POST['state']
        contact_no = request.POST['contact-no']


        if user.is_authenticated:
            if len(contact_no) != 10:
                messages.warning(request, 'Incomplete Contact Number')
                return redirect(request.path_info)

            for char in contact_no:
                if char.isdigit() == False:
                    messages.error(request, 'Invalid Characters in Contact Number')
                    return redirect(request.path_info)

            try:
                address = Address.objects.get(unique_id = address_id)

                address.address_type = address_type
                address.name = name
                address.house_and_building = house_and_building
                address.street_or_colony = street_or_colony
                address.landmark = landmark
                address.pincode = pincode
                address.area = area
                address.district = district
                address.city = city
                address.state = state
                address.contact_no = contact_no
                address.save()
                
                if 'default' in request.POST:
                    all_addresses = Address.objects.filter(user = user)
                    for add in all_addresses:
                        if add == address:
                            address.default = True
                            address.save()
                        else:
                            add.default = False
                            add.save()
                
                messages.success(request, 'Address Updated')
                

            except:
                messages.error(request, f'Address already exists')


    return redirect(request.META.get('HTTP_REFERER'))