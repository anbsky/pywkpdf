from distutils.core import setup

setup(
    name='pywkpdf',
    version='0.1dev',
    packages=['pywkpdf',],
    package_data={'pywkpdf': [
        'bin/wkhtmltopdf-linux',
        'bin/wkhtmltopdf.app/Contents/Info.plist',
        'bin/wkhtmltopdf.app/Contents/PkgInfo',
        'bin/wkhtmltopdf.app/Contents/MacOS/wkhtmltopdf',
        'bin/wkhtmltopdf.app/Contents/Resources/empty.lproj',
        'bin/wkhtmltopdf.app/Contents/Resources/qt.conf',
        'bin/wkhtmltopdf.app/Contents/Resources/qt_menu.nib/keyedobjects.nib',
    ]},
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    # test_suite='nose2.collector.collector',
)