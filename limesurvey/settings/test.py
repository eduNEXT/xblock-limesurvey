"""
Settings for the LimeSurvey plugin for testing purposes.
"""

# SECURITY WARNING: keep the secret key used in production secret!
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "default.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
    "read_replica": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "read_replica.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}


INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "limesurvey",
)


SECRET_KEY = "not-so-secret-key"

# Internationalization
# https://docs.djangoproject.com/en/2.22/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_TZ = True

# LimeSurvey API credentials
LIMESURVEY_API_USER = "test-user"
LIMESURVEY_API_PASSWORD = "test-password"

# LimeSurvey API timeout
LIMESURVEY_API_TIMEOUT = 5

# LimeSurvey URL
LIMESURVEY_URL = "https://test-url.com"

# LimeSurvey internal survey URL
LIMESURVEY_INTERNAL_API = "https://test-url.com/index.php/admin/remotecontrol"
