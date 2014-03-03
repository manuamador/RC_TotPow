# -*- coding: utf-8 -*-
"""
Reverberation quality factor measurement
 
"""
from __future__ import division
import time
import os
from numpy import *
import visa
from pylab import *

from Stirrer import *
import SignalGenerator 
import Spectrum

test_name = raw_input('Enter the name of the calibration?')   
if os.path.isdir('Calibration_'+test_name)==False:            #verify if the folder exists
   os.mkdir('Calibration_'+test_name)						#create the folder
    
os.chdir('Calibration_'+test_name)


###############################################
##########   Testing parameters  ##############
###############################################

fstart=2.5e9      #start frequency
fstop=2.7e9       #stop frequency
fcenter=0.5*(fstart+fstop)   #center frequency        
fspan=fstop-fstart   #Span
RBW=1e6      #RBW size in Hz
VBW=100e3       #VBW size in Hz
SwpPt=101       #number of points
f=linspace(fstart,fstop,SwpPt) #frequency points


#Stirrer######################################  
N=30 # Number of Stirrer positions
Angles=linspace(360/N,360,N) #liste des positions en degré

#Signal_generator#######################################
P0=-10 #output power in dBm
CableLoss=-0.95
P_gene=P0-CableLoss

print '__________________________\nInstruments initializations\n'
print '\nSpectrum analyzer:'
Spectre=Spectrum.FSV30()
Spectre.reset()
Spectre.RBW(RBW)
Spectre.SweepPoint(SwpPt)    
Spectre.UnitDBM()            
Spectre.SPAN(fspan)
Spectre.centerFreq(fcenter)


print '\nSignalGenerator:'
gene=SignalGenerator.RS_SMF100A()
gene.reset()
gene.off() #RF OFF
gene.setPower(P_gene)
gene.setFreq(fstart)

print '\nStirrer:'
Stirrer=Stirrer('/com2',1)
print 'Moving to 0 deg'
Stirrer.reset()


####################################################
################# Measurement ######################
####################################################
Pin=zeros((len(Angles),len(f))) #Injected power matrix
Pmeas=zeros((len(Angles),len(f))) #Measured power matrix
Measurement=zeros((1,4))
for i in range(0,len(Angles)): 
    Stirrer.setPosition(int(Angles[i]))
    #print'Stabilization'
    time.sleep(5)
    gene.on()
    for j in range(0,len(f)):
        Spectre.centerFreq(fcenter)
        gene.setFreq(f[j])
        gene.setPower(P0-CableLoss)
        time.sleep(0.02)
        Level = Spectre.getTrace(SwpPt)
        max(Level)           
        Pin[i,j]=P0
        Pmeas[i,j]=max(Level) 
        Measurement=vstack((Measurement,array([Angles[i],f[j],Pin[i,j],Pmeas[i,j]])))
        print 'N = %3d/%3d, f = %2.2f MHz, Pin = %2.2f dBm, Pmeas= %2.2f dBm' %(i+1,N,f[j]/1e6,P0,Pmeas[i,j])
    gene.off()

V=54.5 #chamber volume in cubic meters
PmeasMoy=(10**(Pmeas/10)/1000).mean(axis=0)
Q=V*16*pi**2/(3e8/f)**3*PmeasMoy/(10**(P0/10)/1000 ) 
Q=transpose(array([f,Q]))
savetxt('Qcal.txt',Q)
savetxt('../Qcal.txt',Q)

savez('Q_cal.npz',f=f,Pmeas=Pmeas)
fname ='Synthesis_Cal_'+ test_name +'.txt'  
#File structure:
#Angle [°]|frequency [Hz]|Pin[dBm]|Pmeas [dBm]
savetxt(fname,Measurement[1:,:])
