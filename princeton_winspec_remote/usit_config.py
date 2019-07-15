# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:47:17 2019

@author: quentin.chateiller
"""

import pandas as pd

def configure(devDriver,devUsit):
    """
    This script configures Usit to use your device properly.
    devDriver is an instance of the class Device() located in the script driver.py
    devUsit is a Usit Device object that this function is supposed to configure, 
    by affecting the functions contained in devDriver to variable and actions objects 
    of the devUsit object.
    """
    
    toc = devUsit.addSubDevice('toc')
    

    toc.addVariable('exposureTime',float,
                        setFunction=devDriver.toc.setExposureTime,
                        getFunction=devDriver.toc.getExposureTime)
    
    toc.addVariable('autoExposureTime',bool,
                        setFunction=devDriver.toc.setAutoExposureTimeEnabled,
                        getFunction=devDriver.toc.isAutoExposureTimeEnabled)
    
    toc.addVariable('spectrum',pd.DataFrame,
                        getFunction=devDriver.toc.getSpectrum)
    
    toc.addVariable('temperature',float,
                        getFunction=devDriver.toc.getTemperature)
    
    toc.addVariable('mainPeakWavelength',float,
                        getFunction=devDriver.toc.getMainPeakWavelength)
    
    toc.addVariable('mainPeakFwhm',float,
                        getFunction=devDriver.toc.getMainPeakFWHM)
    
    toc.addVariable('maxPower',float,
                        getFunction=devDriver.toc.getMaxPower)
    
    toc.addVariable('integratedPower',float,
                        getFunction=devDriver.toc.getIntegratedPower)
    
    toc.addAction('acquire',
                      function=devDriver.toc.acquireSpectrum)
    
    
    