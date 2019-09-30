#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Supported instruments (identified):
- Wavemaster 8620A
- Waverunner 104Xi
- Waverunner 6050A
"""

#WARNING Remains: WARNINGs here and there, autoscale, encoding, bash handler


import sys,os
import time
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
        self.write(command)
        return self.read()
    def read(self):
        return self.inst.read()
    def read_raw(self):
        return self.inst.read_raw()
    def write(self,command):
        self.inst.write(command)
    def close(self):
        self.inst.close()

class Device_VXI11():
    def __init__(self, address, **kwargs):
        import vxi11 as v
    
        Device.__init__(self, **kwargs)
        self.inst = v.Instrument(address)

    def query(self, command, nbytes=100000000):
        self.write(command)
        return self.read(nbytes)
    def read(self,nbytes=100000000):
        self.inst.read(nbytes)
    def write(self,cmd):
        self.inst.write(cmd)
    def close(self):
        self.inst.close()
############################## Connections classes ##############################
#################################################################################


class Device():
    def __init__(self,nb_channels=4):
        
        self.nb_channels = nb_channels
        self.encoding    = 'BYTE'
        
        self.scope.write('CFMT DEF9,'+encoding+',BIN')
        self.scope.write('CHDR SHORT')
        
        for i in range(1,self.nb_channels+1):
            setattr(self,f'channel{i}',Channel(self,i))
    
    
    ### User utilities
    def get_data_channels(self,channels=[]):
        """Get all channels or the ones specified"""
        previous_trigger_state = self.get_previous_trigger_state()    #1 WARNING previous trigger state in memory or returned
        self.stop()
        self.is_stopped()
        if channels == []: channels = list(range(1,self.nb_channels+1))
        for i in channels():
            if not(getattr(self,f'channel{i}').is_active()): continue
            else:
                pass
                # WARNING Do we warn the user he is stupid?
            data = getattr(self,f'channel{i}').get_data()
            log_data = getattr(self,f'channel{i}').get_log_data()
        self.set_previous_trigger_state(previous_trigger_state)
        #return pandas.DataFrame
        
    def save_data_channels(self,channels=[]):
        if channels == []: channels = list(range(1,self.nb_channels+1))
        for i in self.active_channels():
            getattr(self,f'channel{i}').save_data()
            getattr(self,f'channel{i}').save_log_data()
        
    ### Trigger functions
    def single(self):
        self.inst.write("TRMD SINGLE")
    def stop(self):
        self.inst.write("TRMD STOP")
    def is_stopped(self):
        while self.query('TRMD?') != 'TRMD STOP':
            time.sleep(0.05)
        return True
    def get_previous_trigger_state(self):
        return self.query('TRMD?')
        
    def set_previous_trigger_state(self):                 # go to 1 WARNING
        self.scope.write(self.prev_trigg_mode)
        
    ### Cross-channel settings 
    def set_encoding(self,encoding):
        self.encoding = encoding
        self.scope.write('CFMT DEF9,'+self.encoding+',BIN')
        if encoding=='BYTE':dtype=int8;NUM=256;LIM=217.          # 15% less than the maximal number possible
        elif encoding=='WORD':dtype=int16;NUM=65536;LIM=55700.   # 15% less than the maximal number possible
    def get_encoding(self):
        return self.encoding
    

class Channel():
    def __init__(self,dev,channel):
        self.channel          = int(channel)
        self.dev              = dev
        self.autoscale_iter   = 0
        self.autoscale_factor = 8
    
    
    def get_data(self):
        if self.autoscale_iter:
            self.do_autoscale()
            
        self.inst.write(f'C{self.channel}:WF? DAT1')
        data = self.read_raw()
        return data[data.find(b'#')+11:-1]
    def get_log_data(self):
        rep = self.query(f"C{self.channel}:INSP? 'WAVEDESC'")
        return rep
    
    def save_data(self,filename):
        temp_filename = f'{filename}_lecroyC{self.channel}'
        temp = os.listdir()                         # if file exist => exit
        for i in range(len(temp)):
            if temp[i] == temp_filename and not(FORCE):
                print('\nFile ', temp_filename, ' already exists, change filename or remove old file\n')
                return
        
        f = open(temp_filename,'wb')# Save data
        f.write(self.data)
        f.close()
    def save_log_data(self,filename):
        temp_filename = f'{filename}_lecroyC{self.channel}'
        f = open(temp_filename + '.log','w')
        f.write(self.preamb)
        f.close()
    
    def get_data_numerical(self):
        return array_of_float
    def save_data_numerical(self):
        return array_of_float
    
    # additionnal functions
    def get_min(self):
        stri  = self.query(f'C{self.channel}:PAVA? MIN,MAX')
        temp2 = 'MIN,'
        temp3 = stri.find(temp2)
        temp4 = stri.find(f' V')
        return float(stri[temp3+len(temp2):temp4])
    def get_max(self):
        stri  = self.query(f'C{self.channel}:PAVA? MIN,MAX')
        stri  = stri[stri.find(f' V')+len(f' V'):]
        temp2 = 'MAX,'
        temp3 = stri.find(temp2)
        temp4 = stri.find(f' V')
        return float(stri[temp3+len(temp2):temp4])
        
    def get_mean(self):                      # WARNING to test
        return float(self.query(f'C{self.channel}:PAVA? MEAN'))
        
    def set_vertical_offset(self,val):
        self.scope.write(f'C{self.channel}:OFST {val}') 
    def get_vertical_offset(self,val):
        return self.scope.write(f'C{self.channel}:OFST?').split(' ')[1]
    def set_vertical_amplitude(self,val):
        self.scope.write(f'C{self.channel}:VDIV {val}') 
    def get_vertical_amplitude(self,val):
        return self.scope.write(f'C{self.channel}:VDIV?').split(' ')[1])
        
    def do_autoscale():
        k = 1
        while k <= self.autoscale_iter()
            mi = self.get_min()
            ma = self.get_max()
            diff = abs(mi) + abs(ma)
            
            val = round((-1)*diff/2. + abs(mi),3)
            self.set_vertical_offset(val)
            new_channel_amp  = round(diff/self.autoscale_factor,3)
            if new_channel_amp<0.005: new_channel_amp = 0.005 # if lower than the lowest possible 5mV/div
            self.set_vertical_offset(new_channel_amp)
            
            self.single()
            print('Optimisation loop index:', k,self.autoscale_iter)
            if k==self.autoscale_iter:
                VDIV = self.get_vertical_amplitude()
                OFST = self.get_vertical_offset()
                R_MI = -(4.5 * VDIV) - OFST
                R_MA =   4.5 * VDIV  - OFST
                mi = self.get_min()
                ma = self.get_max()
                if mi<R_MI or ma>R_MA:                        #if trace out of the screen optimize again
                    print('(SCOPE)   Min:',R_MI,' Max:',R_MA)
                    print('(TRACE)   Min:',mi,' Max:',ma)
                    k = k-1
            k = k+1
            
    def set_autoscale_iter(self,val):
        self.autoscale_iter = val
    def get_autoscale_iter(self):
        return self.autoscale_iter
    def set_autoscale_factor(self,val):
        self.autoscale_factor = val
    def get_autoscale_factor(self):
        return self.autoscale_factor
           
    def is_active():
        temp = self.query(f'C{self.channel}:TRA?')
        if temp.find('ON') == -1:
            print('\nWARNING:  Channel',channel[i], 'is not active  ===>  exiting....\n')
            sys.exit()
        # WARNING see what the scope return to return bool here


if __name__ == '__main__':
    from optparse import OptionParser
    import inspect
    
    usage = """usage: %prog [options] arg

               EXAMPLES:
                   get_lecroywavemaster 1 -o filename
                   Record the first channel and create two files name filename_lecroy and filename_lecroy.log
            
                   get_lecroywavemaster -i 192.168.0.4 -e WORD -o test 3
                   Same as before but record channel 3 with giving an IP address and an int16 data type
                    
                   get_lecroywavemaster -i 192.168.0.5 -F -t -m [10,1,2] -n 8 -o test 1,2
                   Uses autoscale for automatic adjustments of the vertical scale on channel 1 and 2
                   Note: if channel is not to be acquired it won't be subjected to amplitude optimization
                    
               
               IMPORTANT INFORMATIONS:
                    - Datas are obtained in a binary format: int8 
                    - To retrieve datas (in "VERTUNIT"), see corresponding log file:
                    DATA(VERTUNIT) = DATA(ACQUIRED) * VERTICAL_GAIN - VERTICAL_OFFSET
                    
                See for more informations:  toniq/Prog_guide/Lecroy.pdf

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
    
    if query:
        print('\nAnswer to query:',query)
        rep = self.query(query)
        print(rep,'\n')
        sys.exit()
    elif command:
        print('\nExecuting command',command)
        self.scope.write(command)
        print('\n')
        sys.exit()
