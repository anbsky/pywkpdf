# encoding=utf-8

import os
from tempfile import NamedTemporaryFile
from nose.tools import raises

from pywkpdf import get_options, argument_options, html_to_pdf, html_to_pdf_file


def test_get_options():
    assert isinstance(get_options('a.html', 'b.pdf'), list)


@raises(ValueError)
def test_get_options_invalid_option():
    get_options('a.html', 'b.pdf', invalid_option='invalid')


@raises(ValueError)
def test_get_options_invalid_value():
    get_options('a.html', 'b.pdf', low_quality='invalid')


def test_get_options_args():
    options = get_options('a.html', 'b.pdf', javascript_wait=100)

    assert len(options) == 1 + 2 + 4 + 2
    assert argument_options['javascript_wait'] in options


def test_generate_pdf():
    pdf = html_to_pdf('<html><body><h1>Hello world</h1></body></html>')

    assert os.path.getsize(pdf.name)

    pdf.close()


def test_generate_pdf_file():
    temp_file = NamedTemporaryFile()
    pdf = html_to_pdf_file(
        '<html><body><h1>Hello world</h1></body></html>', temp_file.name)

    assert os.path.getsize(temp_file.name)

    pdf.close()
    temp_file.close()