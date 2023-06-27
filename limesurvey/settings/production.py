"""
Settings for the LimeSurvey plugin.
"""
from limesurvey import LIMESURVEY_ROOT_DIRECTORY


def plugin_settings(settings):
    """
    Read / Update necessary project settings for production envs.
    """
    settings.MAKO_TEMPLATE_DIRS_BASE.append(LIMESURVEY_ROOT_DIRECTORY / "templates")
    # Timeout configured to 5s as the average timeout for regular HTTP request
    settings.LIMESURVEY_API_TIMEOUT = getattr(settings, "ENV_TOKENS", {}).get(
        "LIMESURVEY_API_TIMEOUT",
        settings.LIMESURVEY_API_TIMEOUT
    )
    settings.LIMESURVEY_API_USER = getattr(settings, "ENV_TOKENS", {}).get(
        "LIMESURVEY_API_USER",
        settings.LIMESURVEY_API_USER
    )
    settings.LIMESURVEY_API_PASSWORD = getattr(settings, "ENV_TOKENS", {}).get(
        "LIMESURVEY_API_PASSWORD",
        settings.LIMESURVEY_API_PASSWORD
    )

    # Limesurvey backend settings
    settings.LIMESURVEY_COURSEWARE_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "LIMESURVEY_COURSEWARE_BACKEND",
        settings.LIMESURVEY_COURSEWARE_BACKEND
    )
    settings.LIMESURVEY_XMODULE_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "LIMESURVEY_XMODULE_BACKEND",
        settings.LIMESURVEY_XMODULE_BACKEND
    )
