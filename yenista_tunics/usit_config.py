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
        
    
    devUsit.addVariable('wavelength',float,
                        setFunction=devDriver.setWavelength,
                        getFunction=devDriver.getWavelength)
    
    devUsit.addVariable('frequency',float,
                        setFunction=devDriver.setFrequency,
                        getFunction=devDriver.getFrequency)
    
    devUsit.addVariable('power',float,
                        setFunction=devDriver.setPower,
                        getFunction=devDriver.getPower)
    
    devUsit.addVariable('intensity',float,
                        setFunction=devDriver.setIntensity,
                        getFunction=devDriver.getIntensity)
    
    devUsit.addVariable('output',float,
                        setFunction=devDriver.setOutput,
                        getFunction=devDriver.getOutput)
    
    