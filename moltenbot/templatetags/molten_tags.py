from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='heat_color')
def heat_color(value):
    try:
        temp = int(value)
    except (ValueError, TypeError):
        return "#ffffff"

    if temp <= 200:
        return "#3498db" # Blue
    elif temp <= 500:
        return "#2ecc71" # Green
    elif temp <= 800:
        return "#f39c12" # Orange
    else:
        return "#e74c3c" # Red

@register.filter(name='heat_gradient')
def heat_gradient(value):
    try:
        temp = int(value)
    except (ValueError, TypeError):
        temp = 0
    
    percentage = min(100, (temp / 1000) * 100)
    return mark_safe(f'style="width: {percentage}%; background-color: {heat_color(temp)};"')
