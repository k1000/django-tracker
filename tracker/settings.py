# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

EMAIL_NOTIFIY = getattr(settings, "TRACKER_EMAIL_NOTIFIY", True)

# tracer initialization settings !!!dont'change after instalation
PROJECT_INTEGRATION = getattr(settings, "TRACKER_PROJECT_INTEGRATION", True)
EXCLUDE_APPS = getattr(settings, "TRACKER_EXCLUDE_APPS", [])
MULTISITE = getattr(settings, "TRACKER_MULTISITE", False)
ACTIVETE_COMMENTS = getattr(settings, "TRACKER_ACTIVETE_COMMENTS", False)


ASIGNED_USER_CLS = getattr(settings, "TRACKER_ASIGNED_USER", User)
LIMIT_ASIGNED_USERS = getattr(settings, "TRACKER_LIMIT_ASIGNED_STAFF", {'is_staff__exact': True})

SUBMITTER_USER_CLS = getattr(settings, "TRACKER_SUBMITTER_USER", User)
LIMIT_SUBMITTER_USERS = getattr(settings, "TRACKER_LIMIT_SUBMITTER_USERS", {})

IMAGE_UPLOAD_DIR = getattr(settings, "TRACKER_IMAGE_UPLOAD_DIR", "uploads/tracker/images")
FILE_UPLOAD_DIR = getattr(settings, "TRACKER_FILE_UPLOAD_DIR", "uploads/tracker/files")

NOTIFY_MANAGERS = getattr(settings, "TRACKER_NOTIFY_MANAGERS", [])
NOTIFY_FROM_EMAIL = getattr(settings, "TRACKER_NOTIFY_FROM_EMAIL", settings.DEFAULT_FROM_EMAIL)

STATUS_CODES = getattr(settings,
    "TRACKER_STATUS_CODES",
    (
        (1, _('Open')),
        (2, _('In work')),
        (3, _('Closed')),
        (4, _('Ignored')),
        (5, _('Closed - defunkt')),
    )
)

STATUS_COLOR_CODES = getattr(settings,
    "TRACKER_STATUS_COLOR_CODES",
    (
        (1, '#ffbb56'),  # orange
        (2, 'yellow'),
        (3, '#7fff00'),  # lighht green
        (4, '#eaeaea'),  # lighht gray
        (5, '#7fff00'),  # lighht gray
    )
)

KIND_CODES = getattr(settings,
    "TRACKER_KIND_CODES",
    (
        (1, _('Error')),
        (2, _(u'typo')),
        (3, _('improvement')),
    )
)

PRIORITY_CODES = getattr(settings,
    "TRACKER_PRIORITY_CODES",
    (
        (1, _('Urgent!')),
        (2, _('Soon')),
        (3, _('Some day')),
    )
)
DEFAULT_PRIORITY = getattr(settings, "TRACKER_DEFAULT_PRIORITY", 2)

if PROJECT_INTEGRATION:
    EXCLUDE_APPS += [app for app in settings.INSTALLED_APPS if "django." in app]
    apps = [app for app in settings.INSTALLED_APPS if app not in EXCLUDE_APPS]
    PROJECTS = list(enumerate(apps))
