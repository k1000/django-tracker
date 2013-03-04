# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from tracker.settings import NOTIFY_MANAGERS, NOTIFY_FROM_EMAIL


def notify_staff(obj):

    site = getattr(obj, "sites", None)
    if not site:
        site = Site.objects.get_current()
    data = {
        "site": site.name,
        "admin_url": reverse('admin:tracker_ticket_change', args=(obj.id,)),
        'object': obj,
    }

    subject = 'ticket %s: "%s" en %s' % (obj.id, obj.title, data["site"])
    message = render_to_string("tracker/email/notify_staff.txt", dictionary=data)

    #notify asigned staff member
    send_mail(
        subject,
        message,
        NOTIFY_FROM_EMAIL,
        NOTIFY_MANAGERS + [obj.assigned_to.email],
        fail_silently=False
    )

    if obj.assigned_to_id is not obj.submitter_id:
        #notify submitter
        send_mail(
            subject,
            message,
            NOTIFY_FROM_EMAIL,
            [obj.submitter.email],
            fail_silently=False
        )
