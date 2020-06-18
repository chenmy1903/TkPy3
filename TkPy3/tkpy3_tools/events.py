# -*- coding: UTF-8 -*-
from TkPy3.default_configs import get_configs
class TkPyEventType(object):
    name: str

    def __init__(self, name: str = None):
        self.name = name

    def text(self):
        return self.name or 'TkPy3 Event type'

    def __repr__(self):
        return 'TkPy3 PyQt5 Event types.'

def get_event(event_name: str):
    return get_configs()['events'][event_name]
