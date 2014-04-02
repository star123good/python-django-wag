import warnings

from django import template

from wagtail.wagtailadmin.views import userbar
from wagtail.wagtailcore.models import Page

register = template.Library()

@register.simple_tag(takes_context=True)
def wagtailuserbar(context, css_path=None):
    if css_path is not None:
        warnings.warn(
            "Passing a CSS path to the wagtailuserbar tag is no longer required; use {% wagtailuserbar %} instead",
            DeprecationWarning
        )

    # Find request object
    request = context['request']
    
    # Don't render if user doesn't have permission to access the admin area
    if not request.user.has_perm('wagtailadmin.access_admin'):
        return ''

    # Find page object
    if 'self' in context and isinstance(context['self'], Page) and context['self'].id is not None:
        pass
    else:
        return ''

    # Render edit bird
    return userbar.render_edit_frame(request, context) or ''