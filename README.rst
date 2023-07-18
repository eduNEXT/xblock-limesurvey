LimeSurvey XBlock
#############################

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
From the LimeSurvey administrator you must enable the use of the API:

1. Login in the LimeSurvey admin → ``<LIMESURVEY_DOMAIN>/admin``
2. Navigate to Configuration → Settings → Global → Interfaces.
3. Enable ``JSON-RPC`` in RPC interface enabled.
4. Save changes.

Next, you must create a user with API access:

1. Navigate to Configuration → Users management → Add user.
2. Fill the form with the desired information. Doesn't set and Expire date/time and set a custom password.
3. Select the permissions to the user.

   - For the ``Surveys`` permission add permissions to ``View/read`` and ``Update``.
   - Preserve the ``Use internal database authentication`` permission.

   Please, select only the permissions that are necessary, to avoid any unwanted modifications.
4. Save changes.
5. Add your authentication configuration to your LMS settings.

   .. code:: python

       LIMESURVEY_API_USER = "<username>"
       LIMESURVEY_API_PASSWORD = "<password>"


Enabling in Studio
******************

You can enable the LimeSurvey XBlock in the studio through the
advanced settings.

1. From the main page of a specific course, navigate to
   ``Settings -> Advanced Settings`` from the top menu.
2. Check for the ``Advanced Module List`` policy key, and add
   ``"limesurvey"`` to the policy value list.
3. Click the "Save changes" button.


Instructor Dashboard
********************
In the instructor dashboard, you can see a table containing a list
of all the blocks added to the course by the instructor.
This table contains the block's name and a button to access the
administrator according to the URL of the service defined in the block.


Behavior
**************
1. When the URLs are not configured, the service will display an error message.
2. When the survey ID is not valid, the service will display an error message.


Tips
****
1. All surveys added of closed-access mode, must have an ``attribute_1``, which
   allows the assignment of a unique identifier for each survey participant.
2. Use distinctive names for each LimeSurvey block to make it easier to identify
   them in the instructor dashboard.
3. The URL of the LimeSurvey installation can be edited in each block's configuration
   in the ``Limesurvey URL`` field. If the field is empty, it will take the default
   URL defined in the service configuration.
4. To use anonymous surveys you should edit in the block configuration and set the
   field ``Anonymous survey = True``.


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

.. |pypi-badge| image:: https://img.shields.io/pypi/v/{{ cookiecutter.repo_name }}.svg
    :target: https://pypi.python.org/pypi/{{ cookiecutter.repo_name }}/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/openedx/{{ cookiecutter.repo_name }}/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/openedx/{{ cookiecutter.repo_name }}/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/openedx/{{ cookiecutter.repo_name }}/coverage.svg?branch=main
    :target: https://codecov.io/github/openedx/{{ cookiecutter.repo_name }}?branch=main
    :alt: Codecov

.. |doc-badge| image:: https://readthedocs.org/projects/{{ cookiecutter.repo_name }}/badge/?version=latest
    :target: https://docs.openedx.org/projects/{{ cookiecutter.repo_name }}
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.repo_name }}.svg
    :target: https://pypi.python.org/pypi/{{ cookiecutter.repo_name }}/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/openedx/{{ cookiecutter.repo_name }}.svg
    :target: https://github.com/openedx/{{ cookiecutter.repo_name }}/blob/main/LICENSE.txt
    :alt: License

.. TODO: Choose one of the statuses below and remove the other status-badge lines.
.. |status-badge| image:: https://img.shields.io/badge/Status-Experimental-yellow
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Deprecated-orange
.. .. |status-badge| image:: https://img.shields.io/badge/Status-Unsupported-red
