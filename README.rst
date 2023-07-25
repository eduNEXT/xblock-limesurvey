LimeSurvey XBlock
#################

|status-badge| |license-badge| |ci-badge|

Purpose
*******

`XBlock`_ is the Open edX component architecture for building custom
learning interactives.

.. _XBlock: https://openedx.org/r/xblock

LimeSurvey XBlock allows students to view and complete
the different surveys assigned to them.


Getting Started
***************

You can see the LimeSurvey in action in the XBlock Workbench.  Running the Workbench requires having docker running.

.. code:: bash

    git clone git@github.com:eduNEXT/xblock-limesurvey
    virtualenv venv/
    source venv/bin/activate
    cd xblock-limesurvey
    make upgrade
    make install
    make dev.run

You can interact with the LimeSurveyXBlock in the Workbench by navigating to http://localhost:8000

For details regarding how to deploy this or any other XBlock in the lms instance, see the `installing-the-xblock`_ documentation.

.. _installing-the-xblock: https://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html#installing-the-xblock


Compatibility Notes
===================

+------------------+--------------+
| Open edX Release | Version      |
+==================+==============+
| Olive            | >= 0.2.1     |
+------------------+--------------+
| Palm             | >= 0.2.0     |
+------------------+--------------+

The following changes to the plugin settings are necessary. If the release you are looking for is
not listed, then the accumulation of changes from previous releases is enough.

**Olive**

.. code-block:: yaml

   LIMESURVEY_COURSEWARE_BACKEND: "limesurvey.edxapp_wrapper.backends.courseware_o_v1"

These settings can be changed in ``limesurvey/settings/common.py`` or, for example, in tutor configurations.

**NOTE**: the current ``common.py`` works with Open edX Palm version.


Set up LimeSurvey
*****************
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
5. Add your authentication configuration to your LMS settings.

   .. code:: python

       LIMESURVEY_API_USER = "<username>"
       LIMESURVEY_API_PASSWORD = "<password>"


Configuring LimeSurvey
**********************

Survey Modes
============
In LimeSurvey, you can configure 2 survey modes: closed or open (anonymous).

- **Closed:** Closed surveys limit access to the survey to any person, i.e., only students with
  an access code will be able to fill it out. All surveys added to closed-access mode, must have an
  ``attribute_1``, which allows the assignment of a unique identifier for each survey participant.
  If this attribute is not added, students will not be able to complete the survey.
- **Open:** Open surveys allow any student with access to the link to fill out the survey. In this mode,
  there is no way to relate the answers to the students.


Enabling in Studio
******************

You can enable the LimeSurvey XBlock in the studio through the advanced settings.

.. image:: https://github.com/eduNEXT/xblock-limesurvey/assets/64033729/67f62cc9-68f5-4d96-a47c-c0ef7f7b6adb

1. From the main page of a specific course, navigate to ``Settings → Advanced Settings`` from the top menu.
2. Check for the ``Advanced Module List`` policy key, and add ``"limesurvey"`` to the policy value list.
3. Click the "Save changes" button.


Configuring Component
*********************
.. image:: https://github.com/eduNEXT/xblock-limesurvey/assets/64033729/95f42b3d-fd30-4655-ac85-07afefa81b81

Fields
======
- **Display name (String)**: Name of the component. This name will be displayed in the instructor dashboard.
- **Survey ID (Integer)**: The ID of the survey to be embedded. Verify that the field value is correct,
  otherwise, the service will display an error message from the LMS.
- **Anonymous Survey (Boolean)**: Whether the survey is anonymous or not. By default it is set to ``False``,
  to use anonymous surveys you must edit the block configuration and set the value to ``True``
- **LimeSurvey URL (String)**: The URL of the LimeSurvey installation without the trailing slash. If not
  set, it will be taken from the service configurations.


View from Learning Management System (LMS)
******************************************

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

To use the instructor management view, you must add this feature to your LMS configurations: 

.. code:: python

    FEATURES["ENABLE_LIMESURVEY_INSTRUCTOR_VIEW"] = True

Currently, the LimeSurvey instructor management view is not broadly available for the community to use. So
to use it in your installation -- eg. creating your own Open edX docker image, you must follow the instructions explained `here <https://github.com/eduNEXT/xblock-limesurvey/pull/8>`__.
We're working towards getting this feature upstream.

Getting Help
************

Documentation
=============

If you're having trouble, we have discussion forums at
https://discuss.openedx.org where you can connect with others in the
community.

Our real-time conversations are on Slack. You can request a `Slack
invitation`_, then join our `community Slack workspace`_.

For anything non-trivial, the best path is to open an issue in this
repository with as many details about the issue you are facing as you
can provide.

https://github.com/eduNEXT/xblock-limesurvey/issues

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL-3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome.
Please read `How To Contribute <https://openedx.org/r/how-to-contribute>`_ for details.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.


The Open edX Code of Conduct
****************************

All community members are expected to follow the `Open edX Code of Conduct`_.

.. _Open edX Code of Conduct: https://openedx.org/code-of-conduct/

People
******

The assigned maintainers for this component and other project details may be
found in `Backstage`_. Backstage pulls this data from the ``catalog-info.yaml``
file in this repo.

.. _Backstage: https://backstage.openedx.org/catalog/default/component/{{ cookiecutter.repo_name }}


Reporting Security Issues
*************************

Please do not report security issues in public. Please email security@tcril.org.

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
.. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
