# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

import datetime
rules = {
    1:(
        lambda obj: obj.created < datetime.datetime.now()
        and
        lambda obj: obj.is_active
    )
}


class StateBase(models.Model):
    """(State description)"""
    name = models.CharField(_('name'), blank=True, max_length=200)
    move_next_state = models.BooleanField(default=True, help_text="move to next state automaticaly")
    next_state = models.ForeignKey(self,)

    def check_rule(self):
        obj = self
        return rules[self.pk]
           
    class Meta:
        abstract = True

class State(StateBase):
    """(State description)"""
    description = models.TextField(blank=True, null=True)
    


    class Meta:
        abstract = True
        verbose_name = _('State')
        verbose_name_plural = _('States')

    def __unicode__(self):
        return self.name

    

class Transition(models.Model):
    """(Transition description)"""
    destination = models.ForeignKey(State)
    
    
    class Meta:
        verbose_name = _('Transition')
        verbose_name_plural = _('Transitions')

    def __unicode__(self):
        return u"Transition"
    
    @models.permalink
    def get_absolute_url(self):
        return #('perfil-edit', (), { 'user':self.username,},  )


    


