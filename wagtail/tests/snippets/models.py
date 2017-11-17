from __future__ import absolute_import, unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

from .forms import FancySnippetForm


# AlphaSnippet and ZuluSnippet are for testing ordering of
# snippets when registering.  They are named as such to ensure
# thier ordering is clear.  They are registered during testing
# to ensure specific [in]correct register ordering

# AlphaSnippet is registered during TestSnippetOrdering
class AlphaSnippet(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


# ZuluSnippet is registered during TestSnippetOrdering
class ZuluSnippet(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


# Register model as snippet using register_snippet as both a function and a decorator

class RegisterFunction(models.Model):
    pass


register_snippet(RegisterFunction)


@register_snippet
class RegisterDecorator(models.Model):
    pass


# A snippet model that inherits from index.Indexed can be searched on

@register_snippet
class SearchableSnippet(index.Indexed, models.Model):
    text = models.CharField(max_length=255)

    search_fields = [
        index.SearchField('text'),
    ]

    def __str__(self):
        return self.text


@register_snippet
class StandardSnippet(models.Model):
    text = models.CharField(max_length=255)


@register_snippet
class FancySnippet(models.Model):
    base_form_class = FancySnippetForm


@register_snippet
class FileUploadSnippet(models.Model):
    file = models.FileField()


class RichTextSection(models.Model):
    snippet = ParentalKey('MultiSectionRichTextSnippet', related_name='sections', on_delete=models.CASCADE)
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]


@register_snippet
class MultiSectionRichTextSnippet(ClusterableModel):
    panels = [
        InlinePanel('sections'),
    ]
