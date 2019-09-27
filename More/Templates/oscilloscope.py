#!/usr/bin/env python3

"""
Supported instruments (identified):
- 
"""

import sys,os
import time
from numpy import fromstring,int8,int16,float64,sign
import pandas


#################################################################################
############################## Connections classes ##############################
class Device_TCPIP():
    def __init__(self, address, **kwargs):
        import visa as v
        
        Device.__init__(self, **kwargs)
        
        rm        = v.ResourceManager()
        self.inst = rm.get_instrument(address)


    def query(self,command):
        return self.inst.query(command)

    def read(self):
        return self.inst.read()

    def write(self,command):
        self.inst.write(commande,length=self.length)


class Device_VXI11():
    def __init__(self, address, **kwargs):
        import vxi11 as v
    
        Device.__init__(self, **kwargs)
        
        self.inst = v.Instrument(address)


    def query(self,command):
        return self.inst.query(command)

    def read(self):
        return self.inst.read()

    def write(self,command):
        self.inst.write(commande,length=self.length)
############################## Connections classes ##############################
#################################################################################


class Device():
    def __init__(self,nb_channels=4):
              
        self.nb_channels = nb_channels
        
        for i in range(1,self.nb_channels+1):
            setattr(self,f'channel{i}',Channel(self,i))
    
    
    ### User utilities
    def get_data_channels(self,channels=[]):
        """Get all channels or the ones specified"""
        previous_trigger_state = self.get_previous_trigger_state()
        self.stop()
        self.is_stopped()
        if channels == []: channels = list(range(1,self.nb_channels+1))
        for i in channels():
            if not(getattr(self,f'channel{i}').is_active()): continue
            else:
                pass
                # WARNING Do we warn the user he is stupid?
            data = getattr(self,f'channel{i}').get_data()
        self.set_previous_trigger_state(previous_trigger_state)
        #return pandas.DataFrame
        
    def save_data_channels(self,channels=[]):
        if channels == []: channels = list(range(1,self.nb_channels+1))
        for i in self.active_channels():
            getattr(self,f'channel{i}').save_data()
        
    ### Trigger functions
    def single(self):
        pass
    def stop(self):
        pass
    def is_stopped(self):
        while self.query('TRMD?') != 'TRMD STOP':    # typical example
            time.sleep(0.05)
        return True
    def get_previous_trigger_state(self):
        return str(previous_trigger_state)
        
    def set_previous_trigger_state(self):
        pass
        
    ### Cross-channel settings 
    def set_encoding(self):
        return str
    def get_encoding(self):
        return str
    

class Channel():
    def __init__(self,dev,slot):
        self.slot = slot
        self.dev  = dev
        self.autoscale = False
    
    
        
    def get_data(self):
    
        #if self.option is True :
            #min= self
            #max =...
            
        #data = 
        
        return bytes
        
        
    def get_log_data(self):
        return str
    def save_data(self):
        pass
    def get_data_numerical(self):
        return array_of_float
    def save_data_numerical(self):
        return array_of_float
    
    # additionnal functions
    def get_min(self):
        return float
    def get_max(self):
        return float
    def get_mean(self):
        return float
       
    
    def set_autoscale_enabled(bool):
        #self.autoscale = 
        pass
    def is_autoscable_enabled():
        return bool
    def do_autoscale():
        pass
       
    def is_active():
        pass



if __name__ == '__main__':
    from optparse import OptionParser
    import inspect
    
    usage = """usage: %prog [options] arg

               EXAMPLES:
                   

               """
    parser = OptionParser(usage)
    parser.add_option("-c", "--command", type="str", dest="com", default=None, help="Set the command to use." )
    parser.add_option("-q", "--query", type="str", dest="que", default=None, help="Set the query to use." )
    parser.add_option("-i", "--address", type="string", dest="address", default='192.168.0.4', help="Set ip address." )
    parser.add_option("-l", "--link", type="string", dest="link", default='VXI11', help="Set the connection type." )
    (options, args) = parser.parse_args()
    
    ### Compute channels to acquire ###
    #if (len(args) == 0) and (options.com is None) and (options.que is None):
        #print('\nYou must provide at least one channel\n')
        #sys.exit()
    #elif len(args) == 1:
        #chan = []
        #temp_chan = args[0].split(',')                  # Is there a coma?
        #for i in range(len(temp_chan)):
            #chan.append('C' + temp_chan[i])
    #else:
        #chan = []
        #for i in range(len(args)):
            #chan.append('C' + str(args[i]))
    #print('Channel(s):   ', chan)
    ####################################
    
    ### Start the talker ###
    classes = [name for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass) if obj.__module__ is __name__]
    assert 'Device_'+options.link in classes , "Not in " + str([a for a in classes if a.startwith('Device_')])
    Device_LINK = getattr(sys.modules[__name__],'Device_'+options.link)
    I = Device_LINK(address=options.address)
    
