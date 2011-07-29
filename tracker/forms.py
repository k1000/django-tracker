# -*- coding: utf-8 -*-
from django import forms

from models import Note

class CreateNoteForm(forms.ModelForm):
    class Meta():
        model = Note
        exclude = ("created_at", "created_by",)
        widgets ={
            "ticket":forms.HiddenInput(),
        }
    