import django
from django.template import Library
from django.template.defaulttags import url as django_url

register = Library()


@register.tag
def url(parser, token):
    """
    A compatibility wrapper for the `url` template tag.
    """
    return django_url(parser, token)
