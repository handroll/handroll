# Copyright (c) 2015, Matt Layman
"""
Learn more about handroll at the `project home page
<http://handroll.github.io>`_. handroll development is done on `GitHub
<https://github.com/handroll/handroll>`_. Announcements and discussions happen
on `Google Groups <https://groups.google.com/forum/#!forum/handroll>`_.

handroll is a static website generator that uses markup languages like
Markdown, ReStructuredText, and Textile.
"""

from setuptools import find_packages, setup
from setuptools.command.sdist import sdist
import sys

__version__ = '1.6'


class Sdist(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created."""

    def run(self):
        self.run_command('compile_catalog')
        # sdist is an old style class so super cannot be used.
        sdist.run(self)

if __name__ == '__main__':
    with open('docs/releases.rst', 'r') as f:
        releases = f.read()

    long_description = __doc__ + '\n\n' + releases

    install_requires = [
        'argparse',  # For Python 2.6 support
        'blinker',
        'docutils',
        'Jinja2',
        'Markdown==2.4',  # 2.5 dropped support for Python 2.6.
        'mock',
        'Pygments',
        'PyYAML',
        'textile',
        'watchdog',
        'werkzeug',
    ]

    # Add some developer tools.
    if 'develop' in sys.argv:
        install_requires.extend([
            'Babel',
            'coverage',
            'flake8',
            'nose',
            'requests',
            'Sphinx',
            'tox',
        ])

    setup(
        name='handroll',
        version=__version__,
        url='http://handroll.github.io',
        license='BSD',
        author='Matt Layman',
        author_email='matthewlayman@gmail.com',
        description='A website generator for software artisans',
        long_description=long_description,
        packages=find_packages(),
        entry_points={
            'console_scripts': ['handroll = handroll.command:main'],
            'handroll.composers': [
                '.atom = handroll.composers.atom:AtomComposer',
                '.md = handroll.composers.md:MarkdownComposer',
                '.rst = handroll.composers.rst:ReStructuredTextComposer',
                '.sass = handroll.composers.sass:SassComposer',
                '.scss = handroll.composers.sass:SassComposer',
                '.textile = handroll.composers.txt:TextileComposer',
            ],
            'handroll.extensions': [
                'blog = handroll.extensions.blog:BlogExtension',
            ]
        },
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=install_requires,
        setup_requires=[
            'Babel',  # sdist compiles po into mo.
        ],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Artistic Software',
            'Topic :: Documentation',
            'Topic :: Internet :: WWW/HTTP :: Site Management',
            'Topic :: Office/Business :: News/Diary',
            'Topic :: Software Development :: Documentation',
            'Topic :: Text Processing :: Markup :: HTML',
        ],
        keywords=[
            'generator',
            'Markdown',
            'ReStructuredText',
            'Textile',
        ],
        cmdclass={'sdist': Sdist},
    )
