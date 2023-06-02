# Modules
from atexit import register
from enum import unique
from unicodedata import category
from django.db import models
from tinymce.models import HTMLField
from django.conf import settings
from django.utils.text import slugify



# Models
from Base.models import *
from Account.models import *



# Options
class ProductCategory(BaseModel):
    category_name = models.CharField(max_length = 50, blank=False, null=False)
    slug = models.SlugField(max_length=255, unique=True, editable=False, blank=True)


    def __str__(self):
        return self.category_name


    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(ProductCategory, self).save(*args, **kwargs)

    
    def get_products_3(self):
        product_structures = ProductStructure.objects.filter(category = self)
        products = Product.objects.filter(product_structure__in = product_structures)[:3]
        return products



# Models Starts Here:

# Product Components
class ProductStructure(BaseModel):
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, blank=False, null=False)
    
    product_name = models.CharField(max_length=50)
    product_description = models.TextField()
    common_specifications = HTMLField()

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    unique_name = models.CharField(max_length=255, editable=False, blank=True, unique=True)
    slug = models.SlugField(max_length=500, unique=True, editable=False, blank=True)


    def __str__(self):
        return self.product_name

    
    def save(self , *args , **kwargs):
        self.unique_name = f"{self.product_name} {self.seller}"
        self.slug = slugify(self.unique_name)
        super(ProductStructure, self).save(*args, **kwargs)



class ColourVariant(BaseModel):
    colour = models.CharField(max_length=20)
    product_structure = models.ForeignKey(ProductStructure, on_delete=models.CASCADE)

    unique_name = models.CharField(max_length=255, editable=False, blank=True, unique=True)
    slug = models.SlugField(max_length=500, unique=True, editable=False, blank=True)


    def __str__(self):
        return self.colour


    def save(self , *args , **kwargs):
        self.unique_name = f"{self.product_structure} {self.colour} {self.product_structure.seller}"
        self.slug = slugify(self.unique_name)
        super(ColourVariant, self).save(*args, **kwargs)



class SpecsVariant(BaseModel):
    variant = models.CharField(max_length=30)
    variant_specifications = HTMLField()

    product_structure = models.ForeignKey(ProductStructure, on_delete=models.CASCADE)

    unique_name = models.CharField(max_length=255, editable=False, blank=True, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False, blank=True)


    def __str__(self):
        return self.variant


    def save(self , *args , **kwargs):
        self.unique_name = f"{self.product_structure} {self.variant} {self.product_structure.seller}"
        self.slug = slugify(self.unique_name)
        super(SpecsVariant, self).save(*args, **kwargs)



class ProductImage(BaseModel):
    image_name = models.CharField(max_length=20)
    image = models.ImageField(upload_to="Product_Images")

    product_structure = models.ForeignKey(ProductStructure, on_delete=models.CASCADE)
    colour = models.ForeignKey(ColourVariant, on_delete=models.CASCADE)

    unique_image_name = models.CharField(max_length=255, editable=False, blank=True, unique=True)
    slug = models.SlugField(max_length=500, unique=True, editable=False, blank=True)


    def __str__(self):
        return self.unique_image_name


    def save(self , *args , **kwargs):
        self.unique_image_name = f"{self.product_structure} {self.colour} {self.image_name} {self.product_structure.seller}"
        self.slug = slugify(self.unique_image_name)
        super(ProductImage, self).save(*args, **kwargs)



# Product
class Product(BaseModel):
    name = models.CharField(max_length=30, blank=True, null=True)
    product_name = models.CharField(max_length=180, blank=True, null=True, editable = False)
    selling_price = models.IntegerField()
    max_retail_price = models.IntegerField()

    product_structure = models.ForeignKey(ProductStructure, on_delete=models.CASCADE,blank=False, null=False)
    colour = models.ForeignKey(ColourVariant, on_delete=models.CASCADE, blank=False, null=False)
    variant = models.ForeignKey(SpecsVariant, on_delete=models.CASCADE, null=False)
    product_thumbnail = models.ForeignKey(ProductImage, on_delete = models.CASCADE, related_name = 'product_thumbnail', blank = True, null = True)
    product_images = models.ManyToManyField(ProductImage, related_name = 'product_images', blank = True)

    unique_product_name = models.CharField(max_length=255, editable=False, blank=True, unique=True)
    slug = models.SlugField(max_length=500, unique=True, editable=False, blank=True)

    @property
    def seller(self):
        return self.product_structure.seller

    def __str__(self):
        return self.product_name


    def save(self , *args , **kwargs):
        if self.name:
            self.product_name = f"{self.product_structure} ({self.colour}, {self.variant}) - {self.name}"
        else:
            self.product_name = f"{self.product_structure} ({self.colour}, {self.variant})"
            
        self.category = self.product_structure.category
        self.unique_product_name = f"{self.product_structure} {self.colour} {self.variant} {self.name} {self.product_structure.seller}"

        self.slug = slugify(self.unique_product_name)
        super(Product, self).save(*args, **kwargs)