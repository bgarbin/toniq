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
    
    for subName,subDriver in [('tic',devDriver.tic),('tac',devDriver.tac)] :
    
        subDevUsit = devUsit.addModule(subName)             
        
        subDevUsit.addVariable('velocity',float,
                            setFunction=subDriver.setVelocity,
                            getFunction=subDriver.getVelocity)
        
        subDevUsit.addVariable('acceleration',float,
                            setFunction=subDriver.setAcceleration,
                            getFunction=subDriver.getAcceleration)
        
        subDevUsit.addVariable('angle',float,
                            setFunction=subDriver.setAngle,
                            getFunction=subDriver.getAngle)
        
        subDevUsit.addVariable('transmission',float,
                            setFunction=subDriver.setTransmission,
                            getFunction=subDriver.getTransmission)
        
        subDevUsit.addAction('setMin',
                          function=subDriver.setMin)
        
        subDevUsit.addAction('setMax',
                          function=subDriver.setMax)
        
        subDevUsit.addAction('goHome',
                          function=subDriver.goHome)
        
    
    
    