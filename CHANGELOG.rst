Change Log
##########

..
   All enhancements and patches to limesurvey will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
**********

*

0.6.4 - 2023-10-04
**********************************************

Changed
=======

* Return dictionary (in all situations) so filter can be used along with other filters.

0.6.3 - 2023-10-04
**********************************************

Changed
=======

* Return dictionary so filter can be used along with other filters.

0.6.2 - 2023-09-11
**********************************************

Changed
=======

* Add improvements to README and captions


0.6.1 - 2023-08-11
**********************************************

Changed
=======

* Add translations folder in package data


0.6.0 - 2023-08-10
**********************************************

Added
=====

* Add translations of es_419 and es_ES in the xblock

Changed
=======

* Update README with new fields and important note


0.5.1 - 2023-08-08
**********************************************

Changed
=======

* Use index.php prefix when calling the internal LimeSurvey API.
* Call LimeSurvey API when the survey is anonymous only.


0.5.0 - 2023-08-04
**********************************************

Added
=====

* Better field descriptions in the studio edit view.
* Support for older LimeSurvey versions (< 6.1.0).
* Support for LimeSurvey API configurable credentials.


0.4.1 - 2023-07-25
**********************************************

Changed
=======

* Load paragon styles in instructor dashboard.


0.4.0 - 2023-07-19
**********************************************

Added
=====

* Add list of multiple LimeSurvey instances from instructor tab.
* Make instructor view configurable by Django settings.


0.3.0 – 2023-07-12
**********************************************

Added
=====

* Xblock support for anonymous surveys.
* Support for multiple LimeSurvey instances per course.


0.2.3 – 2023-07-06
**********************************************

Added
=====

* Added XBlock compatibility notes.


Changed
=======

* Use different admin endpoint for instructors.


0.2.2 – 2023-06-28
**********************************************

Added
=====

* Missing __init__.py file in the wrapper modules.


0.2.1 – 2023-06-28
**********************************************

Added
=====

* Test suite for the Xblock class definition.
* Logging messages when raising an error for better debugging.


Changed
=======

* Return from instructor filter if there is no LimeSurvey block in the course.
* Use import backends to handle multiple source code versions.
* Check if settings exist before using them in the views to avoid misleading errors.


0.2.0 – 2023-06-26
**********************************************

Added
=====

* Studio view handler for instructors to configure limesurvey as an Iframe.
* Student interaction with survey from the LMS with API callings and Iframe integration.

0.1.0 – 2023-05-31
**********************************************

Added
=====

* First release.
