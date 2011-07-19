# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

EMAIL_NOTIFIY = getattr(settings, "TRACKER_EMAIL_NOTIFIY", True )

# tracer initialization settings !!!dont'change after instalation
PROJECT_INTEGRATION = getattr(settings, "TRACKER_PROJECT_INTEGRATION", True )
EXCLUDE_APPS = getattr(settings, "TRACKER_EXCLUDE_APPS", [] )
MULTISITE = getattr(settings, "TRACKER_MULTISITE", False )
ACTIVETE_COMMENTS = getattr(settings, "TRACKER_ACTIVETE_COMMENTS", False )


ASIGNED_USER_CLS = getattr(settings, "TRACKER_ASIGNED_USER", User )
LIMIT_ASIGNED_USERS = getattr(settings, "TRACKER_LIMIT_ASIGNED_STAFF", {'is_staff__exact': True}  )

SUBMITTER_USER_CLS = getattr(settings, "TRACKER_SUBMITTER_USER", User )
LIMIT_SUBMITTER_USERS = getattr(settings, "TRACKER_LIMIT_SUBMITTER_USERS", {}  )

IMAGE_UPLOAD_DIR = getattr(settings, "TRACKER_IMAGE_UPLOAD_DIR", "uploads/tracker" )

STATUS_CODES = getattr(settings, 
    "TRACKER_STATUS_CODES", 
    (
        (1, _('Abierto')),
        (2, _('En proceso')),
        (3, _('Cerrado')),
        (4, _('Ignorado')),
    ) 
)

KIND_CODES = getattr(settings, 
    "TRACKER_KIND_CODES", 
    (
        (1, _('Error')),
        (2, _(u'Correción linguistica')),
        (3, _('Mejora')),
    ) 
)

PRIORITY_CODES = getattr(settings, 
    "TRACKER_KIND_CODES", 
    (
        (1, _('Urgente')),
        (2, _('Pronto')),
        (3, _(u'Algun día')),
    ) 
)
DEFAULT_PRIORITY = getattr(settings, "TRACKER_DEFAULT_PRIORITY", 2 )

if PROJECT_INTEGRATION:
    EXCLUDE_APPS += [ app for app in settings.INSTALLED_APPS if "django." in app ]
    apps = [ app for app in settings.INSTALLED_APPS if app not in EXCLUDE_APPS ]
    PROJECTS = list(enumerate(apps))