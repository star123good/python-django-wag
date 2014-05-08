from django import forms
from django.db import models
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import permission_required

from wagtail.wagtailadmin.userbar import EditPageItem, AddPageItem, ApproveModerationEditPageItem, RejectModerationEditPageItem
from wagtail.wagtailadmin import hooks
from wagtail.wagtailcore.models import Page, PageRevision

from wagtail.wagtailadmin.edit_handlers import PageChooserPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtaildocs.edit_handlers import DocumentChooserPanel

from wagtail.wagtailadmin.forms import SearchForm
from wagtail.wagtailcore.fields import RichTextField


CHOICES = (
    ('choice1', 'choice 1'),
    ('choice2', 'choice 2'),
)

class ExampleForm(forms.Form):
    text = forms.CharField(required=True, help_text="help text")
    url = forms.URLField(required=True)
    email = forms.EmailField(max_length=254)
    date = forms.DateField()
    select = forms.ChoiceField(choices=CHOICES)
    boolean = forms.BooleanField(required=False)

@permission_required('wagtailadmin.access_admin')
def index(request):

    form = SearchForm(placeholder=_("Search something"))

    example_form = ExampleForm()

    messages.success(request, _("Success message"))
    messages.warning(request, _("Warning message"))
    messages.error(request, _("Error message"))

    return render(request, 'wagtailadmin/styleguide/base.html', {
        'search_form': form,
        'example_form': example_form,
    })
