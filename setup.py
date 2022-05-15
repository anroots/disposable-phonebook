from setuptools import find_packages
from setuptools import setup

setup(
    name='disposable-phonebook',
    description='Scraper for disposable phone number services',
    long_description=open('README.md').read(),
    url='https://github.com/anroots/disposable-phonebook',
    project_urls={
        'Documentation': 'https://anroots.github.io/disposable-phonebook/',
        'Source Code': 'https://github.com/anroots/disposable-phonebook'
    },
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Telephony'
    ],
    setup_requires='setuptools',
    license='Apache 2.0',
    packages=find_packages(exclude=['tests*']),
    package_data={
        'dphonebook': ['disposable-phonebook.yml']
    },
    version='0.1.0',
    author='Ando Roots',
    author_email='ando@sqroot.eu',
    install_requires=[
        'requests',
        'click',
        'setuptools',
        'beautifulsoup4',
        'phonenumbers',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'dphonebook = dphonebook.cli:main',
        ],
    },
)
