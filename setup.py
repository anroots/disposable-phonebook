from setuptools import find_packages
from setuptools import setup

setup(
    name='Disposable phonebook',
    packages=find_packages(),
    include_package_data=True,
    version='0.1.0',
    py_modules=['dphonebook.cli'],
    install_requires=[
        'requests',
        'click',
        'setuptools',
        'beautifulsoup4',
        'phonenumbers'

    ],
    entry_points={
        'console_scripts': [
            'dphonebook = dphonebook.cli:main',
        ],
    },
)
