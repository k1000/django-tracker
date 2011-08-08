# -*- coding: utf-8 -*-

#https://github.com/citylive/django-states2

#inspired on http://stackoverflow.com/questions/110803/dirty-fields-in-django
class PreviousStateMixin(object):
    def __init__(self, *args, **kwargs):
        super(PreviousStateMixin, self).__init__(*args, **kwargs)
        self._previous_state = self._as_dict()

    def _reset_state(self, *args, **kwargs):
        self._previous_state = self._as_dict()

    def _as_dict(self):
        return dict([(f.name, f.value_to_string(self) ) for f in self._meta.local_fields])

    def get_updated_fields(self):
        new_state = self._as_dict()
        return dict([(key, [ value, new_state[key] ]) 
                for key, value in self._previous_state.iteritems() if value != new_state[key]])
