from django import template

from tracker.forms import CreateNoteForm

register = template.Library()

#@register.simple_tag(takes_context=True)

def note_form(context):
    initial = {
        "ticket":context["original"]
    }
    if initial["ticket"].id:
        note_form = CreateNoteForm(initial)
    else:
        note_form = None
    return { "note_form":note_form }
        
    
register.inclusion_tag('tracker/note_form.html', takes_context=True)(note_form)