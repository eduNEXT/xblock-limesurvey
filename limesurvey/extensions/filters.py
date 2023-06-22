"""
Open edX Filters needed for LimeSurvey integration.
"""
from crum import get_current_request
from openedx_filters import PipelineStep

try:
    from xmodule.modulestore.django import modulestore
    from lms.djangoapps.courseware.block_render import get_block_by_usage_id
except ImportError:
    modulestore = object
    get_block_by_usage_id = object

INSTRUCTOR_TEMPLATE_ABSOLUTE_PATH = "/instructor_dashboard/"
LIMESURVEY_BLOCK_CATEGORY = "limesurvey"

class AddInstructorLimesurveyTab(PipelineStep):
    """Add LimeSurvey tab to instructor dashboard."""

    def run_filter(self, context, template_name):  # pylint: disable=unused-argument, arguments-differ
        """Execute filter that modifies the instructor dashboard context.

        Args:
            context (dict): the context for the instructor dashboard.
            _ (str): instructor dashboard template name.
        """
        course = context["course"]
        request = get_current_request()
        limesurvey_blocks = modulestore().get_items(
            course.id, qualifiers={"category": LIMESURVEY_BLOCK_CATEGORY}
        )
        limesurvey_block = limesurvey_blocks[0]
        block, __ = get_block_by_usage_id(
            request, str(course.id), str(limesurvey_block.location),
            disable_staff_debug_info=True, course=course
        )
        section_data = {
            "fragment": block.render("instructor_view", context={}),
            "section_key": LIMESURVEY_BLOCK_CATEGORY,
            "section_display_name": "LimeSurvey",
            "course_id": str(course.id),
            "template_path_prefix": INSTRUCTOR_TEMPLATE_ABSOLUTE_PATH,
        }
        context["sections"].append(section_data)
        return context
