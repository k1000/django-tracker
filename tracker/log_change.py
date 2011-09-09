# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode

from django.contrib.admin.models import LogEntry, CHANGE

EXCLUDED_FIELDS = ("modifiaction_message", "modified_date")

def get_field_display(field, value):
	if field.flatchoices:
		choices = [(str(k), v) for k, v in field.flatchoices ]
		return force_unicode(dict(choices).get(value, value), strings_only=True)
	else:
		return value

def log_change( ticket ):
	
	updated_fields = ticket.get_updated_fields()
	changes_description = []
	for field_name in ticket.get_updated_fields():
		if field_name not in EXCLUDED_FIELDS:
			field = ticket._meta.get_field(field_name, None)
			changes_description.append( 
				u'%s  "%s" -> "%s"' % (
					field.verbose_name, 
					get_field_display( field, updated_fields[field_name][0]), 
					get_field_display( field, updated_fields[field_name][1])
				)
			)
	
	message = _(u"""modificados:\n
	\n*  %s
	\n
	\n%s
	""") % (
		"\n* ".join(changes_description ),
		ticket.modifiaction_message,
	)
	
	LogEntry.objects.log_action(
            user_id         = ticket.modified_by.pk,
            content_type_id = ContentType.objects.get_for_model(ticket).pk,
            object_id       = ticket.pk,
            object_repr     = force_unicode(ticket),
            action_flag     = CHANGE,
            change_message  = message
    )