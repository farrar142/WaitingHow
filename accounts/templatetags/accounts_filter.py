from django import template
from django.utils.safestring import mark_safe
from django.core import serializers
import json
register = template.Library()

@register.filter
def get_count(waiting):
    shop_waiting = waiting.shop_name.waiting_set.filter(id__lt = waiting.id,is_disposed=False).count()
    return shop_waiting