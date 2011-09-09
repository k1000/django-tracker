# -*- coding: utf-8 -*-
from django.db.models.signals import post_save

from models import Ticket, Note
from notify import ticket_notify_staff, note_notify_staff
from log_change import log_change

def ticket_modified_taskas(sender, **kw):
    ticket_notify_staff( kw["instance"] )

def do_log_change(sender, **kw):
    ticket = kw["instance"]
    log_change( ticket )
    ticket._reset_state()

def note_cerated_taskas(sender, **kw):
    note_notify_staff( kw["instance"] )

post_save.connect(ticket_modified_taskas, sender=Ticket)
post_save.connect(do_log_change, sender=Ticket)
post_save.connect(note_cerated_taskas, sender=Note)