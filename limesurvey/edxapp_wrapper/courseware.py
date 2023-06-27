"""
Courseware generalized definitions.
"""

from importlib import import_module
from django.conf import settings


def get_object_by_usage_id_function(*args, **kwargs):
    """Get the block object for the given block usage id."""

    backend_function = settings.LIMESURVEY_COURSEWARE_BACKEND
    backend = import_module(backend_function)

    return backend.get_object_by_usage_id(*args, **kwargs)


get_object_by_usage_id = get_object_by_usage_id_function()
