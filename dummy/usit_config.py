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
        
    
    devUsit.addVariable('amplitude',float,
                        getFunction=devDriver.getAmplitude,
                        setFunction=devDriver.setAmplitude,
                        unit='V')
    
    devUsit.addVariable('phase',float,
                        getFunction=devDriver.getPhase)
    
    devUsit.addAction('sth',
                        function=devDriver.doSth)