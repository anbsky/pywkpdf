# encoding=utf-8

from os import path
from django.http import HttpResponse
from django.template import Template, Context, RequestContext
from django.template.loader import select_template, get_template, render_to_string
from django.conf import settings
from wsgiref.util import FileWrapper

from . import html_to_pdf, html_to_pdf_file


def render_to_pdf(template_name, dictionary=None,
                  context_instance=None, convert_args=None):
    convert_args = convert_args or {}
    html = _render_template(template_name, dictionary, context_instance)
    return html_to_pdf(html, **convert_args)


def render_to_file(template_name, file_name, dictionary=None,
                   context_instance=None, convert_args=None):
    convert_args = convert_args or {}
    html = _render_template(template_name, dictionary, context_instance)
    return html_to_pdf_file(html, file_name, **convert_args)


def render_to_response(request, template_name, dictionary=None,
                       file_name=None, convert_args=None):
    pdf_file = render_to_pdf(
        template_name, dictionary, RequestContext(request), convert_args)
    file_name = file_name or path.basename(pdf_file.name)

    response = HttpResponse(FileWrapper(pdf_file), content_type='application/pdf')
    if file_name:
        response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(
            file_name)
    else:
        response['Content-Disposition'] = 'attachment'
    response['Content-Length'] = pdf_file.tell()
    pdf_file.seek(0)

    return response


def _render_template(template_name, dictionary, context_instance):
    new_dictionary = {
        'STATIC_URL': settings.STATIC_ROOT,
        'PROJECT_PATH': settings.PROJECT_PATH
    }
    if dictionary:
        new_dictionary.update(dictionary)
    return render_to_string(template_name, new_dictionary, context_instance)