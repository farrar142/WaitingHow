from django import template
from django.utils.safestring import mark_safe
from django.core import serializers
register = template.Library()

@register.filter
def half(num):
    result = int(num/2)
    return mark_safe(result)

@register.filter
def divide(num,args):
    result = int(num/args)
    return mark_safe(result)

@register.filter
def percentage(num,args):
    result = int(num*args/100)
    return mark_safe(result)


@register.filter
def add(num,args):
    result = int(num)+int(args)
    return mark_safe(result)