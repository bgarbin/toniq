#!/usr/bin/env python3

"""
Supported instruments (identified):
- 
"""

import sys,os
import time
from numpy import fromstring,int8,int16,float64,sign
import pandas

class Device():
    def __init__(self,nb_channel=4):
        #WARNING how to select channels to instantiate
              
        self.nbchaannel = nbprt              
        self.channel1 = Channel(self,1)
        self.slot2 = Channel(self,2)
        self.slot3 = Channel(self,3)
        self.slot4 = Channel(self,4)

    
    ### user utilities
    def get_all_channels(self,channels=[]}):
        """Get mentionned channels or all"""
        previous_trigger_state = self.get_previous_trigger_state()
        if trigger: self.single               #WARNING  stop forced
        self.has_scope_triggered()
        for i in self.active_channels()       #WARNING
            data = getattr(self,f'{channel_{i}').getData() et isactive
            #eval('rep = self.slot%d.get_data()' %i)
        self.set_previous_trigger_state(previous_trigger_state)
        return pandas
        
    def save_all_channels(self):
        for i in self.active_channels()
            eval('self.slot%d.save_data()' %i)
        
    ### trigger functions
    def single(self):
        self.write
        
    def stop(self true):
    
    def isstop(self)
        
    def get_previous_trigger_state(self):
        return str(previous_trigger_state)
        
    def set_previous_trigger_state(self):
        
    def has_scope_triggered(self):
        return bool
        
    ### possible cross-channel settings 
    def set_encoding(self):
        return str
    def get_encoding(self):
        return str
    

class Channel():
    def __init__(self,dev,slot):
        self.slot = slot
        self.dev  = dev
    
    
    def get_data(self):
        return bytes
    def get_log_data(self):
        return str
    def save_data(self):
        
    def get_data_numerical(self):
        return array_of_float
    def save_data_numerical(self):
        return array_of_float
    
    def get_min(self):
        return float
    def get_max(self):
        return float
    def get_mean(self):
        return float
        
    def auto_scale_get_data()
    
    def isActive()


#################################################################################
############################## Connections classes ##############################
class Device_TCPIP():
    def __init__(self, address = ,  **kwargs):
        import visa as v
        
        Device.__init__(self, **kwargs)
        self.scope = ...(address)


    def query(self,command):
        return self.scope.query(command)

    def read(self):
        return self.scope.read()

    def write(self,command):
        self.scope.write(commande,length=self.length)


class Device_VX11(): en haut
    def __init__(self, address =  , **kwargs):
        import vxi11 as v
    
        Device.__init__(self, **kwargs)
        self.scope = ...(address)


    def query(self,command):
        return self.scope.query(command)

    def read(self):
        return self.scope.read()

    def write(self,command):
        self.scope.write(commande,length=self.length)
############################## Connections classes ##############################
#################################################################################

        
        
if __name__ == '__main__':
    from optparse import OptionParser
    
    usage = """usage: %prog [options] arg

               EXAMPLES:
                   

               """
    parser = OptionParser(usage)
    parser.add_option("-c", "--command", type="str", dest="com", default=None, help="Set the command to use." )
    parser.add_option("-q", "--query", type="str", dest="que", default=None, help="Set the query to use." )
    parser.add_option("-i", "--address", type="string", dest="address", default='169.254.166.206', help="Set ip address" )
    (options, args) = parser.parse_args()
    
    ### Compute channels to acquire ###
    if (len(args) == 0) and (options.com is None) and (options.que is None):
        print('\nYou must provide at least one channel\n')
        sys.exit()
    elif len(args) == 1:
        chan = []
        temp_chan = args[0].split(',')                  # Is there a coma?
        for i in range(len(temp_chan)):
            chan.append('C' + temp_chan[i])
    else:
        chan = []
        for i in range(len(args)):
            chan.append('C' + str(args[i]))
    print('Channel(s):   ', chan)
    ####################################
    ### Compute channels for spe_mode to acquire ###
    if options.spe_mode:
        if len(options.spe_mode) > 1:
            spe_mode       = eval(options.spe_mode)[0]
            spe_mode_chans = eval(options.spe_mode)[1:]
            chan_spe = []
            for i in range(len(spe_mode_chans)):
                chan_spe.append('C'+str(spe_mode_chans[i]))
            print('Special mode Channel(s):   ', chan_spe)
        else:
            chan_spe = chan
            spe_mode = eval(options.spe_mode)
            print('Special mode Channel(s):   ', chan_spe)
    else:
        chan_spe = None
        spe_mode = options.spe_mode
    ####################################
    
    ### Start the talker ###
    Device()
