from django import template

register = template.Library()

@register.filter
def custom_strip(value):
    if isinstance(value, str):
        return value.strip()  # Mətnin başlanğıc və sonundakı boşluqları silir
    return value
