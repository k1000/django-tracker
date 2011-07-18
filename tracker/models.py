# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from notify import notify_staff

from tracker.settings import *
# Create your models here.

class Ticket(models.Model):
    """Trouble tickets"""
    title = models.CharField(_("titulo"), max_length=250)
    url = models.URLField(_("url"), blank=True, null=True, verify_exists=False)
    submitted_date = models.DateTimeField(_("creado"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modificado"), auto_now=True)
    submitter = models.ForeignKey(User, related_name="submitter", verbose_name=_("creado por"),)
    assigned_to = models.ForeignKey(User, verbose_name=_("asignado"), limit_choices_to = {'is_staff__exact': True})
    description = models.TextField(_(u"descripción"), blank=True, null=True)
    status = models.PositiveIntegerField(_("status"), default=1, choices=STATUS_CODES)
    priority = models.PositiveIntegerField(_("prioridad"), default=1, choices=PRIORITY_CODES)
    kind = models.PositiveIntegerField(_("tipo"), default=1, choices=KIND_CODES)
    commit_id = models.CharField(_(u'revisión nº'), blank=True, null=True, max_length=100)
    image = models.ImageField(_("imagen"), blank=True, null=True, upload_to="uploads/tracker", )
    
    if PROJECT_INTEGRATION:
        project = models.PositiveIntegerField(_(u"módulo afectado"), blank=True, null=True, max_length=100, choices=PROJECTS)
        
    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)
        if self.assigned_to:
            notify_staff( self )

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="related_ticet")
    text = models.TextField(_("comentario"))
    created_by = models.ForeignKey(User, related_name="creator", verbose_name=_("creado por"),)
    created_at = models.DateTimeField(_("creado"), auto_now=True)
    attachment = models.FileField(upload_to="uploads/tracker/attachments")