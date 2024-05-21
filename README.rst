LimeSurvey XBlock
#################

|status-badge| |license-badge| |ci-badge|

Purpose
*******
LimeSurvey XBlock allows a better integration between the Open edX platform and the Open source `LimeSurvey`_ service.

.. _LimeSurvey: https://www.limesurvey.org/

Once the LimeSurvey component has been added and configured into a course unit, learners can view and complete the different surveys assigned to them.

This Xblock has been created as an open source contribution to the Open edX platform and has been funded by the Unidigital project from the Spanish Government - 2023. 


**NOTE**: This XBlock doesn't deploy the LimeSurvey service. It requires an external service or a service installed
from the Tutor stack. If you want to install a brand new LimeSurvey service using Tutor, you can use the following `plugin`_.

.. _plugin: https://github.com/eduNEXT/tutor-contrib-limesurvey


Compatibility Notes
===================

+------------------+--------------+
| Open edX Release | Version      |
+==================+==============+
| Olive            | >= 0.2.1     |
+------------------+--------------+
| Palm             | >= 0.2.0     |
+------------------+--------------+
| Quince           | >= 0.2.0     |
+------------------+--------------+
| Redwood          | >= 0.2.0     |
+------------------+--------------+

The following changes to the plugin settings are necessary. If the release you are looking for is
not listed, then the accumulation of changes from previous releases is enough.

**Olive**

.. code-block:: yaml

   LIMESURVEY_COURSEWARE_BACKEND: "limesurvey.edxapp_wrapper.backends.courseware_o_v1"

**Palm, Quince and Redwood**

.. code-block:: yaml

   LIMESURVEY_COURSEWARE_BACKEND: "limesurvey.edxapp_wrapper.backends.courseware_p_v1"

These settings can be changed in ``limesurvey/settings/common.py`` or, for example, in tutor configurations.

**NOTE**: the current ``common.py`` works with Open edX Palm, Quince and Redwood version.


Configure LimeSurvey to work with this Xblock
*********************************************

From the LimeSurvey administrator, you must enable the use of the API:

1. Login in the LimeSurvey admin → ``<LIMESURVEY_DOMAIN>/admin``
2. Navigate to Configuration → Settings → Global → Interfaces.
3. Enable ``JSON-RPC`` in RPC interface enabled.
4. Save changes.

Next, you must create a user with API access:

1. Navigate to Configuration → Users management → Add user.
2. Fill the form with the desired information. Doesn't set an Expire date/time and set a custom password.
3. Select the permissions for the user.

   - For the ``Surveys`` permission add permissions to ``View/read`` and ``Update``.
   - Preserve the ``Use internal database authentication`` permission.

   Please, select only the necessary permissions, to avoid any unwanted modifications.
4. Save changes.

Configurations required in the Open edX platform
*************************************************

In order to avoid the need to configure the LimeSurvey credentials each time the component is used, you can add your authentication configuration to your LMS settings.

.. code:: python

    LIMESURVEY_API_USER = "<username>"
    LIMESURVEY_API_PASSWORD = "<password>"
    FEATURES["ENABLE_LIMESURVEY_INSTRUCTOR_VIEW"] = True


Enabling the XBlock in a course
*******************************

When the Xblock has been installed, you can enable the LimeSurvey XBlock for a particular course in STUDIO through the advanced settings.

.. image:: https://github.com/eduNEXT/xblock-limesurvey/assets/64033729/67f62cc9-68f5-4d96-a47c-c0ef7f7b6adb

1. From the main page of a specific course, navigate to ``Settings → Advanced Settings`` from the top menu.
2. Check for the ``Advanced Module List`` policy key, and add ``"limesurvey"`` to the policy value list.
3. Click the "Save changes" button.


Adding a LimeSurvey Component to a course unit
**********************************************
.. image:: https://github.com/eduNEXT/xblock-limesurvey/assets/64033729/95f42b3d-fd30-4655-ac85-07afefa81b81

Fields
======
- **Display name (String)**: Name of the component. This name will be displayed in the instructor dashboard.
- **Survey ID (Integer)**: The ID of the survey to be embedded. Verify that the field value is correct,
  otherwise, the service will display an error message from the LMS.
- **Survey Mode**: Whether the survey is set to be public for everyone (open-access mode) or invite only (closed-access mode) in the LimeSurvey administration console. When the Survey is closed-access, make sure that an additional attribute is created in the Survey's participants table. This new field is needed to store the learner's anonymized id.
- **LimeSurvey URL (String)**: The URL of the LimeSurvey installation without the trailing slash. Leave this field empty to use the default configurations.
- **LimeSurvey API username (String)**: The username to authenticate with the LimeSurvey service. Leave this field empty to use the default configurations. 
- **LimeSurvey API password (String)**: The password to authenticate with the LimeSurvey service. Leave this field empty to use the default configurations.

Survey Modes
============
In LimeSurvey, you can configure 2 survey modes: closed or open (anonymous).

- **Open-access:** Open surveys allow any visitor with access to the link to fill out the survey. In this mode,
  there is no way to relate the response to the identity of the specific learner.
- **Closed-access:** Closed surveys limit access to the survey to a specifil list of participants. i.e., only learners that are enrolled in the course. When accessing a closed-access Survey, the LimeSurvey Xblock will automatically insert the learner information in the participants table in Limesurvey, including the course specific anonimized_id, which is stored in an additional field  (``attribute_1``) that needs to be added to the table. This allows the assignment of a unique identifier for each survey participant even when using anonymous responses.   If this attribute is not added when creating the Survey in Limesurvey, students will not be able to complete the survey.



View from the Learning Management System (LMS)
**********************************************

As a Student
============
.. image:: https://github.com/eduNEXT/xblock-limesurvey/assets/64033729/b7ad78df-7cc9-4bf6-9c17-41ddd9a8171f

- The student observes the component from the LMS and will be able to complete the assigned survey.
- The student can save the progress of the survey and complete it later. Click on "Resume later",
  and assigns a name and password. At the next login, the progress can be loaded by clicking on
  "Load unfinished survey"

As an Instructor
================
.. image:: https://github.com/eduNEXT/xblock-limesurvey/assets/64033729/0cd3630e-becf-4eaf-ad87-ce0101b11b51

The instructor can access the instructor dashboard. In the instructor dashboard, you can see a table with
the following columns:

- **Component name:** This is the name assigned to each component in the ``Display name`` field.
- **Management Console(s):** This is the URL of the administrator assigned to each component in the
  ``LimeSurvey URL`` field.


Currently, the LimeSurvey instructor management view is not broadly available for the community to use. So
to use it in your installation -- eg. creating your own Open edX docker image, you must follow the instructions explained `here <https://github.com/eduNEXT/xblock-limesurvey/pull/8>`__.
We're working towards getting this feature upstream.


Experimenting with this Xblock in the Workbench
************************************************

`XBlock`_ is the Open edX component architecture for building custom learning interactive components.

.. _XBlock: https://openedx.org/r/xblock

You can see the LimeSurvey component in action in the XBlock Workbench. Running the Workbench requires having docker running.

.. code:: bash

    git clone git@github.com:eduNEXT/xblock-limesurvey
    virtualenv venv/
    source venv/bin/activate
    cd xblock-limesurvey
    make upgrade
    make install
    make dev.run

Once the process is done, you can interact with the LimeSurvey XBlock in the Workbench by navigating to http://localhost:8000

For details regarding how to deploy this or any other XBlock in the Open edX platform, see the `installing-the-xblock`_ documentation.

.. _installing-the-xblock: https://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html#installing-the-xblock


Getting Help
*************

If you're having trouble, the Open edX community has active discussion forums available at https://discuss.openedx.org where you can connect with others in the community.

Also, real-time conversations are always happening on the Open edX community Slack channel. You can request a `Slack invitation`_, then join the `community Slack workspace`_.

For anything non-trivial, the best path is to open an issue in this repository with as many details about the issue you are facing as you can provide.

https://github.com/eduNEXT/xblock-limesurvey/issues


For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL-3.0 unless otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome.

This project is currently accepting all types of contributions, bug fixes, security fixes, maintenance
work, or new features.  However, please make sure to have a discussion about your new feature idea with
the maintainers prior to beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing your idea.


Translations
============
This Xblock is initially available in English and Spanish. You can help by translating this component to other languages. Follow the steps below:

1. Create a folder for the translations in ``locale/``, eg: ``locale/fr_FR/LC_MESSAGES/``, and create
   your ``text.po`` file with all the translations.
2. Run ``make compile_translations``, this will generate the ``.mo`` file.
3. Create a pull request with your changes!


Reporting Security Issues
*************************

Please do not report a potential security issue in public. Please email security@edunext.co.

.. |pypi-badge| image:: https://img.shields.io/pypi/v/xblock-limesurvey.svg
    :target: https://pypi.python.org/pypi/xblock-limesurvey/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/eduNEXT/xblock-limesurvey/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/xblock-limesurvey/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/eduNEXT/xblock-limesurvey/coverage.svg?branch=main
    :target: https://codecov.io/github/eduNEXT/xblock-limesurvey?branch=main
    :alt: Codecov

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/xblock-limesurvey.svg
    :target: https://pypi.python.org/pypi/xblock-limesurvey/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/xblock-limesurvey.svg
    :target: https://github.com/eduNEXT/xblock-limesurvey/blob/main/LICENSE.txt
    :alt: License

.. TODO: Choose one of the statuses below and remove the other status-badge lines.
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red