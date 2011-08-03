# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect

from tracker.models import Ticket, Note, Project, Component, Milestone
from settings import STATUS_COLOR_CODES

#https://github.com/HonzaKral/custom_admin_form/blob/master/adhack/adapp/admin.py
"""
class NoteInlineForm(forms.Form):
    subject = forms.CharField(max_length=30)
    adverb = forms.CharField(max_length=30)
    adjective =  forms.CharField(max_length=30)

    options = forms.CharField(widget=forms.Textarea)

    def __init__(self, data=None, files=None, instance=None, **kwargs):
        self._instance = instance
        super(NoteInline, self).__init__(data, files, **kwargs)

    def save_m2m(self):
        opts = self.cleaned_data['options'].split('\n')
        for opt in opts:
            self._instance.polloption_set.create(text=opt.strip())


    def save(self, commit=True):
        obj = self._instance or Poll()

        obj.name = self.cleaned_data['subject']
        obj.question = 'Do you really think %(subject)s is %(adverb)s %(adjective)s?' % self.cleaned_data
        if commit:
            obj.save()

        self._instance = obj

        return obj
"""
#http://www.ibm.com/developerworks/opensource/library/os-django-admin/index.html
class NoteInline(admin.TabularInline):
    
    #def save_new(self, form, commit=True): 
    def save_model(self, request, obj, form, change):
        obj = form.save(commit=False)
        pk_value = getattr(self.instance, self.fk.rel.field_name)
        setattr(obj, self.fk.get_attname(), getattr(pk_value, 'pk', pk_value))
        if commit:
            obj.created_by = self.request.user
            obj.save()
        # form.save_m2m() can be called via the formset later on if commit=False
        if commit and hasattr(form, 'save_m2m'):
            form.save_m2m()
        obj.save()
        
    model = Note
    readonly_fields = ( "created_at", "created_by")
    extra = 1
    
class TicketAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change): 
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
    
    #https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_for_manytomany
    def formfield_for_choice_field(self, db_field, request, **kwargs):
            if db_field.name == "milestone":
                kwargs['choices'] = Milestone.objects.filter(milestone__project__exact = self.original.project )
            return super(TicketAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)
            
    fieldsets = (
        (None, {
                'fields': ( "title", 
                            ("status", "kind"),
                            ("project", "milestone"),
                            "description",
                            "url",
							("assigned_to","priority"),
							"estimated_time",
							( "commit_id"), 
							'image',
                          )
        }),
    )
    
    status_color.short_description = 'status'
    status_color.allow_tags = True
    
    ordering = ('-submitted_date',)
    date_hierarchy = 'submitted_date'
    list_display = ( 'title', "id", 'status_color',  "submitted_date", "priority",  'kind',   )
    
    search_fields = ('title', 'id', 'project', 'description', "commit_id" )

    list_filter = ( "priority", 'status',  'kind',  'project', 'assigned_to', )


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