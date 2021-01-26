# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from suit.apps import DjangoSuitConfig

class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'
    
class ScolarityConfig(AppConfig):
    name = 'Scolarity'
