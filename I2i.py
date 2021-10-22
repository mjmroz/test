#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:33:54 2020

@author: mateusz
"""

import numpy as np 
from matplotlib import rcParams; rcParams["figure.dpi"] = 1500
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
def conv(x,a,b):
    I,V=x[:,0],x[:,1]
    return ( I + a * (V-I) + b)


def conv_l(x,a,b):
    return x * a +b


SDSS='SDSS_Stetson.list'
data=pd.read_csv(SDSS,header=0,index_col=False,sep='\t')
idx=np.where((data['good_i']==1) & (data['I']!=0) & ( data['V']!=0))    
    

x=np.column_stack((data.loc[idx]['I'],data.loc[idx]['V']))
y=np.array(data.loc[idx]['psfMag_i'])



popt, pcov=curve_fit(conv,x,y)

popt_l,pcov_l=curve_fit(conv_l,data.loc[idx]['I'],data.loc[idx]['psfMag_i'])

plt.scatter(data.loc[idx]['I'],data.loc[idx]['psfMag_i'],s=0.1,label='$i_{observed}$')
plt.scatter(x[:,0], conv(x, *popt),s=0.1,label='i(I,V)')
plt.xlim([21.5,12.5 ])
plt.ylim([23,13])
plt.xlabel('I[mag]')
plt.ylabel('i[mag]')
plt.legend()
plt.savefig('itoI.png')
plt.show()



plt.scatter(x[:,0],conv(x, *popt)-data.loc[idx]['psfMag_i'],s=0.1)
plt.ylim([-0.5,0.5])
plt.xlim([21.5,12.5 ])
plt.hlines([0.1,-0.1],12.5,21.5,linewidth=0.5)
plt.hlines([0],12.5,21.5,linewidth=0.5,color='r')
plt.ylabel('i - i(I,V)[mag]')
plt.xlabel('I[mag]')
plt.savefig('itoI_err.png')
plt.show()

plt.plot(data.loc[idx]['I'],conv_l(data.loc[idx]['I'],*popt_l),"r",label='linear transformation')
plt.scatter(data.loc[idx]['I'],data.loc[idx]['psfMag_i'],s=0.1,label='observed')
plt.xlim([21.5,12.5 ])

plt.show()

plt.scatter(data.loc[idx]['I'],conv_l(data.loc[idx]['I'],*popt_l)-data.loc[idx]['psfMag_i'],s=0.1)
plt.ylim([-0.5,0.5])
plt.xlim([21.5,12.5 ])
plt.hlines([0.1,-0.1],12.5,21.5,linewidth=0.5)
plt.hlines([0],12.5,21.5,linewidth=0.5,color='r')
plt.ylabel('i - i(I)[mag]')
plt.xlabel('I [mag]')
plt.savefig('itoI_err_linear.png')
plt.show()

i=91

print(data.loc[i]['I'] + popt[0] * (data.loc[i]['V'] - data.loc[i]['I'] ) + popt[1])
print(data.loc[i]['psfMag_i'])