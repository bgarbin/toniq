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
    
    toc = devUsit.addModule('toc')
    
    
    toc.addVariable('velocity',float,
                        setFunction=devDriver.toc.setVelocity,
                        getFunction=devDriver.toc.getVelocity)
    
    toc.addVariable('acceleration',float,
                        setFunction=devDriver.toc.setAcceleration,
                        getFunction=devDriver.toc.getAcceleration)
    
    toc.addVariable('angle',float,
                        setFunction=devDriver.toc.setAngle,
                        getFunction=devDriver.toc.getAngle)
    
    toc.addVariable('transmission',float,
                        setFunction=devDriver.toc.setTransmission,
                        getFunction=devDriver.toc.getTransmission)
    
    toc.addAction('setMin',
                      function=devDriver.toc.setMin)
    
    toc.addAction('setMax',
                      function=devDriver.toc.setMax)
    
    toc.addAction('goHome',
                      function=devDriver.toc.goHome)
        
    
    
    