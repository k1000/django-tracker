# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from notify import notify_staff

from tracker.settings import *


class Ticket(models.Model):
    """Trouble tickets"""
    title = models.CharField(_("title"), max_length=250)
    url = models.URLField(_("URL"), blank=True, null=True, verify_exists=False)
    submitted_date = models.DateTimeField(_("created"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified"), auto_now=True)

    submitter = models.ForeignKey(SUBMITTER_USER_CLS,
            related_name="submitter",
            verbose_name=_("created by"),
            limit_choices_to=LIMIT_SUBMITTER_USERS,
    )
    notify_submitter = models.BooleanField(_("notify creator"), default=True)

    assigned_to = models.ForeignKey(ASIGNED_USER_CLS,
            verbose_name=_("assigned to"),
            limit_choices_to=LIMIT_ASIGNED_USERS,
    )

    description = models.TextField(_(u"description"), blank=True, null=True)
    status = models.PositiveIntegerField(_("status"),
            default=1,
            choices=STATUS_CODES)
    priority = models.PositiveIntegerField(_("priority"),
            default=DEFAULT_PRIORITY,
            choices=PRIORITY_CODES)
    #browser_profile = models.TextField(_("perfil del navegador"), blank=True, null=True )
    kind = models.PositiveIntegerField(_("type"),
            default=1,
            choices=KIND_CODES)
    commit_id = models.CharField(_(u'revision nº'), blank=True, null=True, max_length=100)
    attachment = models.FileField(_("attachement"),
            blank=True, null=True,
            upload_to=IMAGE_UPLOAD_DIR, )

    if PROJECT_INTEGRATION:
        project = models.PositiveIntegerField(_(u"afected module"),
                    blank=True, null=True,
                    max_length=100,
                    choices=PROJECTS)

    if MULTISITE:
        from django.contrib.sites.models import Site
        sites = models.ForeignKey(Site, verbose_name=_("Webs"), related_name="related_sites", )

    def __unicode__(self):
        return "#%s %s" % (self.id, self.title)

    def save(self, *args, **kwargs):
        super(Ticket, self).save(*args, **kwargs)
        if EMAIL_NOTIFIY:
            if self.assigned_to:
                notify_staff(self)


class Note(models.Model):
    '''A Comment is some text about a given Document'''
    ticket = models.ForeignKey(Ticket,
        related_name='comments',
        verbose_name=_("ticket")
    )
    text = models.TextField(_("note"), help_text="text may be formated using 'textile'")
    created_at = models.DateTimeField(_(u"creation date"), auto_now_add=True)
    created_by = models.ForeignKey(ASIGNED_USER_CLS,
        related_name='created',
        verbose_name=_("created by")
    )
    attachment = models.FileField(
        _("attachement"),
        upload_to=FILE_UPLOAD_DIR,
        blank=True, null=True,
        help_text=_("patch etc."),
    )

    def __unicode__(self):
        return self.text
