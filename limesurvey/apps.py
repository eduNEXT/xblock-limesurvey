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
                    "test": {"relative_path": "settings.test"},
                    "production": {"relative_path": "settings.production"},
                },
                "cms.djangoapp": {
                    "common": {"relative_path": "settings.common"},
                    "test": {"relative_path": "settings.test"},
                    "production": {"relative_path": "settings.production"},
            },
        }
    }
