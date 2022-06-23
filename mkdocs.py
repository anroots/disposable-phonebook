"""
Mkdocs-macros module
https://mkdocs-macros-plugin.readthedocs.io/en/latest/macros/
"""
from dphonebook.lib.providers import number_provider_classes


def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

    env.variables['dphonebook_providers'] = number_provider_classes
