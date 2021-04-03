from django import template
from rango.models import UserProfile

register = template.Library()

@register.inclusion_tag('rango/sellers.html')
#function to get the list of categories to be used in menu
def get_category_list(current_seller=None):
    return {'sellers': UserProfile.objects.filter(is_seller=True),'current_seller': current_seller}
