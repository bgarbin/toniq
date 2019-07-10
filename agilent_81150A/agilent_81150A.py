#!/usr/bin/env python3

import visa as v
from optparse import OptionParser
import sys
import time
from numpy import zeros,ones,linspace

IP = '169.254.119.244'

class Device():
    def __init__(self,host=IP):
        # Instantiation
        rm = v.ResourceManager('@py')
        self.inst = rm.get_instrument('TCPIP::'+host+'::INSTR')
    
    def amplitude(self,amplitude,chan):
        self.inst.write(':VOLT'+chan+' '+amplitude)
    def offset(self,offset,chan):
        self.inst.write(':VOLT'+chan+':OFFS '+offset)
    def frequency(self,frequency,chan):
        self.inst.write(':FREQ'+chan+' '+frequency)
    
    def query(self,query):
        self.write(query)
        return self.read()
    def write(self,query):
        self.inst.write(query)
    def read(self):
        rep = self.inst.read()
        return rep
    def exit(self):
        self.inst.close()
        sys.exit()
    def idn(self):
        self.inst.write('*IDN?')
        self.read()
        
            
if __name__ == '__main__':

    usage = """usage: %prog [options] arg
               
               
               EXAMPLES:
                   set_agilent_81150A -a 1 -o 1 -f 50KHZ 1,2
				   set the frequency to 50 kHz, the amplitude to 1V, the offset to 1V for both channel 1 and 2


               """
    parser = OptionParser(usage)
    parser.add_option("-c", "--command", type="str", dest="command", default=None, help="Set the command to use." )
    parser.add_option("-q", "--query", type="str", dest="query", default=None, help="Set the query to use." )
    parser.add_option("-o", "--offset", type="str", dest="offset", default=None, help="Set the offset value." )
    parser.add_option("-a", "--amplitude", type="str", dest="amplitude", default=None, help="Set the amplitude." )
    parser.add_option("-f", "--frequency", type="str", dest="frequence", default=None, help="Set the frequency; may be 50000 or 50KHZ" )
    parser.add_option("-i", "--ip_address", type="str", dest="ip_address", default=IP, help="Set the Ip address to use for communicate." )
    (options, args) = parser.parse_args()
    
    ### Compute channels to act on ###
    if (len(args) == 0) and (options.command is None) and (options.query is None):
        print('\nYou must provide at least one channel\n')
        sys.exit()
    elif (options.command is not None) or (options.query is not None):
        pass
    else:
        chan = args[0].split(',')
        print(chan)

    ### Start the talker ###
    I = Device(host=options.ip_address)
    if options.query:
        print('\nAnswer to query:',options.query)
        rep = I.query(options.query)
        print(rep,'\n')
        I.exit()
    elif options.command:
        print('\nExecuting command',options.command)
        I.write(options.command)
        print('\n')
        I.exit()
    
    if options.amplitude:
        I.amplitude(options.amplitude)
    if options.offset:
        I.offset(options.offset)
    if options.frequency:
        I.frequency(options.frequency)
    
    I.exit()