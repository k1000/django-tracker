# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from notify import notify_staff

from tracker.settings import *

class Ticket(models.Model):
    """Trouble tickets"""
    title = models.CharField(_("titulo"), max_length=250)
    url = models.URLField(_("URL"), blank=True, null=True, verify_exists=False)
    submitted_date = models.DateTimeField(_("creado"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modificado"), auto_now=True)
    
    submitter = models.ForeignKey(SUBMITTER_USER_CLS, 
            related_name="submitter", 
            verbose_name=_("creado por"),
            limit_choices_to = LIMIT_SUBMITTER_USERS,
    )
    notify_submitter = models.BooleanField(_("notificar el creador"), default=True)
    
    assigned_to = models.ForeignKey(ASIGNED_USER_CLS, 
            verbose_name=_("asignado"), 
            limit_choices_to = LIMIT_ASIGNED_USERS,
    )
    
    description = models.TextField(_(u"descripción"), blank=True, null=True)
    status = models.PositiveIntegerField(_("status"), 
            default=1, 
            choices=STATUS_CODES)
    priority = models.PositiveIntegerField(_("prioridad"), 
            default=DEFAULT_PRIORITY, 
            choices=PRIORITY_CODES)
    #browser_profile = models.TextField(_("perfil del navegador"), blank=True, null=True )
    kind = models.PositiveIntegerField(_("tipo"), 
            default=1, 
            choices=KIND_CODES)
    commit_id = models.CharField(_(u'revisión nº'), blank=True, null=True, max_length=100)
    image = models.ImageField(_("imagen"), 
            blank=True, null=True, 
            upload_to=IMAGE_UPLOAD_DIR, )
    
    
    if PROJECT_INTEGRATION:
        project = models.PositiveIntegerField(_(u"módulo afectado"), 
                    blank=True, null=True, 
                    max_length=100, 
                    choices=PROJECTS)
        
    if MULTISITE:
        from django.contrib.sites.models import Site
        sites = models.ForeignKey(Site, verbose_name=_("Webs"), related_name="related_sites", )
        
    def __unicode__(self):
        return "#%s %s" % ( self.id, self.title )
        
    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)
        if EMAIL_NOTIFIY:
            if self.assigned_to:
                notify_staff( self )
