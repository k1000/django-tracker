# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django import forms
from django.db import models

from tracker.forms import CreateNoteForm, LogForm, StatusTicketForm
from tracker.models import Ticket, Note, Project, Component, Milestone
from settings import STATUS_COLOR_CODES

from staff import is_user_in_workgroup, is_user_manager, is_user_submitter

#https://github.com/HonzaKral/custom_admin_form/blob/master/adhack/adapp/admin.py
#http://www.ibm.com/developerworks/opensource/library/os-django-admin/index.html


# -------  audit & history state ---------
#http://djangosnippets.org/snippets/1234/
#https://bitbucket.org/q/django-simple-history/src/da88a95fbd5a/simple_history/models.py
#http://code.google.com/p/fullhistory/source/checkout
#https://github.com/smn/django-historicalrecords
#https://bitbucket.org/carljm/django-model-utils/src

class TicketAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.fieldsets = (
                (None, {
                        'fields': ( "title", 
                                    ( "kind"),
                                    ("project", "milestone"),
                                    ("component","url",),
                                    "description",
                                    ("priority"),
                                    "estimated_time",
                                    ( "commit_id"), 
                                    'image',
                                  )
                }),
            )
            #self.fields = ('status',)
        elif is_user_manager( obj, request.user):
            self.fieldsets = (
                (None, {
                        'fields': ( "title", 
                                    ("status", "kind"),
                                    ("project", "milestone"),
                                    ("component","url",),
                                    "description",
        							("assigned_to","priority"),
        							"estimated_time",
        							("commit_id"), 
        							'image',
                                  )
                }),
            )
        else:
            self.fields = ('status',)

        form = super(TicketAdmin, self ).get_form( request, obj, **kwargs)
        return form


    def get_related_logs(self, object_id):
        from django.contrib.admin.models import LogEntry
        model = self.model
        return LogEntry.objects.filter(
             object_id = object_id,
             content_type__id__exact = ContentType.objects.get_for_model(model).id
         ).select_related().order_by('action_time')


    def change_view(self, request, object_id, extra_context=None):
        obj = self.get_object(request, object_id)
        
        if is_user_manager(obj, request.user): #or request.user is component_responsable:
            self.change_form_template = "admin/tracker/ticket/change_form.html"
        else:
            self.change_form_template = "admin/tracker/ticket/user_change_form.html"
            #self.change_form_template = "admin/tracker/ticket/change_form.html"
        note_kwargs = dict(
            prefix = "note",
            initial = { "ticket":obj.id },
        )
        extra_context = extra_context or {
             "history": self.get_related_logs(object_id),
             "note_form":CreateNoteForm(**note_kwargs),
        }
        return super(TicketAdmin, self).change_view(
            request, 
            object_id, 
            extra_context=extra_context
        )


    def save_model(self, request, obj, form, change):
        if obj.id:
            obj.modified_by = request.user
        else:
            obj.submitter = request.user
        obj.save()
    
    def get_urls(self):
            urls = super(TicketAdmin, self).get_urls()
            my_urls = patterns('',
                (r'^(\d*)/note/$', self.admin_site.admin_view(self.note_form),)
            )
            return my_urls + urls
            
    def note_form(self, request, ticket_id):
        from tracker.forms import CreateNoteForm
        
        form = CreateNoteForm( request.POST, request.FILES )
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
        return HttpResponseRedirect("../")
        
    def status_color(self, obj):
            return '<span style="background: %s; color:black; display: block">%s</span>' % (
                STATUS_COLOR_CODES[ obj.status - 1 ][1], obj.get_status_display() 
            )
    
    def log_change(self, request, object, message):
        # "log_change" signal do the job
        pass
    
    #https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_for_manytomany
    def formfield_for_choice_field(self, db_field, request, **kwargs):
            if db_field.name == "status": #TODO!!!! adjust available satatus according to current status
                if request.user.is_superuser:
                    pass #models.TextField: {'widget': forms.HiddenInput },
                else:
                    pass
            if db_field.name == "milestone":
                kwargs['choices'] = Milestone.objects.filter(milestone__project__exact = self.original.project )
            if db_field.name == "component":
                kwargs['choices'] = self.original.project.component_set.all()
            return super(TicketAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
            
    
    
    status_color.short_description = 'status'
    status_color.allow_tags = True
    
    ordering = ('-submitted_date',)
    date_hierarchy = 'submitted_date'
    list_display = ( 'title', "id", 'status_color',  "submitted_date", "priority",  'kind',   )
    
    search_fields = ('title', 'id', 'project', 'description', "commit_id" )

    list_filter = ( "project", "priority", 'status',  'kind',  'project', 'assigned_to', )


class ComponentInline(admin.StackedInline):

    #def save_new(self, form, commit=True): 
    model = Component
    #readonly_fields = ( "created_at", "created_by")
    extra = 1

class MilestoneInline(admin.StackedInline):

    model = Milestone
    
    fieldsets = (
        (None, {
                'fields': ( 
                            ( "version", "title",),
                            "description",
							("deadline","reached_at"),
                          )
        }),
    )
    extra = 1
    
class ProjectAdmin(admin.ModelAdmin):
    
    inlines = [
            ComponentInline,
            MilestoneInline,
    ]
    fieldsets = (
        (None, {
                'fields': ( 
                            ("name", "slug"),
                            "is_active",
                            "description",
                            "url",
							("project_manager","subbmitters"),
                          )
        }),
    )

    prepopulated_fields = {"slug": ("name",)}
    list_display = ( 'name', "id", 'is_active', "project_manager", "subbmitters", )
    list_filter = ( "is_active",  )
                
admin.site.register( Ticket, TicketAdmin )
admin.site.register( Project, ProjectAdmin )