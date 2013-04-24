# encoding=utf-8

from django.template import Template, Context
from django.template.loader import select_template, get_template, render_to_string
from django.conf import settings

from . import html_to_pdf, html_to_pdf_file


def render_to_pdf(template_name, dictionary=None, context_instance=None):
    new_dictionary = {
        'STATIC_URL': settings.STATIC_URL,
        'PROJECT_PATH': settings.PROJECT_PATH
    }
    new_dictionary.update(dictionary)
    result = render_to_string(template_name, new_dictionary, context_instance)

    return html_to_pdf(result)


def render_to_file(template_name, file_name, dictionary=None, context_instance=None):
    new_dictionary = {
        'STATIC_URL': settings.STATIC_URL,
        'PROJECT_PATH': settings.PROJECT_PATH
    }
    new_dictionary.update(dictionary)
    result = render_to_string(template_name, new_dictionary, context_instance)

    return html_to_pdf_file(result, file_name)


class PDFTemplate(Template):
    def render(self, context):
        context.update({
            'STATIC_URL': settings.STATIC_URL,
            'PROJECT_PATH': settings.PROJECT_PATH}
        )
        result = super(PDFTemplate, self).render(context)
        return result