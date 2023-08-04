"""
Settings for the LimeSurvey plugin.
"""
from limesurvey import LIMESURVEY_ROOT_DIRECTORY


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    settings.MAKO_TEMPLATE_DIRS_BASE.append(LIMESURVEY_ROOT_DIRECTORY / "templates")
    # Timeout configured to 5s as the average timeout for regular HTTP request
    settings.LIMESURVEY_API_TIMEOUT = 5
    settings.LIMESURVEY_API_USER = None
    settings.LIMESURVEY_API_PASSWORD = None

    # Limesurvey backend settings
    settings.LIMESURVEY_COURSEWARE_BACKEND = "limesurvey.edxapp_wrapper.backends.courseware_p_v1"
    settings.LIMESURVEY_XMODULE_BACKEND = "limesurvey.edxapp_wrapper.backends.xmodule_p_v1"
