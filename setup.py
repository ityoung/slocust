import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'slocust', '__version__.py'),
          'r', encoding='utf-8') as f:
    exec(f.read(), about)

packages = ['slocust']

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    license=about['__license__'],
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=packages,
    include_package_data=True,
    platforms='any',
    install_requires=requires,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: Testers',
    ] + [
        ('Programming Language :: Python :: %s' % x)
        for x in '3.5 3.6'.split()
    ],
    entry_points={
        'console_scripts': [
            'slocust = slocust:main',
        ]
    },
)
