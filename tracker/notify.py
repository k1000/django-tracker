from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse# Create your views here.
from django.contrib.sites.models import Site

CURRENT_SITE = Site.objects.get_current()

def notify_staff( obj ):
    body = """
ticket %s: %s %s
estado:%s
creado: %s
priridad: %s
url: %s
-------------------------
%s
-------------------------
este mensage ha side generado automaticamente
    """ % (
    obj.id,
    obj.title,
    "%s/%s" % ( CURRENT_SITE, reverse( 'admin:tracker_ticket_change', args=(obj.id,) ) ),
    obj.status,
    obj.submitted_date,
    obj.priority,
    obj.url,
    obj.description,
    )
    send_mail(
        'ticket %s: "%s"' % (obj.id, obj.title), 
        obj.description, 
        obj.submitter.email,
        [obj.assigned_to.email ], 
        fail_silently=False
    )