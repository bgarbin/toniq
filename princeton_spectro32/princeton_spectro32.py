#!/usr/bin/env python3

import pvcam_Manis
import visa
from optparse import OptionParser
import sys
import subprocess
import time
from numpy import fromstring,int8,int16,float64,sign,savetxt

CAMERA  = 'Camera1'
ADDRESS = 'ASRL6::INSTR'

class Device():
    def __init__(self,camera=CAMERA):
        self.pvcam = pvcam_Manis.Init_PVCam()
        
		### Initiate communication with the requested camera ###
        print('Trying to get: %s' %camera)
        self.CAM = self.get_camera(camera=camera)


    def get_data(self, nb_frames=1, exposure=None, region=None, binning=None):
        data = self.CAM.acq(frames=nb_frames, exposure=exposure, region=region, binning=binning)
        self.data = [list(data[i].squeeze()) for i in xrange(len(data))]
        #return data2

    def save_data(self,filename,camera=CAMERA,FORCE=False):
        # Verify file doesn't already exist
        temp_filename = filename + '_spectro32' + camera + '.txt'
        #temp = subprocess.getoutput('ls').splitlines()
        #for i in range(len(temp)):
         #   if temp[i] == temp_filename and not(FORCE):
         #       print('\nFile ', temp_filename, ' already exists, use -F option, change filename or remove old file\n')
         #       sys.exit()
        self.lambd=[list(range(len(self.data[0])))]
        assert self.lambd, 'You may want to get_data before saving ...'
        [self.lambd.append(self.data[i]) for i in xrange(len(self.data))]
        f = savetxt(temp_filename,self.lambd)  ## squeeze
        print(camera + ' saved')

    def get_camera(self,camera='Camera1'):
        CAM = self.pvcam.PVCam.getCamera(camera)
        print('Got: %s' %camera)
        return CAM

    def list_cameras(self):
        return self.pvcam.listCameras()
    
    def close(self):
        pass


if __name__=='__main__':

    usage = """usage: %prog [options] arg

               EXAMPLES:
                  
               

               """
    parser = OptionParser(usage)
    parser.add_option("-c", "--command", type="str", dest="com", default=None, help="Set the command to use." )
    parser.add_option("-q", "--query", type="str", dest="que", default=None, help="Set the query to use." )
    parser.add_option("-i", "--camera", type="string", dest="camera", default=CAMERA, help="Set camera to get" )
    parser.add_option("-n", "--nb_frames", type="int", dest="nb_frames", default=1, help="Set the number of frames" )
    parser.add_option("-e", "--exposure", type="float", dest="exposure", default=0.01, help="Set the time of exposure" )
    parser.add_option("-o", "--filename", type="string", dest="filename", default=None, help="Set the name of the output file" )
    parser.add_option("-F", "--force",action = "store_true", dest="force", default=False, help="Allows overwriting file" )
    (options, args) = parser.parse_args()
    
    ### Start the talker ###
    I = Device(camera=options.camera)
    
    if options.query:
        print('\nAnswer to query:',options.query)
        rep = I.query(options.query)
        print(rep,'\n')
    elif options.command:
        print('\nExecuting command',options.command)
        I.scope.write(options.command)
        print('\n')
    
    
    I.data = I.get_data(nb_frames=options.nb_frames,exposure=options.exposure)
    I.save_data(filename=options.filename,camera=options.camera,FORCE=options.FORCE)
    
    I.close()
    sys.exit()
