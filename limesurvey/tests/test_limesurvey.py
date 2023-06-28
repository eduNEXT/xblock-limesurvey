"""
Tests for the LimeSurveyXBlock definition class.
"""
from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import Mock, patch

import pytz
from ddt import data, ddt, unpack
from django.conf import settings
from django.test.utils import override_settings

from limesurvey.limesurvey import (
    ExceededLoginAttempts,
    InvalidSessionKey,
    LimeSurveyAPIError,
    LimeSurveyXBlock,
    NoParticipantFound,
    MisconfiguredLimeSurveyService,
)


class TestLimeSurveyXBlock(TestCase):
    """
    Test suite for the LimeSurveyXBlock definition class.
    """

    def setUp(self) -> None:
        """
        Set up the test suite.
        """
        self.xblock = LimeSurveyXBlock(runtime=Mock(), field_data=Mock(), scope_ids=Mock())
        self.student = Mock()
        self.anonymous_user_id = "test-anonymous-user-id"
        self.xblock.anonymous_user_id = Mock()
        self.xblock.render_template = Mock(return_value="Test render")
        self.xblock.resource_string = Mock()
        self.xblock.is_student = Mock()
        self.xblock.user_is_staff = Mock()
        self.xblock.setup_student_view_survey = Mock()
        self.xblock.display_name = "Test LimeSurvey"
        self.xblock.survey_id = "test-survey-id"

    @patch("limesurvey.limesurvey.Fragment")
    def test_student_view_with_survey(self, _):
        """
        Check student view is rendered correctly.

        Expected result:
            - The student view is set up for the render with the student and the anonymous user id.
        """
        show_survey = True
        self.xblock.is_student.return_value = True
        self.xblock.runtime.service.return_value.get_current_user.return_value = self.student
        self.xblock.anonymous_user_id.return_value = self.anonymous_user_id
        expected_context = {
            "self": self.xblock,
            "show_survey": show_survey,
            "error_message": None,
        }

        self.xblock.student_view(show_survey)

        self.xblock.setup_student_view_survey.assert_called_once_with(self.student, self.anonymous_user_id)
        self.xblock.render_template.assert_called_once_with("static/html/limesurvey.html", expected_context)

    @patch("limesurvey.limesurvey.Fragment")
    def test_student_view_survey_with_errors(self, _):
        """
        Check student view is rendered correctly when an error is raised.

        Expected result:
            - An error is rendered.
        """
        show_survey = True
        self.xblock.is_student.return_value = True
        self.xblock.runtime.service.return_value.get_current_user.return_value = self.student
        self.xblock.anonymous_user_id.return_value = self.anonymous_user_id
        self.xblock.setup_student_view_survey.side_effect = Exception("Test exception")
        expected_context = {
            "self": self.xblock,
            "show_survey": show_survey,
            "error_message": "Test exception",
        }

        self.xblock.student_view(show_survey)

        self.xblock.setup_student_view_survey.assert_called_once_with(self.student, self.anonymous_user_id)
        self.xblock.render_template.assert_called_once_with("static/html/limesurvey.html", expected_context)

    @patch("limesurvey.limesurvey.Fragment")
    def test_student_view_from_studio(self, _):
        """
        Check student view is rendered correctly when called from studio.

        Expected result:
            - The student is not added as participant in the survey.
            - The survey info is not set by handler.
            - A message is rendered instead.
        """
        show_survey = False
        self.xblock.is_student.return_value = False
        self.xblock.user_is_staff.return_value = False
        self.xblock.runtime.service.return_value.get_current_user.return_value = self.student
        self.xblock.anonymous_user_id.return_value = self.anonymous_user_id
        expected_context = {
            "self": self.xblock,
            "show_survey": show_survey,
            "error_message": None,
        }

        self.xblock.student_view(show_survey)

        self.xblock.setup_student_view_survey.assert_not_called()
        self.xblock.render_template.assert_called_once_with("static/html/limesurvey.html", expected_context)

    def test_studio_view(self):
        """
        Check studio view is rendered correctly.

        Expected result:
            - The studio view is set up for the render.
        """
        expected_context = {
            "survey_id": self.xblock.survey_id,
            "display_name": self.xblock.display_name,
        }

        self.xblock.studio_view()

        self.xblock.render_template.assert_called_once_with(
            "static/html/limesurvey_edit.html",
            expected_context
        )

    def test_instructor_view(self):
        """
        Check instructor view is rendered correctly.

        Expected result:
            - The instructor view is set up for the render.
        """
        expected_context = {
            "limesurvey_url": getattr(settings, "LIMESURVEY_URL", None),
        }

        self.xblock.instructor_view()

        self.xblock.render_template.assert_called_once_with(
            "static/html/instructor.html",
            expected_context
        )


@ddt
class TestLimeSurveyUtilities(TestCase):
    """
    Test suite for the LimeSurveyXBlock utilities methods.
    """

    def setUp(self) -> None:
        """
        Set up the test suite.
        """
        self.xblock = LimeSurveyXBlock(runtime=Mock(), field_data=Mock(), scope_ids=Mock())
        self.xblock.session_key = "test-session-key"
        self.xblock.survey_id = "test-survey-id"

    @patch("limesurvey.limesurvey.uuid")
    @patch("limesurvey.limesurvey.requests")
    @data(
        (
            "get_session_key",
            [
                "test-username",
                "test-password",
            ],
            True,
        ),
        (
            "add_participants",
            [
                {
                    "email": "test-email",
                    "lastname": "test-lastname",
                    "firstname": "test-firstname",
                    "attribute_1": "test-attribute-1",
                }
            ],
            False,
        ),
        (
            "get_participant_properties",
            [
                "test-survey-id",
                {
                    "attribute_1": "test-attribute-1",
                },
            ],
            False,
        ),
        (
            "list_participants",
            [
                "test-survey-id",
                0,
                1,
                False,
                ["attribute_1"],
                {"attribute_1": "test-attribute-1"},
            ],
            False,
        ),
        (
            "get_summary",
            [
                "test-survey-id",
            ],
            False,
        )
    )
    @unpack
    def test_make_request_to_service(self, method, params, get_session_key, requests_mock, uuid_mock):
        """
        Check requests to the LimeSurvey API are made correctly.

        Expected result:
            - A request is made to the LimeSurvey API.
            - The request is made with the correct parameters.
            - The response is returned.
        """
        uuid_mock.uuid4.return_value.hex = 1
        expected_response = {"result": "test-response"}
        expected_params = params if get_session_key else [self.xblock.session_key, *params]
        requests_mock.post.return_value = Mock(status_code=200, json=Mock(return_value=expected_response))

        response = self.xblock.call_procedure(method, *params, get_session_key=get_session_key)

        requests_mock.post.assert_called_once_with(
            url=settings.LIMESURVEY_INTERNAL_API,
            json={
                "method": method,
                "params": expected_params,
                "id": 1,
            },
            timeout=settings.LIMESURVEY_API_TIMEOUT,
        )
        self.assertEqual(expected_response.get("result"), response)

    @override_settings(LIMESURVEY_INTERNAL_API=None)
    def test_limesurvey_service_not_configured(self):
        """
        When the LimeSurvey service is not configured, an exception is raised.

        Expected result:
            - An exception is raised.
        """
        method = "test_rpc_method"
        params = ["test-param-1", "test-param-2"]

        with self.assertRaises(LimeSurveyAPIError):
            self.xblock.call_procedure(method, *params)

    @patch("limesurvey.limesurvey.requests")
    @data(
        ("Invalid session key", InvalidSessionKey, True),
        ("No survey participants found.", NoParticipantFound, True),
        ("Any other error!", LimeSurveyAPIError, False),
    )
    @unpack
    def test_limesurvey_api_call_errors(self, status_message, exception, request_status_ok, requests_mock):
        """
        Check exceptions are raised when the LimeSurvey API returns an error.

        Expected result:
            - An exception is raised.
        """
        method = "test_rpc_method"
        params = ["test-param-1", "test-param-2"]
        requests_mock.post.return_value.ok = request_status_ok
        requests_mock.post.return_value.json.return_value = {
            "result": {
                "status": status_message,
            },
        }

        with self.assertRaises(exception):
            self.xblock.call_procedure(method, *params)

    @data(
            (["participant_1", "participant_2"], True),
            ([], False),
    )
    @unpack
    def test_check_user_in_survey(self, response, expected_result):
        """
        Check if a user is in a survey.

        Expected result:
            - A request is made to the LimeSurvey API checking for participants.
        """
        self.xblock.call_procedure = Mock(return_value=response)
        anonymous_user_id = "test-anonymous-user-id"
        params = {
            "survey_id": self.xblock.survey_id,
            "start": 0,
            "limit": 1,
            "unused": False,
            "attributes": ["attribute_1"],
            "conditions": {"attribute_1": anonymous_user_id},
        }

        result = self.xblock.check_user_in_survey(anonymous_user_id)

        self.xblock.call_procedure.assert_called_once_with("list_participants", *params.values())
        self.assertEqual(expected_result, result)

    def test_add_participant_to_survey(self):
        """
        Check adding a participant to a survey.

        Expected result:
            - A request is made to the LimeSurvey API adding the participant.
        """
        self.xblock.call_procedure = Mock()
        self.xblock.check_user_in_survey = Mock(side_effect=NoParticipantFound)
        anonymous_user_id = "test-anonymous-user-id"
        user = Mock(
            emails=["test-email"],
            last_name="test-lastname",
            first_name="test-firstname",
            full_name="test-firstname test-lastname",
        )
        participant = {
            "email": user.emails[0],
            "lastname": user.last_name,
            "firstname": user.first_name,
            "attribute_1": anonymous_user_id,
        }

        self.xblock.add_participant_to_survey(user, anonymous_user_id)

        self.xblock.call_procedure.assert_called_once_with(
            "add_participants",
            self.xblock.survey_id,
            [participant],
        )

    def test_set_new_session_key(self):
        """
        Check setting the session key for the LimeSurvey API.

        Expected result:
            - A request is made to the LimeSurvey API setting the session key.
        """
        new_session_key = "test-session-key-1"
        self.xblock.last_login_attempt = None
        self.xblock.call_procedure = Mock(return_value=new_session_key)
        self.xblock.get_survey_summary = Mock(side_effect=InvalidSessionKey)

        self.xblock.set_session_key()

        self.xblock.call_procedure.assert_called_once_with(
            "get_session_key",
            settings.LIMESURVEY_API_USER,
            settings.LIMESURVEY_API_PASSWORD,
            get_session_key=True,
        )
        self.assertEqual(self.xblock.session_key, new_session_key)

    def test_new_session_key_still_valid(self):
        """
        Check that the session key is not set when it is still valid.

        Expected result:
            - No request is made to the LimeSurvey API.
        """
        self.xblock.get_survey_summary = Mock()
        self.xblock.call_procedure = Mock()

        self.xblock.set_session_key()

        self.xblock.call_procedure.assert_not_called()

    @override_settings(
        LIMESURVEY_API_USER=None,
        LIMESURVEY_API_PASSWORD=None,
    )
    def test_set_session_key_misconfigured(self):
        """
        Check that when the LimeSurvey Xblock session key set up is misconfigured.

        Expected result:
            - Since the API user/password is not set then an exception is raised.
        """
        self.xblock.get_survey_summary = Mock(side_effect=InvalidSessionKey)
        self.xblock.last_login_attempt = None

        with self.assertRaises(MisconfiguredLimeSurveyService):
            self.xblock.set_session_key()

    @override_settings(LIMESURVEY_URL=None)
    def test_set_student_view_service_misconfigured(self):
        """
        Check that when the LimeSurvey Xblock student view set up is misconfigured.

        Expected result:
            - Since the service URL is not set, an exception is raised.
        """
        user = Mock()
        anonymous_user_id = "test-anonymous-user-id"

        with self.assertRaises(MisconfiguredLimeSurveyService):
            self.xblock.setup_student_view_survey(
                user,
                anonymous_user_id,
            )

    def test_login_attempt_exceeded(self):
        """
        Check that when login attempt is exceeded an exception is raised.

        Expected result:
            - The exception is raised.
        """
        self.xblock.call_procedure = Mock()
        self.xblock.get_survey_summary = Mock(side_effect=InvalidSessionKey)
        self.xblock.last_login_attempt = datetime.now().replace(tzinfo=pytz.utc)  + timedelta(days=1)

        with self.assertRaises(ExceededLoginAttempts):
            self.xblock.set_session_key()

    def test_login_attempt_not_exceeded(self):
        """
        Check that when login attempt is exceeded an exception is raised.

        Expected result:
            - The exception is raised.
        """
        new_session_key = "test-session-key-1"
        self.xblock.call_procedure = Mock(return_value=new_session_key)
        self.xblock.get_survey_summary = Mock(side_effect=InvalidSessionKey)
        self.xblock.last_login_attempt = datetime.now().replace(tzinfo=pytz.utc) - timedelta(days=1)

        self.xblock.set_session_key()

        self.xblock.call_procedure.assert_called_once_with(
            "get_session_key",
            settings.LIMESURVEY_API_USER,
            settings.LIMESURVEY_API_PASSWORD,
            get_session_key=True,
        )
        self.assertEqual(self.xblock.session_key, new_session_key)

    def test_get_survey_summary(self):
        """
        Check getting the survey summary.

        Expected result:
            - A request is made to the LimeSurvey API getting the survey summary.
        """
        expected_result = "survey_summary"
        self.xblock.call_procedure = Mock(return_value=expected_result)
        params = {
            "survey_id": self.xblock.survey_id,
        }

        result = self.xblock.get_survey_summary()

        self.xblock.call_procedure.assert_called_once_with("get_summary", *params.values())
        self.assertEqual(expected_result, result)

    def test_get_student_access_code(self):
        """
        Check getting the current student access code given an anonymous_user_id.

        Expected result:
            - A request is made to the LimeSurvey API getting the access code.
        """
        expected_result = {"token": "test-token"}
        self.xblock.call_procedure = Mock(return_value=expected_result)
        anonymous_user_id = "test-anonymous-user-id"

        self.xblock.set_student_access_code(anonymous_user_id)

        self.xblock.call_procedure.assert_called_once_with(
            "get_participant_properties",
            self.xblock.survey_id,
            {"attribute_1": anonymous_user_id},
        )
        self.assertEqual(expected_result.get("token"), self.xblock.access_code)

    @data(
            ("FirstName", "LastName", "FirstName LastName"),
            ("LastName", "", "LastName"),
            ("FirstName", "", "FirstName"),
            ("", "", ""),
    )
    @unpack
    def test_get_full_name(self, first_name, last_name, full_name):
        """
        Get student first name and last name given a user.

        Expected result:
            - Return a tuple with first and last name.
        """
        user = Mock(full_name=full_name, first_name=first_name, last_name=last_name)

        result = self.xblock.get_fullname(user)

        self.assertTupleEqual((user.first_name, user.last_name), result)
