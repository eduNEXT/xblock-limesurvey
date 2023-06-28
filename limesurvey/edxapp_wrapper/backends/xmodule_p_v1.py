"""
Xmodule definitions for Open edX Palm release.
"""
from xmodule.modulestore.django import modulestore

def get_modulestore(*args, **kwargs):
    """
    Get the modulestore object.
    """
    return modulestore(*args, **kwargs)
