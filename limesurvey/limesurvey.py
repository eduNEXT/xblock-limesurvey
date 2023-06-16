"""TO-DO: Write a description of what this XBlock is."""
from __future__ import annotations
import pkg_resources
import requests
from django.utils import translation
from django.conf import settings
from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader


class LimeSurveyXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    display_name = String(
        display_name="Display Name",
        default="LimeSurvey",
        scope=Scope.settings
    )

    survey_id = Integer(
        default=0,
        scope=Scope.settings,
        help="The ID of the survey to be embedded",
    )

    access_key = String(
        default=None,
        scope=Scope.settings,
        help="Authentication key for the LimeSurvey API",
    )

    survey_url = String(
        default=None,
        scope=Scope.user_state_summary,
        help="The URL of the survey",
    )

    access_code = String(
        default=None,
        scope=Scope.user_state,
        help="The access code of the user for the survey",
    )

    error_message = String(
        default=None,
        scope=Scope.user_state,
        help="The error message to display to the user",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        Render the primary view of the LimeSurveyXBlock, shown to students when viewing courses.
        """
        if context:
            pass  # TO-DO: do something based on the context.

        limesurvey_api_url = getattr(settings, "LIMESURVEY_INTERNAL_API", None)

        if limesurvey_api_url:
            anonymous_user_id = self.runtime.anonymous_student_id
            if response := self.valid_session_key(anonymous_user_id) is not False:
                if not self.user_in_survey(response):
                    self.add_participant_to_survey(
                        self.runtime.get_real_user(anonymous_user_id),
                        anonymous_user_id,
                )
                self.get_survey(anonymous_user_id)

        html = self.resource_string("static/html/limesurvey.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/limesurvey.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/limesurvey.js"))
        frag.initialize_js("LimeSurveyXBlock")
        return frag

    def studio_view(self, _context=None):
        """
        The studio view of the LimeSurveyXBlock, shown to instructors.
        """
        html = self.resource_string("static/html/limesurvey_edit.html")
        frag = Fragment(
            html.format(
                access_key=self.access_key,
                survey_id=self.survey_id,
                display_name=self.display_name,
            ),
        )
        frag.add_css(self.resource_string("static/css/limesurvey.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/limesurveyEdit.js"))
        frag.initialize_js("LimeSurveyXBlock")
        return frag

    @XBlock.json_handler
    def studio_submit(self, data, suffix=""):  # pylint: disable=unused-argument
        """
        Called when submitting the form in Studio.
        """
        self.display_name = data.get("display_name")
        self.access_key = data.get("access_key")
        self.survey_id = data.get("survey_id")

        return {
            "result": "success",
        }

    def get_survey(self, anonymous_user_id: str):
        """
        Return the survey URL and access code for the user.
        
        args:
            anonymous_user_id (str): The anonymous user ID of the user
        """
        self.survey_url = f"{settings.LIMESURVEY_URL}/{self.survey_id}"
        self.access_code = self.get_student_access_code(anonymous_user_id)

    def user_in_survey(self, response: dict) -> bool:
        """
        Check if the user is already in the survey.

        args:
            response (dict): The response from the API

        Returns:
            bool: True if the user is in the survey, False otherwise
        """
        if isinstance(response.get("result"), list):
            return len(response.get("result", 0)) > 0

        return False

    def valid_session_key(self, anonymous_user_id: str) -> bool | dict:
        """
        Check if the session key is valid.

        Args:
            anonymous_user_id (str): The anonymous user ID of the user
        """
        params = [
            self.survey_id, 0, 1, False,
            ["attribute_1"], {"attribute_1": anonymous_user_id}
        ]

        return self._invoke("list_participants", *params)

    def get_student_access_code(self, anonymous_user_id):
        """
        Return the access code for the current user.
        
        args:
            anonymous_user_id (str): The anonymous user ID of the user
        """
        limesurvey_api_url = getattr(settings, "LIMESURVEY_INTERNAL_API", None)
        if not limesurvey_api_url:
            return False

        response = self._invoke(
            "get_participant_properties",
            self.survey_id,
            {"attribute_1": anonymous_user_id}
        )

        return response.get("result", {}).get("token")

    def add_participant_to_survey(self, user, anonymous_user_id: str):
        """
        Add the student as participant to specified survey.

        args:
            user: The user to add as participant
            anonymous_user_id (str): The anonymous user ID of the user
        """
        firstname, lastname = None, None

        if user.profile.name is not None:
            fullname = user.profile.name.split()
            if len(fullname) > 1:
                firstname, lastname = fullname
            else:
                firstname = fullname[0]

        participant = {
            "email": user.email,
            "lastname": lastname,
            "firstname": firstname,
            "attribute_1": anonymous_user_id,
        }

        self._invoke("add_participants", self.survey_id, [participant])

    def _invoke(self, method: str, *params) -> dict | bool:
        """
        Invoke a method on the LimeSurvey API.

        args:
            method (str): The method to invoke
            params (*args): The parameters to pass to the method

        returns:
            The response from the API
        """
        payload = {
            "method": method,
            "params": [self.access_key, *params],
            "id": 1,
        }

        response = requests.post(
            settings.LIMESURVEY_INTERNAL_API,
            json=payload,
            timeout=1,
        )

        if response.status_code != requests.status_codes.codes.ok: # pylint: disable=no-member
            raise Exception(response.text)

        json_response = response.json()

        if "status" in json_response.get("result", {}):
            self.error_message = json_response.get("result").get("status")
            return False

        return json_response

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
            loader = ResourceLoader(__name__)
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
