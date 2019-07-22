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

    devUsit.addVariable('exposureTime',float,
                        setFunction=devDriver.setExposureTime,
                        getFunction=devDriver.getExposureTime)
    
    devUsit.addVariable('autoExposureTime',bool,
                        setFunction=devDriver.setAutoExposureTimeEnabled,
                        getFunction=devDriver.isAutoExposureTimeEnabled)
    
    devUsit.addVariable('autoBackgroundRemoval',bool,
                        setFunction=devDriver.setAutoBackgroundRemovalEnabled,
                        getFunction=devDriver.isAutoBackgroundRemovalEnabled)
    
    devUsit.addVariable('spectrum','dataframe',
                        getFunction=devDriver.getSpectrum)
    
    devUsit.addVariable('temperature',float,
                        getFunction=devDriver.getTemperature)
    
    devUsit.addVariable('mainPeakWavelength',float,
                        getFunction=devDriver.getMainPeakWavelength)
    
    devUsit.addVariable('mainPeakFwhm',float,
                        getFunction=devDriver.getMainPeakFWHM)
    
    devUsit.addVariable('maxPower',float,
                        getFunction=devDriver.getMaxPower)
    
    devUsit.addVariable('integratedPower',float,
                        getFunction=devDriver.getIntegratedPower)
    
    devUsit.addAction('acquire',
                      function=devDriver.acquireSpectrum)
    
    
    