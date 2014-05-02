# Copyright (c) 2014, Matt Layman
'''
handroll development is on `GitHub <https://github.com/mblayman/handroll>`_.
'''

from setuptools import find_packages, setup
import sys

__version__ = '1.0'

if __name__ == '__main__':
    install_requires = [
        'argparse',
        'Markdown',
    ]

    # Add some developer tools.
    if 'develop' in sys.argv:
        install_requires.extend([
            'coverage',
            'nose',
        ])

    setup(
        name='handroll',
        version=__version__,
        url='https://github.com/mblayman/handroll',
        license='BSD',
        author='Matt Layman',
        author_email='matthewlayman@gmail.com',
        description='Website development is a finely crafted art.',
        long_description=__doc__,
        packages=find_packages(),
        entry_points={
            'console_scripts': ['handroll = handroll.command:main']
        },
        include_package_data=True,
        zip_safe=False,
        install_requires=install_requires,
    )
