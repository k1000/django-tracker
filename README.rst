About
-----

*django-tracker* - simple bug tracker loosely coupled with your django project.

Features:
    * bug/feature submission and tracking
    * task assignment
    * email notification when bug/feature changes
    * convinient configuration via settings

Optional Features (activated via settings):
    * coupling to project apps
    * multisite support

Known to work in Django 1.3

Installation
------------
    
1. Download and install::

        git clone https://github.com/k1000/django-tracker.git
        cd django-tracker
        python setup.py install

    or using pip::     
    
        pip install -e git+https://github.com/k1000/django-tracker.git#egg=tracker

2. Add "tracker" to your APPS settings.

TODO
----

    * email notification templates
    * maybe notifing fired by signals instead save method overload ?


LICENSE
-------

Django-tracker is released under the MIT License. See the __LICENSE file for more
details.

.. _LICENSE: http://github.com/k1000/django-backfire/blob/master/LICENSE
