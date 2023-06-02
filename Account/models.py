# Modules
import uuid
from django.utils.text import slugify
from django.core.validators import MinLengthValidator, int_list_validator
    




# Models
from django.db import models
from django.contrib.auth.models import AbstractUser
from Account.manager import *


from Base.models import *
from Catalogue.models import Product



# Choices Data
GENDER_CHOICES = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ('OTHERS', 'Others'),
    ('PREFER NOT TO SAY', 'Prefer not to Say'),
)


ACCOUNT_TYPE_CHOICES = (
    ('INDIVIDUAL', 'Individual'),
    ('BUSINESS', 'Business'),
)


ADDRESS_TYPE = (
    ('HOME', 'Home Address'),
    ('WORK', 'Office/Work Address'),
)




# Create your models here.
class MyUser(AbstractUser):
    unique_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, blank=False, null=False)

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, blank=False, null=False)
    is_verified = models.BooleanField(blank=False, null=False, default=False)
    is_seller = models.BooleanField(blank=False, null=False, default=False)

    account_verification_token = models.CharField(max_length=100, editable=False, blank=True, null=True)
    reset_password_token = models.CharField(max_length=100, editable=False, blank=True, null=True, default = None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()


    def __str__(self):
        return self.email


    def get_total_cart_items(self):
        total_cart_items = 0
        cart_items = CartItem.objects.filter(user = self)

        for cart_item in cart_items:
            total_cart_items = total_cart_items + cart_item.quantity

        return total_cart_items



    def get_cart_total(self):
        cart_total = 0
        cart_items = CartItem.objects.filter(user = self)
        
        for cart_item in cart_items:
            cart_total = cart_total + cart_item.get_cart_item_total()
        
        return cart_total



# from django.core.mail import send_mail

# @receiver(post_save, sender=MyUser)
# def send_verification_email(sender, instance, created, **kwargs):
#     if created:
#         mail_subject = 'Verify your Account | My Store'
#         mail_body = f"Please verify your email address to complete your registration. Click on the link to verify. http://127.0.0.1:8000/account/activate/{instance.account_verification_token}"
#         email_from = settings.EMAIL_HOST_USER
#         email_to = [instance.email]
#         send_mail(subject = mail_subject, message = mail_body, from_email = email_from, recipient_list = email_to, fail_silently = False)


class IndividualUserAccount(BaseModel):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=25, blank=False, null=False)
    last_name = models.CharField(max_length=25, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=False, null=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

    def __str__(self):
        return self.full_name




class BusinessUserAccount(BaseModel):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, unique=True, blank=False, null=False)
    organization_name = models.CharField(max_length=150, blank=False, null=False)
    headquarters_address = models.TextField(unique=True, blank=False, null=False)
    date_of_establishment = models.DateField(blank=False, null=False)
    gst_in_no = models.CharField(max_length=15, unique=True, blank=False, null=False)


    def __str__(self):
        return self.organization_name




class IndividualSellerAccount(BaseModel):
    user = models.OneToOneField(IndividualUserAccount, on_delete=models.CASCADE, unique=True, blank=False, null=False)
    business_name = models.CharField(max_length=150, blank=False, null=False)
    seller_name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    primary_address = models.TextField(unique=True, blank=False, null=False)
    seller_email = models.EmailField(blank=False, null=False, unique=True)
    gst_in_no = models.CharField(max_length=15, blank=False, null=False, unique=True)


    def __str__(self):
        return self.seller_name




class BusinessSellerAccount(BaseModel):
    user = models.OneToOneField(BusinessUserAccount, on_delete=models.CASCADE, unique=True, blank=False, null=False)
    seller_name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    seller_email = models.EmailField(blank=False, null=False, unique=True)


    def __str__(self):
        return self.seller_name




# User Specific Models:
class CartItem(BaseModel):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    
    quantity = models.PositiveIntegerField()
    is_paid = models.BooleanField(blank=False, null=False, default=False)


    def __str__(self):
        return f"{self.product} ({self.quantity}) - {self.user}"


    def get_cart_item_total(self):
        return self.product.selling_price * self.quantity



class Wishlist(BaseModel):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)


    def __str__(self):
        return f"{self.name} - {self.user}"



class WishlistItem(BaseModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    

    def __str__(self):
        return f"{self.product} ({self.wishlist})"



class Address(BaseModel):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, blank=False, null=False, default=None)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE, blank=False, null=False, default='HOME')
    name = models.CharField(max_length=50, blank=False, null=False)
    house_and_building = models.CharField(max_length=100, blank=False, null=False)
    street_or_colony = models.CharField(max_length=100, blank=False, null=False)
    landmark = models.CharField(max_length=60, blank=True, null=True, default=None)
    area = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    district = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=30, blank=False, null=False)
    pincode = models.CharField(max_length=6, validators=[int_list_validator(sep=''), MinLengthValidator(6)], blank=False, null=False)
    contact_no = models.CharField(max_length=10, validators=[int_list_validator(sep=''), MinLengthValidator(10)], blank=False, null=False)
    default = models.BooleanField(blank=False, null=False)

    slug = models.TextField(unique=True)


    @property
    def address(self):
        if self.landmark == None:
            return f'''{self.house_and_building},
            {self.street_or_colony},
            {self.area}, {self.city} ({self.district} - {self.state}) - {self.pincode}
            Contact: {self.contact_no}'''

        else:
            return f'''{self.house_and_building},
            {self.street_or_colony}, Near {self.landmark},
            {self.area}, {self.city} ({self.district} - {self.state}) - {self.pincode}
            Contact: {self.contact_no}'''


    def save(self , *args , **kwargs):
        if self.landmark == None:
            self.slug = slugify(f'{self.user} {self.name} {self.house_and_building} {self.street_or_colony} {self.area} {self.city} {self.district} {self.state} {self.pincode} {self.contact_no}')
        else:
            self.slug = slugify(f'{self.user} {self.name} {self.house_and_building} {self.street_or_colony} {self.landmark} {self.area} {self.city} {self.district} {self.state} {self.pincode} {self.contact_no}')

        super(Address, self).save(*args, **kwargs)


    def __str__(self):
        if self.landmark == None:
            return f'{self.name} - {self.house_and_building}, {self.street_or_colony}, {self.area}, {self.city} ({self.district} - {self.state}) - {self.pincode}, {self.contact_no}'
        else:
            return f'{self.name} - {self.house_and_building}, {self.street_or_colony}, {self.landmark}, {self.area}, {self.city} ({self.district} - {self.state}) - {self.pincode}, {self.contact_no}'