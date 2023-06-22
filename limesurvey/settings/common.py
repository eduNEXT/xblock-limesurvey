"""
Settings for the LimeSurvey plugin.
"""
from limesurvey import LIMESURVEY_ROOT_DIRECTORY


def plugin_settings(settings):
    """
    Read / Update necessary project settings.
    """
    settings.MAKO_TEMPLATE_DIRS_BASE.append(LIMESURVEY_ROOT_DIRECTORY / "templates")
    settings.LIMESURVEY_API_TIMEOUT = 5 # average timeout for regular HTTP request

    settings.LIMESURVEY_API_USER = getattr(settings, 'ENV_TOKENS', {}).get(
        'LIMESURVEY_API_USER',
        settings.LIMESURVEY_API_USER
    )
    settings.LIMESURVEY_API_PASSWORD = getattr(settings, 'ENV_TOKENS', {}).get(
        'LIMESURVEY_API_PASSWORD',
        settings.LIMESURVEY_API_PASSWORD
    )
