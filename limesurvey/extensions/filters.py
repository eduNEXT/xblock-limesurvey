"""
Open edX Filters needed for LimeSurvey integration.
"""
from crum import get_current_request
from django.conf import settings
from openedx_filters import PipelineStep
from django.conf import settings

from limesurvey.edxapp_wrapper.courseware import get_object_by_usage_id
from limesurvey.edxapp_wrapper.xmodule import modulestore

INSTRUCTOR_TEMPLATE_ABSOLUTE_PATH = "/instructor_dashboard/"
LIMESURVEY_BLOCK_CATEGORY = "limesurvey"

class AddInstructorLimesurveyTab(PipelineStep):
    """Add LimeSurvey tab to instructor dashboard."""

    def run_filter(self, context, template_name):  # pylint: disable=unused-argument, arguments-differ
        """Execute filter that modifies the instructor dashboard context.

        Args:
            context (dict): the context for the instructor dashboard.
            template_name (str): instructor dashboard template name.
        """
        if not settings.FEATURES.get("ENABLE_LIMESURVEY_INSTRUCTOR_VIEW", False):
            return context

        course = context["course"]
        request = get_current_request()
        limesurvey_blocks = modulestore().get_items(
            course.id, qualifiers={"category": LIMESURVEY_BLOCK_CATEGORY}
        )
        limesurvey_block = None
        if len(limesurvey_blocks) > 0:
            limesurvey_block = limesurvey_blocks[0]

        # Return if there is no LimeSurvey block in the course
        if not limesurvey_block:
            return context

        block = get_object_by_usage_id(
            request, str(course.id), str(limesurvey_block.location),
            disable_staff_debug_info=True, course=course
        )

        limesurvey_url = getattr(settings, "LIMESURVEY_URL", None)
        xblock_urls = [
            (block.display_name, block.limesurvey_url or limesurvey_url)
            for block in limesurvey_blocks
        ]

        section_data = {
            "fragment": block.render("instructor_view", context={"xblock_urls": xblock_urls}),
            "section_key": LIMESURVEY_BLOCK_CATEGORY,
            "section_display_name": "LimeSurvey",
            "course_id": str(course.id),
            "template_path_prefix": INSTRUCTOR_TEMPLATE_ABSOLUTE_PATH,
        }
        context["sections"].append(section_data)
        return context
