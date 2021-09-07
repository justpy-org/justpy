from .htmlcomponents import *
import demjson
from addict import Dict


# class Formula(Div):
#
#     vue_type = 'katexjp'
#
#     def __init__(self, **kwargs):
#         self.formula = ''
#         self.raw = False
#         self.options = {'macros': {}}
#         kwargs['temp'] = False  # Force an id to be assigned
#         super().__init__(**kwargs)
#
#     def convert_object_to_dict(self):
#         d = super().convert_object_to_dict()
#         d['formula'] = self.formula
#         d['raw'] = self.raw
#         self.options['throwOnError'] = False
#         d['options'] = self.options
#         return d
#
#
