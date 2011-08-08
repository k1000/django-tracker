# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from tracker.settings import NOTIFY_MANAGERS, NOTIFY_FROM_EMAIL


def ticket_notify_staff( ticket ):

    subject = 'nuevo ticket #%s: "%s" en proyecto "%s"' % (ticket.pk, ticket.title, ticket.project)
    data = {
        "project": ticket.project,
        "admin_url": reverse( 'admin:tracker_ticket_change', args=(ticket.id,) ),
        'ticketect': ticket,
    }
    message = render_to_string("tracker/email/ticket_notify_staff.txt", dictionary=data )
    recipients = NOTIFY_MANAGERS + [
            ticket.submitter.email, ticket.project.project_manager.email 
    ]
    workteam = ticket.get_related_staff()
    if workteam:
        recipients += workteam.values("email")
    else:
        all_staff = User.objects.filter(is_staff=True, is_active=True)
        recipients += [staff_member.email for staff_member in all_staff]
    #notify asigned staff member                  
    send_mail(
        subject, 
        message,
        NOTIFY_FROM_EMAIL,
        recipients, 
        fail_silently=False
    )


def note_notify_staff(note):
    ticket = note.ticket
    project = ticket.project

    subject = '"nueva nota para el ticket #%s: "%s" en proyecto %s' % (ticket.pk, ticket.title, project)

    data = {
        "project": ticket.project,
        "admin_url": reverse( 'admin:tracker_ticket_change', args=(ticket.id,) ),
        'ticketect': ticket,
    }

    message = render_to_string("tracker/email/note_notify_staff.txt", dictionary=data )
    recipients = NOTIFY_MANAGERS + project.get_staff.values("email")

    #ticket_note_creators = note.related_creators.values("email")
    componet_workteam = note.ticket.component.workteam
    if componet_workteam:
        recipients += componet_workteam.values("email")
    else:
        all_staff = User.objects.filter(is_staff=True, is_active=True)
        recipients += [staff_member.email for staff_member in all_staff]
    #notify asigned staff member      

    send_mail(
        subject, 
        message, 
        NOTIFY_FROM_EMAIL,
        recipients,
        fail_silently=False
    )

