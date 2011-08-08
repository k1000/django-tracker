# -*- coding: utf-8 -*-
from django import forms

from models import Note, Ticket

class CreateNoteForm(forms.ModelForm):
    class Meta():
        model = Note
        exclude = ("created_at", "created_by",)
        widgets ={
            "ticket":forms.HiddenInput(),
        }

class StatusTicketForm(forms.ModelForm):
    
    def __init__(self, data=None, files=None, instance=None, **kwargs):
        self._instance = instance
        super(StatusTicketForm, self).__init__(data, files, **kwargs)
            
    class Meta():
        model = Ticket
        fields = ("status",)
        
    def save(self, commit=True):
            obj = self._instance or Ticket()
            #obj.name = self.cleaned_data['subject']
            #obj.question = 'Do you really think %(subject)s is %(adverb)s %(adjective)s?' % self.cleaned_data
            if commit:
                obj.save()

            self._instance = obj
            return obj


class LogForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    