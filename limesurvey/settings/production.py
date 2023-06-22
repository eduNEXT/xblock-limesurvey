"""
Settings for the LimeSurvey plugin.
"""

def plugin_settings(settings):
    """
    Read / Update necessary project settings for production envs.
    """
    settings.LIMESURVEY_API_USER = getattr(settings, 'ENV_TOKENS', {}).get(
        'LIMESURVEY_API_USER',
        settings.LIMESURVEY_API_USER
    )
    settings.LIMESURVEY_API_PASSWORD = getattr(settings, 'ENV_TOKENS', {}).get(
        'LIMESURVEY_API_PASSWORD',
        settings.LIMESURVEY_API_PASSWORD
    )
