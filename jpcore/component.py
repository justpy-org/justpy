'''
Created on 2022-09-13

@author: wf
'''
from jpcore.tailwind import Tailwind

# @TODO refactor as per #528
class Component(Tailwind):
    """
    keep track of ids an instances
    """
    next_id = 1
    instances = {}    
