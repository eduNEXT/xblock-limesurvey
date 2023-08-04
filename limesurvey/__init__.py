"""
Init for the LimeSurveyXBlock package.
"""
import os
from pathlib import Path
from .limesurvey import LimeSurveyXBlock

__version__ = '0.5.0'

LIMESURVEY_ROOT_DIRECTORY = Path(os.path.dirname(os.path.abspath(__file__)))
