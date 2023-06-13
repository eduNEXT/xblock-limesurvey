"""
LimeSurvey Django application initialization.
"""

from django.apps import AppConfig


class LimeSurveyConfig(AppConfig):
    """
    Configuration for the LimeSurvey Django application.
    """

    name = "limesurvey"
    plugin_app = {
            "settings_config": {
                "lms.djangoapp": {
                    "common": {"relative_path": "settings.common"},
                },
                "cms.djangoapp": {
                    "common": {"relative_path": "settings.common"},
            },
        }
    }
