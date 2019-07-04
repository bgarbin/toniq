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
    
    for subName,subDriver in [('slot1',devDriver.slot1),('slot2',devDriver.slot2)] :
    
        subDevUsit = devUsit.addModule(subName)  
        
        subDevUsit.addVariable('averagingState',bool,
                           setFunction=subDriver.setAveragingState,
                           getFunction=subDriver.getAveragingState)
        
        subDevUsit.addVariable('bufferSize',int,
                           setFunction=subDriver.setBufferSize,
                           getFunction=subDriver.getBufferSize)
        
        subDevUsit.addVariable('wavelength',float,
                           setFunction=subDriver.setWavelength,
                           getFunction=subDriver.getWavelength)
        
        subDevUsit.addVariable('power',float,
                           getFunction=subDriver.getPower)
    
    
    