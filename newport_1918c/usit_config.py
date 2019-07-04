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
    
    devUsit.addAction('zero',
                       function=devDriver.setZero)
    
    devUsit.addVariable('autorange',bool,
                       setFunction=devDriver.setAutoRange,
                       getFunction=devDriver.getAutoRange)
    
    devUsit.addVariable('zeroValue',float,
                       setFunction=devDriver.setZeroValue,
                       getFunction=devDriver.getZeroValue)
    
    devUsit.addVariable('bufferSize',int,
                       setFunction=devDriver.setBufferSize,
                       getFunction=devDriver.getBufferSize)
    
    devUsit.addVariable('bufferInterval',float,
                       setFunction=devDriver.setBufferInterval,
                       getFunction=devDriver.getBufferInterval)
    
    devUsit.addVariable('wavelength',float,
                       setFunction=devDriver.setWavelength,
                       getFunction=devDriver.getWavelength)
    
    devUsit.addVariable('power',float,
                       getFunction=devDriver.getPower)
    
    devUsit.addVariable('powerMean',float,
                       getFunction=devDriver.getPowerMean)
    

    