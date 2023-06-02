from django import template
register = template.Library()


# Models
from Account.models import *


# Tags
@register.simple_tag()
def is_in_cart(user, product):
    if user.is_authenticated:
        cart_items = CartItem.objects.filter(user = user, product = product)

        if cart_items.exists():
            return True

        else:
            return False

    else:
            return False