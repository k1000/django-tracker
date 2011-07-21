# -*- coding: utf-8 -*-
from django.contrib import admin

from tracker.models import Ticket
from settings import STATUS_COLOR_CODES

class TicketAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change): 
        obj.submitter = request.user
        obj.save()  
        
    fieldsets = (
        (None, {
                'fields': ( "title", 
                            ("status", "kind"),
                            ("project", "url"),
                            "description",
							("assigned_to","priority"),
							"commit_id", 
							'image',
                          )
        }),
    )
    
    def status_color(self, obj):
        return '<span style="background: %s; color:black; display: block">%s</span>' % (STATUS_COLOR_CODES[ obj.status - 1 ][1], obj.get_status_display() )
        
    status_color.short_description = 'status'
    status_color.allow_tags = True
    
    ordering = ('-submitted_date',)
    date_hierarchy = 'submitted_date'
    list_display = ( 'title', "id", 'status_color', "submitted_date", "priority",  'kind',  'project',"submitter", 'assigned_to', )
    
    search_fields = ('title', 'id', 'project', 'description', "commit_id" )

    list_filter = ( "priority", 'status',  'kind',  'project', 'assigned_to', )

admin.site.register( Ticket, TicketAdmin)
