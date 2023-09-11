"""XBlock to embed a LimeSurvey survey in Open edX."""
from __future__ import annotations

import logging
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Tuple

import pkg_resources
import pytz
import requests
from django.conf import settings
from django.utils import translation
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Boolean, DateTime, Integer, Scope, String
from xblockutils.resources import ResourceLoader

from limesurvey.utils import _

log = logging.getLogger(__name__)
loader = ResourceLoader(__name__)

class LimeSurveyAPIError(Exception):
    """Exception raised when the LimeSurvey API returns an error."""

    def __init__(self, message=_("LimeSurvey API error.")):
        """Initialize the exception.

        args:
            message: The error message for the LimeSurvey API error.
        """
        super().__init__(message)

class NoParticipantFound(LimeSurveyAPIError):
    """Exception raised when no participant is found for the user."""

    def __init__(self, message=_("No participant in the survey.")):
        """Initialize the exception.

        args:
            message: The error message for the no participant error.
        """
        super().__init__(message)


class ExceededLoginAttempts(LimeSurveyAPIError):
    """Exception raised when the user has exceeded the number of login attempts."""

    def __init__(self, message=_("Exceeded the number of login attempts.")):
        """Initialize the exception.

        args:
            message: The error message for the exceeded login attempts error.
        """
        super().__init__(message)


class InvalidSessionKey(LimeSurveyAPIError):
    """Exception raised when the session key is expired."""

    def __init__(self, message=_("Invalid session key.")):
        """Initialize the exception.

        args:
            message: The error message for the invalid session key error.
        """
        super().__init__(message)



class InvalidCredentials(LimeSurveyAPIError):
    """Exception raised when the credentials are invalid."""

    def __init__(self, message=_("Invalid credentials to authenticate with LimeSurvey API.")):
        """Initialize the exception.

        args:
            message: The error message for the invalid credentials error.
        """
        super().__init__(message)


class MisconfiguredLimeSurveyService(Exception):
    """Exception raised when the survey service is misconfigured."""

    def __init__(self, message=_("Survey service is misconfigured.")):
        """Initialize the exception.

        args:
            message: The error message for the misconfigured survey service error.
        """
        super().__init__(message)


API_EXCEPTIONS_MAPPING = defaultdict(lambda: LimeSurveyAPIError)
API_EXCEPTIONS_MAPPING["Invalid session key"] = InvalidSessionKey
API_EXCEPTIONS_MAPPING["No survey participants found."] = NoParticipantFound
API_EXCEPTIONS_MAPPING["Invalid user name or password"] = InvalidCredentials


@XBlock.wants("user")
@XBlock.needs("i18n")
class LimeSurveyXBlock(XBlock):
    """
    LimeSurvey XBlock provides a way to embed surveys from LimeSurvey in a course.
    """

    display_name = String(
        display_name=_("Display name"),
        default="LimeSurvey",
        scope=Scope.settings,
        help=_(
            "The display name for this component. Please, use a distinctive name, "
            "as it will be used to identify the component in the LimeSurvey tab of "
            "the instructor dashboard when enabled."
        ),
    )

    survey_id = Integer(
        default=0,
        scope=Scope.settings,
        help=_(
            "The ID of the survey to be embedded. You can find the ID in the URL of "
            "the survey. For example, if the URL is https://limesurvey.example.com/index.php/123456?lang=en"
            ", the survey ID is 123456."
        ),
    )

    anonymous_survey = Boolean(
        default=False,
        scope=Scope.settings,
        help=_(
            "Whether the survey is set to be public for everyone (open-access mode) or invite only (closed-access mode)"
            "in the LimeSurvey administration console. When the Survey is closed-access, make sure that an additional attribute "
            "is created in the Survey's participants table. This new field is needed to store the learner's anonymized id."
        ),
    )

    limesurvey_url = String(
        display_name=_("LimeSurvey URL"),
        default="",
        scope=Scope.settings,
        help=_(
            "The URL of the LimeSurvey service, including the https scheme and without "
            "the trailing slash. If not set, it will be taken from the service "
            "configurations. Here is an example: https://limesurvey.example.com"
        ),
    )

    api_username = String(
        display_name=_("API username"),
        default="",
        scope=Scope.settings,
        help=_(
            "The username to authenticate with the LimeSurvey service."
            "Leave this field empty to use the default configurations."
        ),
    )

    api_password = String(
        display_name=_("API user's password"),
        default="",
        scope=Scope.settings,
        help=_(
            "The password to authenticate with the LimeSurvey service. "
            "Leave this field empty to use the default configurations."
        ),
    )

    session_key = String(
        default=None,
        scope=Scope.user_state_summary,
        help=_("Authentication key for the LimeSurvey API"),
    )

    survey_url = String(
        default=None,
        scope=Scope.user_state_summary,
        help=_("The URL of the survey for the current student."),
    )

    limesurvey_internal_api = String(
        default="",
        scope=Scope.settings,
        help=_(
            "The URL of the LimeSurvey internal API, it's calculated from the "
            "LimeSurvey URL after saving the XBlock in Studio. If the LimeSurvey "
            "URL is not set, this configuration will be taken from the service "
            "configurations."
        ),
    )

    access_code = String(
        default=None,
        scope=Scope.user_state,
        help=_("The access code of the user for the survey"),
    )

    last_login_attempt = DateTime(
        default=None,
        scope=Scope.user_state,
        help=_("The time of the last login attempt"),
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def render_template(self, template_path, context=None) -> str:
        """
        Render a template with the given context. The template is translated
        according to the user's language.

        args:
            template_path: The path to the template
            context: The context to render in the template

        returns:
            The rendered template
        """
        return loader.render_django_template(
            template_path, context, i18n_service=self.runtime.service(self, 'i18n')
        )

    def user_is_staff(self, user) -> bool:
        """
        Check whether the user has course staff permissions for this XBlock.
        """
        return user.opt_attrs.get("edx-platform.user_is_staff")

    def is_student(self, user) -> bool:
        """
        Check if the user is a student.
        """
        return user.opt_attrs.get("edx-platform.user_role") == "student"

    def anonymous_user_id(self, user) -> str:
        """
        Return the anonymous user ID of the user.
        """
        return user.opt_attrs.get("edx-platform.anonymous_user_id")

    def setup_student_view_survey(self, user, anonymous_user_id):
        """
        Setup LimeSurvey configurations for the student view of the XBlock.
        """
        limesurvey_url = self.limesurvey_url or getattr(settings, "LIMESURVEY_URL", None)
        if not limesurvey_url:
            raise MisconfiguredLimeSurveyService("LIMESURVEY_URL is not set in your service configurations.")

        self.survey_url = f"{limesurvey_url}/index.php/{self.survey_id}"

        if not self.anonymous_survey:
            self.set_session_key()
            self.add_participant_to_survey(user, anonymous_user_id)
            self.set_student_access_code(anonymous_user_id)

    def student_view(self, show_survey):
        """
        Render the primary view of the LimeSurveyXBlock, shown to students when viewing courses.
        """
        user_service = self.runtime.service(self, "user")
        user = user_service.get_current_user()
        show_survey = self.is_student(user) or self.user_is_staff(user)
        anonymous_user_id = self.anonymous_user_id(user)
        error_message = None

        if show_survey:
            try:
                self.setup_student_view_survey(user, anonymous_user_id)
            except Exception as e:  # pylint: disable=broad-except
                log.exception("Error while setting up student view of LimeSurveyXBlock")
                error_message = str(e)

        context = {
            "self": self,
            "show_survey": show_survey,
            "error_message": error_message,
        }

        frag = Fragment()
        frag.add_content(self.render_template("static/html/limesurvey.html", context))
        frag.add_css(self.resource_string("static/css/limesurvey.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/limesurvey.js"))
        frag.initialize_js("LimeSurveyXBlock")
        return frag

    def studio_view(self, context=None):
        """
        The studio view of the LimeSurveyXBlock, shown to instructors.
        """
        context = {
            "display_name": self.display_name,
            "limesurvey_url": self.limesurvey_url,
            "survey_id": self.survey_id,
            "anonymous_survey": self.anonymous_survey,
            "api_username": self.api_username,
            "api_password": self.api_password,
            "survey_id_field": self.fields["survey_id"],
            "display_name_field": self.fields["display_name"],
            "anonymous_survey_field": self.fields["anonymous_survey"],
            "limesurvey_url_field": self.fields["limesurvey_url"],
            "api_username_field": self.fields["api_username"],
            "api_password_field": self.fields["api_password"],
        }

        frag = Fragment()
        frag.add_content(self.render_template(
            "static/html/limesurvey_edit.html", context
        ))
        frag.add_css(self.resource_string("static/css/limesurvey.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(
                self.runtime.local_resource_url(self, statici18n_js_url)
            )

        frag.add_javascript(self.resource_string("static/js/src/limesurveyEdit.js"))
        frag.initialize_js("LimeSurveyXBlock")
        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffix=""):  # pylint: disable=unused-argument
        """
        Called when submitting the form in Studio.
        """
        self.display_name = data.get("display_name")
        self.survey_id = data.get("survey_id")
        self.limesurvey_url = data.get("limesurvey_url")
        if self.limesurvey_url:
            self.limesurvey_url = self.limesurvey_url.rstrip("/")
            self.limesurvey_internal_api = f"{self.limesurvey_url}/index.php/admin/remotecontrol"
        self.api_username = data.get("api_username", "")
        self.api_password = data.get("api_password", "")
        self.anonymous_survey = bool(data.get("anonymous_survey"))

    def get_survey_summary(self) -> dict:
        """
        Get the summary of the current configured survey.
        """
        params = {
            "survey_id": self.survey_id,
        }

        return self.call_procedure("get_summary", *params.values())

    def check_user_in_survey(self, anonymous_user_id: str) -> bool:
        """
        Check if the user is already in the survey.
        - `params` variable is a dict of parameters to pass to the API call.
            - survey_id: The ID of the survey
            - start: Retrieve participants starting from this index
            - limit: Maximum number of participants to retrieve
            - unused: Retrieve only participants with unused tokens
            - attributes: List with extra participant attributes to retrieve
            - conditions: Dictionary of conditions to filter participants

        args:
            anonymous_user_id (str): The anonymous user ID of the user

        Returns:
            bool: True if the user is in the survey, False otherwise
        """
        params = {
            "survey_id": self.survey_id,
            "start": 0,
            "limit": 1,
            "unused": False,
            "attributes": ["attribute_1"],
            "conditions": {"attribute_1": anonymous_user_id},
        }

        response = self.call_procedure("list_participants", *params.values())

        if isinstance(response, list):
            return len(response) > 0

        return False

    def set_student_access_code(self, anonymous_user_id) -> str:
        """
        Return the access code for the current user.

        args:
            anonymous_user_id: The anonymous user ID of the user

        returns:
            The access code for the user
        """
        response = self.call_procedure(
            "get_participant_properties",
            self.survey_id,
            {"attribute_1": anonymous_user_id}
        )

        self.access_code = response.get("token", "")

    @staticmethod
    def get_fullname(user) -> Tuple[str, str]:
        """
        Return the full name of the user.

        args:
            user: The user to get the fullname

        returns:
            A tuple containing the first name and last name of the user
        """
        first_name, last_name = "", ""

        if user.full_name:
            fullname = user.full_name.split(" ", 1)
            first_name = fullname[0]

            if fullname[1:]:
                last_name = fullname[1]

        return first_name, last_name

    def add_participant_to_survey(self, user, anonymous_user_id: str):
        """
        Add the student as participant to specified survey.

        args:
            user: The user to add as participant
            anonymous_user_id: The anonymous user ID of the user
        """
        try:
            self.check_user_in_survey(anonymous_user_id)
            return None
        except NoParticipantFound:
            pass

        firstname, lastname = self.get_fullname(user)

        participant = {
            "email": user.emails[0],
            "lastname": lastname,
            "firstname": firstname,
            "attribute_1": anonymous_user_id,
        }

        return self.call_procedure("add_participants", self.survey_id, [participant])

    def set_session_key(self) -> None:
        """
        Set the session key for the LimeSurvey API when expires.
        """
        try:
            # Check first if the current session key is still valid
            self.get_survey_summary()
            return
        except InvalidSessionKey:
            pass

        current_time = datetime.now().replace(tzinfo=pytz.utc)
        login_attempts_exceeded = self.last_login_attempt and \
        self.last_login_attempt > current_time - timedelta(
            minutes=getattr(
                settings, "LIMESURVEY_LOGIN_ATTEMPTS_TIMEOUT", 5,
            )
        )
        if login_attempts_exceeded:
            raise ExceededLoginAttempts

        self.last_login_attempt = datetime.now()
        limesurvey_api_user = self.api_username or getattr(settings, "LIMESURVEY_API_USER", None)
        limesurvey_api_password = self.api_password or getattr(settings, "LIMESURVEY_API_PASSWORD", None)
        if not limesurvey_api_user or not limesurvey_api_password:
            raise MisconfiguredLimeSurveyService(
                _("LimeSurvey API user or password not configured")
            )

        session_key = self.call_procedure(
            "get_session_key",
            limesurvey_api_user,
            limesurvey_api_password,
            get_session_key=True,
        )

        if isinstance(session_key, str):
            self.session_key = session_key

    def call_procedure(self, method: str, *params, get_session_key=False) -> dict | None:
        """
        Invoke a method on the LimeSurvey API.

        Arguments:
            method: The method to invoke
            params: The parameters to pass to the method
            get_session_key: True if the method is get_session_key, False otherwise

        Returns:
            The response from the API.

        Raises:
            LimeSurveyAPIError: If the API call fails.
            An exception from API_EXCEPTIONS_MAPPING if matches the error message.
        """
        limesurvey_api_url = self.limesurvey_internal_api or getattr(settings, "LIMESURVEY_INTERNAL_API", None)
        if not limesurvey_api_url:
            raise LimeSurveyAPIError(_(
                "LimeSurvey URL for the service API is not set in "
                "your service configurations or in the XBlock."
            ))

        if get_session_key:
            params = [*params]
        else:
            params = [self.session_key, *params]

        payload = {
            "method": method,
            "params": params,
            "id": uuid.uuid4().hex,
        }

        response = requests.post(
            url=limesurvey_api_url,
            json=payload,
            timeout=getattr(settings, "LIMESURVEY_API_TIMEOUT", 5),
        )

        if not response.ok:
            raise LimeSurveyAPIError(response.text)

        result = response.json().get("result")

        if not isinstance(result, dict):
            return result

        if result.get("status") not in ("OK", None):
            log.error("LimeSurvey API error: %s", result.get("status"))
            raise API_EXCEPTIONS_MAPPING[result.get("status")]

        return result

    def instructor_view(self, context: dict):
        """
        The studio view of the LimeSurveyXBlock, shown to instructors.
        """
        frag = Fragment()
        frag.add_content(self.render_template("static/html/instructor.html", context))
        frag.add_css(self.resource_string("static/css/instructor.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(
                self.runtime.local_resource_url(self, statici18n_js_url)
            )

        frag.add_javascript(self.resource_string("static/js/src/instructor.js"))
        frag.initialize_js("LimeSurveyTab")
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """Return a canned scenario for display in the workbench."""
        return [
            ("LimeSurveyXBlock",
             """<limesurvey/>
             """),
            ("Multiple LimeSurveyXBlock",
             """<vertical_demo>
                <limesurvey/>
                <limesurvey/>
                <limesurvey/>
                </vertical_demo>
             """),
        ]

    @staticmethod
    def _get_statici18n_js_url():
        """
        Return the Javascript translation file for the currently selected language, if any.

        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = 'public/js/translations/{locale_code}/text.js'
        lang_code = locale_code.split('-')[0]
        for code in (locale_code, lang_code, 'en'):
            if pkg_resources.resource_exists(
                    loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Return dummy method to generate initial i18n.
        """
        return translation.gettext_noop('Dummy')
