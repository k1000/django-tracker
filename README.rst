--------------
django-tracker
--------------

*django-tracker* - simple bug tracker loosely coupled with your django project.

Features:
    * bug/feature submission and tracking
    * task assignment
    * integration with django.users
    * email notification when bug/feature changes
    * convinient configuration via settings
    * comments/notes from users

Optional Features (activated via settings):
    * coupling to project apps
    * multisite support
    * closing tickets from GIT commit message

Known to work in Django 1.3

Installation
------------
    
1. Download and install::

        git clone https://github.com/k1000/django-tracker.git
        cd django-tracker
        python setup.py install

   or using pip::     
    
        pip install -e git+https://github.com/k1000/django-tracker.git#egg=tracker

2. Add "tracker" to your INSTALLED_APPS in "settings.py" 
3. Run "./manage.py syncdb" to create db tables

Configuration
-------------

See SETTINGS_ for more info.

GIT integration
---------------

You can close tickets directly from GIT appending ticket ref in commit message as "#ticket_ref"
In order to activate integration:

    1. cd to ".git/hooks" directory
    2. backup old update script: "mv update update-bck"
    3. link to tracker management shell script: "ln -s ../../../env/src/tracker/tracker/management/commands/update"
    4. put correct "project_path" and "python_path" in update script
    5. "chmod +x update"

TODO
----

    * [*] email notification templates
    * [*] optional comments
    * [ ] comment notifications
    * [ ] maybe notifying fired by signals instead save method overload ?
    * [ ] RSS feed for open tickets
    * [*] closing tickets from GIT commit message (using update hook)
    * [ ] optional management flow


LICENSE
-------

Django-tracker is released under the MIT License. See the LICENSE_ file for more
details.

.. _LICENSE: http://github.com/k1000/django-backfire/blob/master/LICENSE
.. _SETTINGS: /k1000/django-tracker/blob/master/SETTINGS.rst
