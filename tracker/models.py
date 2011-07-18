# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

from notify import notify_staff

from django.conf import settings
# Create your models here.

STATUS_CODES = (
    (1, 'Abierto'),
    (2, 'En proceso'),
    (3, 'Cerrado'),
    (4, 'Ignorado'),
    )

KIND_CODES = (
    (1, 'Error'),
    (2, u'Correción linguistica'),
    (3, 'Mejora'),
    )
        
PRIORITY_CODES = (
    (1, 'Urgente'),
    (2, 'Pronto'),
    (3, u'Algun día'),
    )
    
EXCLUDE_APPS = []
EXCLUDE_APPS += [ app for app in settings.INSTALLED_APPS if "django." in app ]
apps = [ app for app in settings.INSTALLED_APPS if app not in EXCLUDE_APPS ]
PROJECTS = list(enumerate(apps))

class Ticket(models.Model):
    """Trouble tickets"""
    title = models.CharField(_("titulo"), max_length=250)
    project = models.PositiveIntegerField(_(u"modulo afectado"), blank=True, null=True, max_length=100, choices=PROJECTS)
    url = models.URLField(_("url"), blank=True, null=True, verify_exists=False)
    submitted_date = models.DateTimeField(_("creado"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modificado"), auto_now=True)
    submitter = models.ForeignKey(User, related_name="submitter", verbose_name=_("creado por"),)
    assigned_to = models.ForeignKey(User, verbose_name=_("asignado"), limit_choices_to = {'is_staff__exact': True})
    description = models.TextField(_(u"descripción"), blank=True, null=True)
    status = models.PositiveIntegerField(_("status"), default=1, choices=STATUS_CODES)
    priority = models.PositiveIntegerField(_("prioridad"), default=1, choices=PRIORITY_CODES)
    kind = models.PositiveIntegerField(_("tipo"), default=1, choices=KIND_CODES)
    commit_id = models.CharField(_('id del cometido'), blank=True, null=True, max_length=100)
    image = models.ImageField(blank=True, null=True, upload_to="uploads/tracker", )

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