Configuration
_____________

*django-tracker* - simple bug tracker loosely coupled with your django project.
Allows convinient configuration options via settings

TRACKER_EMAIL_NOTIFIY
    type: Boolean
    default: True

TRACKER_PROJECT_INTEGRATION
    type: Boolean
    default: True

TRACKER_EXCLUDE_APPS
    type: List
    default: []

TRACKER_MULTISITE
    type: Boolean
    default: False

TRACKER_ACTIVETE_COMMENTS
    type: Boolean
    default: False

TRACKER_ASIGNED_USER
    type: Class
    default: User

TRACKER_LIMIT_ASIGNED_USERS
    type: Dict
    default: {'is_staff__exact': True}

TRACKER_SUMITTER_USER
    type: Class
    default: User

TRACKER_LIMIT_SUBMITTER_USERS
    type: Dict
    default: {}

TRACKER_IMAGE_UPLOAD_DIR
    type: Dict
    default: "uploads/tracker"

TRACKER_STATUS_CODES
    type: Tuple
    default: (
        (1, _('Abierto')),
        (2, _('En proceso')),
        (3, _('Cerrado')),
        (4, _('Ignorado')),
    )

TRACKER_KIND_CODES
    type: Tuple
    default: (
        (1, _('Error')),
        (2, _(u'Correción linguistica')),
        (3, _('Mejora')),
    )

TRACKER_PRIORITY_CODES
    type: Tuple
    default: (
        (1, _('Urgente')),
        (2, _('Pronto')),
        (3, _(u'Algun día')),
    )

TRACKER_DEFAULT_PRIORITY
    type: Int
    default: 2