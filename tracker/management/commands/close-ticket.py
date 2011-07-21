# -*- coding: utf-8 -*-
import logging
from django.core.management.base import BaseCommand, CommandError

from tracer.models import Ticket

logger = logging.getLogger("django")


class Command(BaseCommand):
    help = '''busca ticket y lo cierra'''
    def handle(self, *args, **options):
        try:
            ticket = Ticket.objects.get(pk = ref )
            ticket.status = 3
            ticket.save()
            print "ticket #%s closed" % ref
        except:
            raise CommandError( "Can't close ticket" )