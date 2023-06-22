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
    settings.LIMESURVEY_API_USER = "admin"
    settings.LIMESURVEY_API_PASSWORD = "LrciIgIv"
