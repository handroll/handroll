# Copyright (c) 2014, Matt Layman
'''
handroll development is on `GitHub <https://github.com/mblayman/handroll>`_.

handroll is a static website generator that uses Markdown as the source format.
'''

from setuptools import find_packages, setup
import sys

__version__ = '1.1'

if __name__ == '__main__':
    with open('docs/releases.rst', 'r') as f:
        releases = f.read()

    long_description = __doc__ + '\n\n' + releases

    install_requires = [
        'argparse',
        'Markdown',
        'Pygments',
        'textile',
    ]

    # Add some developer tools.
    if 'develop' in sys.argv:
        install_requires.extend([
            'coverage',
            'nose',
            'Sphinx',
            'tox',
        ])

    setup(
        name='handroll',
        version=__version__,
        url='https://github.com/mblayman/handroll',
        license='BSD',
        author='Matt Layman',
        author_email='matthewlayman@gmail.com',
        description='A website generator for software artisans',
        long_description=long_description,
        packages=find_packages(),
        entry_points={
            'console_scripts': ['handroll = handroll.command:main'],
            'handroll.composers': [
                '.md = handroll.composers:MarkdownComposer',
                '.textile = handroll.composers.txt:TextileComposer',
            ]
        },
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=install_requires,
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
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
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
            'Textile',
        ],
    )
