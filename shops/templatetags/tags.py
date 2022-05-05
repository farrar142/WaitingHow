from django import template
from django.utils.safestring import mark_safe
from django.core import serializers
import json
register = template.Library()

@register.filter
def obj(obj):
    target = serializers.serialize('json',obj)
    return mark_safe(target)
