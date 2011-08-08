# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User, Group

from tracker.settings import *
from previous_state_mixin import PreviousStateMixin

class Project(models.Model):
    """(Project description)"""

    name = models.CharField(_('name'), null=True, blank=True, max_length=200)
    slug = models.SlugField(_('identificador'),)
    description = models.TextField(_(u'descripción'), blank=True, null=True, )
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(_("creado"), auto_now_add=True)
    is_active = models.BooleanField(_("¿es activo?"), default=True)
    project_manager = models.ForeignKey(User, 
            verbose_name=_("encargado del proyecto"),
    )
    subbmitters = models.ForeignKey(Group, 
            verbose_name=_("creadores de tickets"),
            blank=True, null=True,
            related_name = "related_submitters",
            help_text = _(u"deje en blanco si todos los miembros del personal pueden crear tickets")
    )
    workgroup = models.ForeignKey(Group, 
            verbose_name=_("grupo de trabajo"),
            blank=True, null=True,
            related_name = "related_workgroups",
            help_text = _(u"deje en blanco si todos los miembros del personal pueden editar tickets")
    )

    def get_staff():
        """
        Returns asigned workgroup or all admin staff
        """
        return self.workgroup or User.objects.filter(is_staff = True, is_active=True)

    def get_subbmitters():
        return self.subbmitters or User.objects.filter(is_staff = True, is_active=True)

    class Meta:
        verbose_name = _('Proyecto')
        verbose_name_plural = _('Proyectos')

    def __unicode__(self):
        return self.name

class Component(models.Model):
    """(Component description)"""
    project = models.ForeignKey(Project, 
        verbose_name=_("Proyecto"),
        related_name = "related_componets",
    )
    name = models.CharField(_('name'), max_length=250)
    description = models.TextField(_(u'descripción'), blank=True, null=True, )
    responsable = models.ForeignKey(User, 
            verbose_name=_("responsable"),
            related_name = "related_resonsables",
            null=True, blank=True,
    )
    workteam = models.ForeignKey(Group, 
            verbose_name=_("grupo de trabajo"),
            blank=True, null=True, 
    )
    
    class Meta:
        verbose_name = _('Componente')
        verbose_name_plural = _('Componentes')

    def __unicode__(self):
        return self.name

class Milestone(models.Model):
    """(Milestone description)"""
    
    project = models.ForeignKey(Project, verbose_name=_("Proyecto"), )
    title = models.CharField(_('titulo'), max_length=200)
    description = models.TextField(_(u'descripción'), blank=True, null=True)
    version = models.CharField(_(u'versión'), max_length=100)
    deadline = models.DateField(_('por alcanzar'), blank=True, null=True, )
    reached_at = models.DateField(_('alcanzado'), blank=True, null=True, )

    class Meta:
        verbose_name = _('Hito')
        verbose_name_plural = _('Hitos')

    def __unicode__(self):
        return self.title

class Ticket(models.Model, PreviousStateMixin):
    """Trouble tickets"""
    
    project = models.ForeignKey(Project, 
        verbose_name=_("Proyecto"), 
        related_name="related_projects", 
    )
    title = models.CharField(_("titulo"), max_length=250)
    url = models.URLField(_("URL"), blank=True, null=True, verify_exists=False)
    submitted_date = models.DateTimeField(_("creado"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modificado"), auto_now=True)
    modified_by = models.ForeignKey(SUBMITTER_USER_CLS, 
            related_name="related_modified_by", 
            verbose_name=_("modificado por"),
            limit_choices_to = LIMIT_SUBMITTER_USERS,
    )
    modifiaction_message = models.TextField(_(u"mensaje de modificación"),
            null=True, blank=True,
    )
    submitter = models.ForeignKey(SUBMITTER_USER_CLS, 
            related_name="related_submitters", 
            verbose_name=_("creado por"),
            limit_choices_to = LIMIT_SUBMITTER_USERS,
    )
    assigned_to = models.ForeignKey(ASIGNED_USER_CLS, 
            verbose_name=_("asignado"), 
            related_name = "related_asigned",
            null=True, blank=True,
            limit_choices_to = LIMIT_ASIGNED_USERS,
    )
    description = models.TextField(_(u"descripción"), blank=True, null=True)
    status = models.PositiveIntegerField(_("status"), 
            default=1, #open
            choices=STATUS_CODES)
    priority = models.PositiveIntegerField(_("prioridad"), 
            default=DEFAULT_PRIORITY, 
            choices=PRIORITY_CODES)
    kind = models.PositiveIntegerField(_("tipo"), 
            default=1, 
            choices=KIND_CODES)
    commit_id = models.CharField(_(u'revisión nº'), blank=True, null=True, max_length=100)
    image = models.ImageField(_("imagen"), 
            blank=True, null=True, 
            upload_to=IMAGE_UPLOAD_DIR, )
    milestone = models.ForeignKey(Milestone, 
            verbose_name=_("hito"),
            blank=True, null=True,
    )
    component = models.ForeignKey(Component, 
            verbose_name=_("componente"),
            blank=True, null=True,
    )
    estimated_time = models.DecimalField(
        _(u"estimado tiempo de ejecución"), 
        max_digits=4, decimal_places=2,
        null=True, blank=True,
        help_text =_("en horas")
    )

    def get_related_staff(self):
        return (self.component and self.component.workteam) or self.project.workgroup

        
    def __unicode__(self):
        return u"#%s: %s" % ( self.id, self.title )

        

class StatusChange(models.Model):
    """(Log description)"""
    ticket = models.ForeignKey(Ticket, 
        related_name='releted_logs', 
        verbose_name=_("ticket")
    )
    message = models.TextField(_("mensaje"), blank=True, null=True)
    changes = models.TextField(_("cambios"), )
    changed_at = models.DateTimeField(_("fecha"), auto_now_add=True)
    changed_by = models.ForeignKey(User, 
            verbose_name=_("hecho por"),
    )
    class Meta:
        verbose_name = _('Cambio de Estado')
        verbose_name_plural = _('Cambios de Estado')

    def __unicode__(self):
        return u"change %s by %s" % (self.changed_at, self.changed_by)

        
class Note(models.Model):
    '''A Comment is some text about a given Document'''
    ticket = models.ForeignKey(Ticket, 
        related_name='comments', 
        verbose_name=_("ticket")
    )
    text = models.TextField(_("nora"), help_text = "se pude dar el formato al text usando textile ")
    created_at = models.DateTimeField( _(u"fecha creación"), auto_now_add=True)
    created_by = models.ForeignKey(ASIGNED_USER_CLS, 
        related_name='related_creators', 
        verbose_name=_("creado por")
    )
    attachment = models.FileField(
        _("fichero adjunto"), 
        upload_to=FILE_UPLOAD_DIR,
        blank=True, null=True,
        help_text=_("pude ser patch etc."),
    )
    
    def __unicode__(self):
        return self.text
