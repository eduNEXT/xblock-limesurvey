"""
Settings for the LimeSurvey plugin.
"""

def plugin_settings(settings):
    """
    Read / Update necessary project settings for testing.
    """
    settings.LIMESURVEY_API_USER = "admin"
    settings.LIMESURVEY_API_PASSWORD = "admin"
