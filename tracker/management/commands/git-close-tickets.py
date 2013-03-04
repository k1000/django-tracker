# -*- coding: utf-8 -*-
import commands
import logging
import re
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _

from tracker.models import Ticket

logger = logging.getLogger("django")

#based on http://progit.org/book/ch7-4.html


class Command(BaseCommand):
    """
    search for ticker rferences in git and close it
    """
    args = '<rev oldrev newrev>'
    help = _('''search for ticker rferences in git and close it''')

    def handle(self, *args, **options):
        ref = args[0]
        oldrev = args[1]
        newrev = args[2]
        self.check_messages(oldrev, newrev)

    def check_messages(self, oldrev, newrev):
        regex = re.compile("#(\d+)")

        missed_revs = commands.getoutput('git rev-list %s..%s' % (oldrev, newrev)).split("\n")
        for rev in missed_revs:
            message = commands.getoutput("git cat-file commit %s | sed '1,/^$/d'" % rev)
            tickets = regex.findall(message)
            if tickets:
                self.close_tickets(rev, tickets)

    def close_tickets(self, rev, tickets):

        for ticket_id in tickets:
            try:
                ticket = Ticket.objects.get(pk=int(ticket_id))
            except Ticket.DoesNotExist:
                raise CommandError(_("Can't close ticket. Ticket #%s doesn't exist") % ticket_id)

            ticket.status = 3
            ticket.commit_id = rev
            ticket.save()

            self.stdout.write(_("ticket #%s has been closed") % ticket_id)
