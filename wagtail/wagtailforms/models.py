from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

import json
import re

from wagtail.wagtailcore.models import PageBase, Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailforms.backends.email import EmailFormProcessor

from modelcluster.fields import ParentalKey
from .forms import FormBuilder


FORM_FIELD_CHOICES = (
    ('singleline',   _('Single line text')),
    ('multiline',    _('Multi-line text')),
    ('email',        _('Email')),
    ('number',       _('Number')),
    ('url',          _('URL')),
    ('checkbox',     _('Checkbox')),
    ('checkboxes',   _('Checkboxes')),
    ('dropdown',     _('Drop down')),
    ('radio',        _('Radio buttons')),
    ('date',         _('Date')),
    ('datetime',     _('Date/time')),
)


HTML_EXTENSION_RE = re.compile(r"(.*)\.html")


class FormSubmission(models.Model):
    """Data for a Form submission."""

    form_data = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    form_page = generic.GenericForeignKey('content_type', 'object_id')

    submit_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)

    def get_data(self):
        return json.loads(self.form_data)

    def __unicode__(self):
        return self.form_data


class AbstractFormFields(Orderable):
    """Database Fields required for building a Django Form field."""

    label = models.CharField(
        max_length=255,
        help_text=_('The label of the form field')
    )
    field_type = models.CharField(max_length=16, choices=FORM_FIELD_CHOICES)
    required = models.BooleanField(default=True)
    choices = models.CharField(
        max_length=512,
        blank=True,
        help_text=_('Comma seperated list of choices. Only applicable in checkboxes, radio and dropdown.')
    )
    default_value = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Default value. Comma seperated values supported for checkboxes.')
    )
    help_text = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('label'),
        FieldPanel('field_type'),
        FieldPanel('required'),
        FieldPanel('choices'),
        FieldPanel('default_value'),
        FieldPanel('help_text'),
    ]

    class Meta:
        abstract = True


FORM_MODEL_CLASSES = []
_FORM_CONTENT_TYPES = []


def get_form_types():
    global _FORM_CONTENT_TYPES
    if len(_FORM_CONTENT_TYPES) != len(FORM_MODEL_CLASSES):
        _FORM_CONTENT_TYPES = [
            ContentType.objects.get_for_model(cls) for cls in FORM_MODEL_CLASSES
        ]
    return _FORM_CONTENT_TYPES


class FormBase(PageBase):
    """Metaclass for Forms"""
    def __init__(cls, name, bases, dct):
        super(FormBase, cls).__init__(name, bases, dct)

        if not cls.is_abstract:
            # register this type in the list of page content types
            FORM_MODEL_CLASSES.append(cls)
            # Check if form_processing_backend is ok
            if hasattr(cls, 'form_processing_backend'):
                cls.form_processing_backend.validate_usage(cls)


class AbstractForm(Page):
    """A Form Page. Pages implementing a form should inhert from it"""

    __metaclass__ = FormBase

    form_builder = FormBuilder
    is_abstract = True  # Don't display me in "Add"

    def __init__(self, *args, **kwargs):
        super(AbstractForm, self).__init__(*args, **kwargs)
        if not hasattr(self, 'landing_page_template'):
            template_wo_ext = re.match(HTML_EXTENSION_RE, self.template).group(1)
            self.landing_page_template = template_wo_ext + '_landing.html'

    class Meta:
        abstract = True

    def serve(self, request):
        fb = self.form_builder(self.form_fields.all())
        form_class = fb.get_form_class()

        if request.method == 'POST':
            self.form = form_class(request.POST)

            if self.form.is_valid():
                # remove csrf_token from form.data
                form_data = dict(
                    i for i in self.form.data.items()
                    if i[0] != 'csrfmiddlewaretoken'
                )

                submission = FormSubmission.objects.create(
                    form_data=json.dumps(form_data),
                    form_page=self,
                    user=request.user,
                )

                # If we have a form_processing_backend call its process method
                if hasattr(self, 'form_processing_backend'):
                    form_processor = self.form_processing_backend()
                    form_processor.process(self, self.form)

                # render the landing_page
                # TODO: It is much better to redirect to it
                return render(request, self.landing_page_template, {
                    'self': self,
                })
        else:
            self.form = form_class()

        return render(request, self.template, {
            'self': self,
            'form': self.form,
        })


class AbstractEmailForm(AbstractForm):
    """A Form Page that sends email. Pages implementing a form to be send to an email should inherit from it"""
    is_abstract = True  # Don't display me in "Add"
    form_processing_backend = EmailFormProcessor

    to_address = models.CharField(max_length=255, )
    from_address = models.CharField(max_length=255, blank=True)
    subject = models.CharField(max_length=255, )

    class Meta:
        abstract = True


# TEST
class ConcreteFormFields(AbstractFormFields):
    page = ParentalKey('wagtailforms.ConcreteForm', related_name='form_fields')


class ConcreteForm(AbstractForm):
    thank_you = models.CharField(max_length=255)

ConcreteForm.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('thank_you', classname="full"),
    InlinePanel(ConcreteForm, 'form_fields', label="Form Fields"),
]


class ConcreteEmailFormFields(AbstractFormFields):
    page = ParentalKey('wagtailforms.ConcreteEmailForm', related_name='form_fields')


class ConcreteEmailForm(AbstractEmailForm):
    thank_you = models.CharField(max_length=255)

ConcreteEmailForm.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('thank_you', classname="full"),
    FieldPanel('to_address', classname="full"),
    FieldPanel('from_address', classname="full"),
    FieldPanel('subject', classname="full"),
    InlinePanel(ConcreteEmailForm, 'form_fields', label="Form Fields"),
]
