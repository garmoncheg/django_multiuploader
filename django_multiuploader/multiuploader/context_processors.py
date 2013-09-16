# -*- coding:utf-8 -*-
from django.utils.crypto import  get_random_string

def booleans(request):
    return { 
            'True': True,
            'False': False 
        }