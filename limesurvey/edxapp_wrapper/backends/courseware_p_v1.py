"""
Courseware definitions for Open edX Palm release.
"""
from lms.djangoapps.courseware.block_render import get_block_by_usage_id


def get_object_by_usage_id(request, course_id, location, disable_staff_debug_info=False, course=None):
    """
    Get the block object for the given block usage id.

    Args:
        request (HttpRequest): Django request object.
        course_id (str): Course ID.
        location (str): block location.
        disable_staff_debug_info (bool): Whether to disable staff debug info.
        course (CourseDescriptor): Course descriptor.

    Returns:
        BlockUsageLocator: Block object.
    """
    block, __ = get_block_by_usage_id(
        request,
        course_id,
        location,
        disable_staff_debug_info=disable_staff_debug_info,
        course=course,
    )
    return block
