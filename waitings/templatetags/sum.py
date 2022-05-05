from django import template
from waitings.models import *
from shops.models import *
register = template.Library()

@register.filter
def how_many_people_waiting(shop):
    peoples = Waiting.objects.filter(shop_name=shop,is_disposed=False)
    result = 0
    for i in peoples:
        result += i.how_many
    return result

@register.filter
def how_many_team_waiting(shop):
    peoples = Waiting.objects.filter(shop_name=shop,is_disposed=False)
    return len(peoples)