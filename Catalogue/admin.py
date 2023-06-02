from django.contrib import admin



# Models
from Catalogue.models import *



# Register your models here.
class ColourVariantAdmin(admin.StackedInline):
    model = ColourVariant
    extra = 3


class SpecsVariantAdmin(admin.StackedInline):
    model = SpecsVariant
    extra = 3


class ProductStructureAdmin(admin.ModelAdmin):
    inlines = [ColourVariantAdmin, SpecsVariantAdmin]


admin.site.register(ProductStructure, ProductStructureAdmin)
admin.site.register([ColourVariant, SpecsVariant, ProductImage])



class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'colour', 'variant', 'selling_price', 'seller']

admin.site.register(Product, ProductAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']

admin.site.register(ProductCategory, ProductCategoryAdmin)