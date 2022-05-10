from setuptools import setup, find_packages

setup(
    name='Disposable phonebook',
    packages=find_packages(),
    include_package_data=True,
    version='0.1.0',
    py_modules=['dphonebook.cli'],
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'dphonebook = dphonebook.cli:main',
        ],
    },
)
