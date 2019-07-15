# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:22:53 2019

@author: quentin.chateiller
"""
from winspec_gui_driver import Winspec

class WinspecConnector :
    
    def __init__(self):
        self.controller = Winspec()
              
    def write(self,command):
        self.controller.command(command)
        
    def query(self,command):
        return self.controller.command(command)
        
    def close(self):
        self.controller = None
