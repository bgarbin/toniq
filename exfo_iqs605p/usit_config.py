# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:47:17 2019

@author: quentin.chateiller
"""

def configure(devDriver,devUsit):
    """
    This script configures Usit to use your device properly.
    devDriver is an instance of the class Device() located in the script driver.py
    devUsit is a Usit Device object that this function is supposed to configure, 
    by affecting the functions contained in devDriver to variable and actions objects 
    of the devUsit object.
    """
    
    iqs9100b = devUsit.addModule('iqs9100b')
    
    
    iqs9100b.addVariable('route',int,
                    setFunction=devDriver.iqs9100b.setRoute,
                    getFunction=devDriver.iqs9100b.getRoute)
    
    iqs9100b.addVariable('shutter',bool,
                    setFunction=devDriver.iqs9100b.setShutter,
                    getFunction=devDriver.iqs9100b.isShuttered)
    