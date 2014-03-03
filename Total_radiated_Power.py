# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:25:50 2013

@author: Administrateur
"""
from __future__ import division
import time
import os
from numpy import *
import visa
from pylab import *

from Stirrer import *
import Spectrum

Qcal=loadtxt('Qcal.txt')

test_name = raw_input('Enter the name of the EUT?')   
if os.path.isdir('Measurement_'+test_name)==False: #verify if the folder exists
   os.mkdir('Measurement_'+test_name)		   #create the folder
    
os.chdir('Measurement_'+test_name)


###############################################
##########   Testing parameters  ##############
###############################################
V=54.5  #volume of the chamber in m3
f=Qcal[:,0]
fstart=f[0] #fréquence de départ
fstop=f[-1] #dernière fréquence
#Données de coSwpPtiguration de l'analyseur de spectre####################################

#fréquences uniformément réparties
SwpPt=len(f)#nombre de fréquence

#Stirrer######################################  
N=10 # Number of stirrer positions
Angles=linspace(360/N,360,N) 
fcenter=0.5*(fstop+fstart)          
fspan=fstop-fstart    #Measurement bandwidth in Hz
RBW=1e6       #Size of the RBW filter in Hz
VBW=1e6       #Size of the VBW filter in Hz
Tmes=1     #Dwelling time in s


#Criterion_Level=-35
#peaksindex=[100,200,300]

print '__________________________\nInstruments initializations\n'
print '\nSpectrum analyzer'
Spectre=Spectrum.FSV30()
Spectre.reset()
Spectre.RBW(RBW)             
Spectre.SweepPoint(SwpPt)   
Spectre.UnitDBM()            
Spectre.SPAN(fspan)
Spectre.centerFreq(fcenter)

print '\nStirrer'
Stirrer=Stirrer('/com2',1)
print 'Moving to 0 deg'
Stirrer.reset()

####################################################
################# Measurement ######################
####################################################

Measurement=zeros((N,2))
Raw_Measurement=zeros((N,SwpPt))
for i in range(0,len(Angles)):
    Stirrer.setPosition(int(Angles[i]))
    #print'Stabilization'
    time.sleep(5)
    Spectre.readwrite()
    Spectre.MaxHold()
    time.sleep(Tmes)                   
    Level = Spectre.getTrace(SwpPt)    
    #while (min(Level[peaksindx])<Criterion_Level):
    #    Level = Spectre.getTrace(SwpPt)
    #    time.sleep(0.5)
    Level = Spectre.getTrace(SwpPt)
    MaximumLevel=max(Level)
    MaxIdx =Level.argmax()
    Maximumf=f[MaxIdx]
    Measurement[i,:]=array([Maximumf,MaximumLevel])
    Raw_Measurement[i,:]=Level
    TotalP=(V*16*pi**2/(3e8/f)**3*(10**(Raw_Measurement[0:i,:]/10)/1000).mean(axis=0)/Qcal[:,1]) 
    print 'N = %3d/%3d, f = %2.2f MHz, Pmes= %2.2f dBm, Pt= %2.2f mW/MHz' %(i+1,N,Maximumf/1e6,MaximumLevel,1000*TotalP.max())
    #savez(test_name,Angles=Angles,f=f,Measurement=Measurement,Raw_Measurement=Raw_Measurement)


#Total radiated power measurement
AverageMaxPower=(10**(Raw_Measurement/10)/1000).mean(axis=0)
      
Pt=(V*16*pi**2/(3e8/f)**3*AverageMaxPower/Qcal[:,1]) 
print 'Pt= %2.5f mW'%(Pt.max()*1000)

fnamez = test_name + '.npz'
savez(fnamez,Angles=Angles,f=f,Measurement=Measurement,Raw_Measurement=Raw_Measurement,Qcal=Qcal,Pt=Pt)
