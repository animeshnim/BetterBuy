# Modules
from django.contrib import admin



# Models
from Account.models import *



# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['email']

admin.site.register(MyUser, MyUserAdmin)




class IndividualUserAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'date_of_birth', 'gender']

admin.site.register(IndividualUserAccount, IndividualUserAccountAdmin)




class BusinessUserAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization_name', 'date_of_establishment', 'headquarters_address', 'gst_in_no']

admin.site.register(BusinessUserAccount, BusinessUserAccountAdmin)

admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)



class AddressAdmin(admin.ModelAdmin):
    list_display = ['address']
    readonly_fields = ['slug']

admin.site.register(Address, AddressAdmin)
