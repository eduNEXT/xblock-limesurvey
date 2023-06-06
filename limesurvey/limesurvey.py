"""TO-DO: Write a description of what this XBlock is."""
from typing import Tuple

import pkg_resources
import requests
from django.utils import translation
from django.conf import settings
from django.template import Template, Context
from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblockutils.resources import ResourceLoader
from web_fragments.fragment import Fragment


@XBlock.wants("user")
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

    timeout = Integer(
        default=5,
        scope=Scope.settings,
        help="Timeout for LimeSurvey API requests",
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def render_template(self, template_path, context=None) -> str:
        """Render the template with the provided context.

        args:
            template_path: The path to the template
            context: The context to render in the template

        returns:
            The rendered template
        """
        template_str = self.resource_string(template_path)
        template = Template(template_str)
        return template.render(Context(context))

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

    def student_view(self, context=None):
        """
        Render the primary view of the LimeSurveyXBlock, shown to students when viewing courses.
        """
        user_service = self.runtime.service(self, "user")
        user = user_service.get_current_user()
        show_survey = self.is_student(user) or self.user_is_staff(user)

        if show_survey:
            anonymous_user_id = self.anonymous_user_id(user)
            self.add_participant_to_survey(user, anonymous_user_id)

        context = {"self": self, "show_survey": show_survey}
        html = self.render_template("static/html/limesurvey.html", context)
        frag = Fragment(html)
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
                timeout=self.timeout,
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
        self.timeout = data.get("timeout")

        return {
            "result": "success",
        }

    @XBlock.json_handler
    def get_survey(self, data, suffix="") -> dict: # pylint: disable=unused-argument
        """
        Return the survey URL and access code for the user.
        """
        self.survey_url = f"{settings.LIMESURVEY_URL}/{self.survey_id}"

        anonymous_user_id = self.runtime.anonymous_student_id
        self.access_code = self.get_student_access_code(anonymous_user_id)

        return {
            "survey_url": self.survey_url,
            "access_code": self.access_code,
        }

    def get_student_access_code(self, anonymous_user_id) -> str:
        """
        Return the access code for the current user.

        args:
            anonymous_user_id: The anonymous user ID of the user

        returns:
            The access code for the user
        """
        response = self._invoke(
            "get_participant_properties",
            self.survey_id,
            {"attribute_1": anonymous_user_id}
        )

        return response.get("result").get("token")

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
        firstname, lastname = self.get_fullname(user)

        participant = {
            "email": user.emails[0],
            "lastname": lastname,
            "firstname": firstname,
            "attribute_1": anonymous_user_id,
        }

        return self._invoke("add_participants", self.survey_id, [participant])

    def _invoke(self, method: str, *params) -> dict:
        """
        Invoke a method on the LimeSurvey API.

        args:
            method: The method to invoke
            params: The parameters to pass to the method

        returns:
            The response from the API
        """
        limesurvey_api_url = getattr(settings, "LIMESURVEY_INTERNAL_API", None)
        if not limesurvey_api_url:
            raise Exception("LIMESURVEY_INTERNAL_API not set")

        payload = {
            "method": method,
            "params": [self.access_key, *params],
            "id": 1,
        }

        response = requests.post(
            url=limesurvey_api_url, json=payload, timeout=self.timeout
        )

        if response.status_code != requests.status_codes.codes.ok: # pylint: disable=no-member
            raise Exception(response.text)

        return response.json()

    @XBlock.json_handler
    def get_survey_url(self, data, suffix=''): # pylint: disable=unused-argument
        """
        Show the survey URL and access code to the user
        """
        self.survey_url = f"{settings.LIMESURVEY_URL}/{self.survey_id}"
        self.access_code = "aMGZtTyFFVhhA0z"

        return {"survey_url": self.survey_url, "access_code": self.access_code}

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
