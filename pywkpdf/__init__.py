# encoding=utf-8

import os, platform, shutil
from subprocess import call
from tempfile import NamedTemporaryFile


wkhtmltopdf_binaries = {
    'Darwin': (os.path.abspath(os.path.split(__file__)[0]) +
        '/bin/wkhtmltopdf.app/Contents/MacOS/wkhtmltopdf'),
    'Linux': (os.path.abspath(os.path.split(__file__)[0]) +
        '/bin/wkhtmltopdf-linux'),
}
wkhtmltopdf_binaries.update({
    'Darwin/x86_64': wkhtmltopdf_binaries['Darwin'],
    'Linux/x86_64': wkhtmltopdf_binaries['Linux'],
    'Linux/i386': wkhtmltopdf_binaries['Linux'],
    'Linux/i686': wkhtmltopdf_binaries['Linux'],
})

platform_type = '/'.join([platform.system(), platform.machine()])

try:
    wkhtmltopdf_cmd = wkhtmltopdf_binaries[platform_type]
except KeyError:
    raise Exception(
        'Cannot find wkhtmltopdf binary for your platform ({})'.format(platform_type))

os.chmod(wkhtmltopdf_cmd, 0755)

binary_options = {
    'low_quality': '-l',
    'quiet': '-q',
    'grayscale': '-g',
    'disable_javascript': '--disable-javascript',
}

argument_options = {
    'margin_bottom': '--margin-bottom',
    'margin_left': '--margin-left',
    'margin_top': '--margin-top',
    'orientation': '-O',
    'page_size': '-s',
    'encoding': '--encoding',
    'javascript_wait': '--javascript-delay',
    'stylesheet': '--user-style-sheet',
    'jpeg_image_quality': '--image-quality'
}

default_options = dict(
    low_quality=True, quiet=True, jpeg_image_quality=70
)


def get_options(in_file, out_file, **kwargs):
    new_kwargs = {}
    new_kwargs.update(default_options)
    new_kwargs.update(kwargs)
    options = [wkhtmltopdf_cmd]

    for k, v in new_kwargs.items():
        if isinstance(v, bool) and k in binary_options and v:
            if v:
                options.append(binary_options[k])
        elif k in argument_options:
            options.extend([argument_options[k], str(v)])
        else:
            raise ValueError('Invalid argument: {}={}'.format(k, v))
    options.extend([in_file, out_file])

    return options


def html_to_pdf(html, delete_html=True, delete_pdf=True, **kwargs):
    html_file = NamedTemporaryFile(delete=delete_html, suffix='.html')
    html_file.write(html.encode('utf-8'))
    html_file.flush()

    source = html_file.name

    pdf_file = NamedTemporaryFile(delete=delete_pdf, suffix='.pdf')

    options = get_options(source, pdf_file.name, **kwargs)
    call(options)

    html_file.close()

    return pdf_file


def html_to_pdf_file(html, to_file, **kwargs):
    pdf = html_to_pdf(html, **kwargs)
    shutil.copy(pdf.name, to_file)
    pdf.close()

    return open(to_file, 'rb')