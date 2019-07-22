# -*- coding: utf-8 -*-
"""
Created on Thu May  2 16:47:17 2019

@author: quentin.chateiller
"""

def configure(devDriver,devUsit):

    
    toc = devUsit.addModule('toc')
    
    
    toc.addVariable('velocity',
                        setFunction=devDriver.toc.setVelocity,
                        getFunction=devDriver.toc.getVelocity)
    
    toc.addVariable('acceleration',
                        setFunction=devDriver.toc.setAcceleration,
                        getFunction=devDriver.toc.getAcceleration)
    
    toc.addVariable('angle',
                        setFunction=devDriver.toc.setAngle,
                        getFunction=devDriver.toc.getAngle)
    
    toc.addVariable('transmission',
                        setFunction=devDriver.toc.setTransmission,
                        getFunction=devDriver.toc.getTransmission)
    
    toc.addAction('setMin',
                      function=devDriver.toc.setMin)
    
    toc.addAction('setMax',
                      function=devDriver.toc.setMax)
    
    toc.addAction('goHome',
                      function=devDriver.toc.goHome)
        
    
    
    