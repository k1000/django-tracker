# -*- coding: utf-8 -*-
from django.contrib import admin

from tracker.models import Ticket

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
							'image',
                          )
        }),
    )
    
    def status_color(self, obj):
        return '<span style="color: #%s;">%s</span>' % ("red", obj.status)
    status_color.short_description = 'status'
    status_color.allow_tags = True
    
    ordering = ('-submitted_date',)
    date_hierarchy = 'submitted_date'
    list_display = ( 'title', "submitted_date", "priority", 'status',  'kind',  'project',"submitter", 'assigned_to', )
    
    search_fields = ('title', 'project', 'description', "commit_id" )

    list_filter = ( "priority", 'status',  'kind',  'project', 'assigned_to', )

admin.site.register( Ticket, TicketAdmin)
