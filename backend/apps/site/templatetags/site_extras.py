"""Small template helpers for the public site."""

from django import template

from apps.site.breadcrumbs import trail

register = template.Library()


@register.simple_tag
def crumb_trail(path, final=None):
    """The breadcrumb list for a path, for both the visible nav and the
    BreadcrumbList beside it."""
    return trail(path, final or None)
