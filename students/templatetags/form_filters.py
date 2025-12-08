from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    """
    Add a CSS class to a form field.
    Usage: {{ form.field|add_class:"form-control" }}
    """
    return value.as_widget(attrs={"class": arg})
