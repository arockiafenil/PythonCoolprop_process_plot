# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:38:34 2022

@author: ICER
"""
#%%
import CoolProp.CoolProp as CP
import os
import math
import enum
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from IPython import get_ipython
import numpy as np
from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots.SimpleCycles import StateContainer
from CoolProp import AbstractState
CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, "C:\Program Files (x86)\REFPROP")
N=int(input('Enter no of Temp. points in temp:'))
# fluid=input('Enter the working fluid (Water/CO2):')
rp0,rpn=input('Enter the range of pressure ratios (initial,end):').split()
rp0=int(rp0)
rpn=int(rpn)
rp=range(rp0,rpn+1,1)
Pin = float(input('Enter Compressor/Pump Inlet Pressure, (bar)= '))*100000
print(rp0,rpn)
Tsat=(PropsSI('T','P',Pin,'Q',0,'CO2')-273.15)
state=CP.AbstractState('REFPROP','CO2')
Tmlt=(state.melting_line(CP.iT, CP.iP, Pin))-273.15
Tmlt=float(math.ceil(Tmlt))
Tsat=float(math.floor(Tsat))
dT=(abs(Tsat-Tmlt))/N
T=list(np.linspace(Tmlt,Tsat,num=N))

#%%
# Pout=[[0 for x in range(len(T))] for y in range(len(rp))]
Pout=[0]*len(rp)
Sin=[0]*len(T)
Hin=[0]*len(T)
rho1=[0]*len(T)
Hout= [[0 for i in range(len(Pout))] for j in range(len(Sin))]
rho2= [[0 for i in range(len(Pout))] for j in range(len(Sin))]
WD=[[0 for i in range(len(Pout))] for j in range(len(Sin))]
Dr=[[0 for i in range(len(Pout))] for j in range(len(Sin))]
    
    
for t in range(len(T)):
    Sin[t]=(PropsSI('S','P',Pin,'T',T[t]+273.15,'CO2'))
    Hin[t]=(PropsSI('H','P',Pin,'T',T[t]+273.15,'CO2'))
    rho1[t]=(PropsSI('D','P',Pin,'T',T[t]+273.15,'CO2'))
    
# for s in range(len(Sin)):
#     for p in range(len(Pout)):
#         Hout[s][p]=(PropsSI('H','P',Pout[p],'S',Sin[s],'CO2'))
#         rho2[s][p]=(PropsSI('D','P',Pout[p],'S',Sin[s],'CO2'))
#         WD[s][p]=Hout[s][p]-Hin[s]
#         Dr[s][p]=rho2[s][p]/rho1[s]
# rp=list(rp)        

props=['P','T','H','S']
    
print(props[0])
sp1=[0]*len(T)
for l in range(len(T)):
    sp1[l]=[0]*len(props)
    # sp1[l]=StateContainer()
    for p in range(len(props)):
        if p==0:
            sp1[l][p]=Pin
        if p==1:
            sp1[l][p]=T[l]+273.15
        else:
            sp1[l][p]=(PropsSI(props[p],'P',Pin,'T',T[l]+273.15,'CO2'))
            
            
sp2=[0]*len(T)
for l in range(len(T)):
    sp2[l]=[0]*len(rp)
    # sp2[l]=StateContainer()
    for p in range(len(rp)):
        Pout[p]=Pin*rp[p]
        sp2[l][p]=[0]*len(props)
        for t in range(len(props)):
            if t==0:
                sp2[l][p][t]=Pout[p]
            if t==4:
                sp2[l][p][t]=Sin[l]
            else:
                sp2[l][p][t]=(PropsSI(props[t],'P',Pout[p],'S',Sin[l],'CO2'))
                        
                
st=[0]*10
for l in range(len(st)):
    st[l]=[0]*5
    for s in range(len(rp)):
        st[l][s]=StateContainer()
        for p in range(len(props)):
              st[l][s][0,props[p]]=sp1[l][p]
              st[l][s][1,props[p]]=sp2[l][s][p]
#         st[s][1,props[p]]=sp2[0][s][p]    


#%%

# get_ipython().run_line_magic('matplotlib', 'qt')
# plot1=plt.figure(1)
# plot=[0]*len()
from CoolProp.Plots import IsoLine
from CoolProp.Plots import Plots
plot= PropertyPlot('CO2', 'PH', unit_system='EUR',tp_limits='NONE')
# plot.props[CP.iQ]['lw'] = '0.5'
plot.props[CP.iQ]['color'] = 'green'
plot.props[CP.iT]['lw'] = '1'
plot.calc_isolines(CP.iQ,iso_range=[0,1], num=5,points=100)

# plot.props[CP.iP]['lw'] = '1.5'
plot.calc_isolines(CP.iT,iso_range=[-100,500], num=80, points=50)
plot.calc_isolines(CP.iSmass,iso_range=[0.5,4], num=80, points=50)
plot.set_axis_limits([0, 500, 0, 500])
# Ts=plot.generate_ranges(CP.iT,-100, 500, num=100)
# Ss=plot.generate_ranges(CP.iSmass,0.5,4, num=100)

plot.draw_isolines()
# xy=plot.get_x_y_dydx(Ts,Ss,Ts)
# plt.plot(Pin,Hin[0],'o-')
# plot.draw()
lnstyl=['b','g','r','c','k','-','--','-.','-',':']
n = len(st)
colors = pl.cm.jet(np.linspace(0.1,2,n))
font1 = {'family':'serif','color':'blue','size':20}
tit=(Pin/1e+05)
plt.title('PH Plot(Inlet Pressure=%i bar)' %tit, fontdict = font1)
rp=[*rp]
label=[0]*len(rp)
for i in range(len(rp)):
    label[i]='P\u2080\u2082/P\u2080\u2081='+str(rp[i])
for l in range(len(st)):
    for i in range(len(st[l])):
        if l>8:
            plot.draw_process(st[l][i],line_opts={'color':colors[i], 'lw':2, 'ls':'--','label':label[i]})
              
        else:
            plot.draw_process(st[l][i],line_opts={'color':colors[i], 'lw':2, 'ls':'--'})
            
# plt.annotate('S',xy=(100,100)) 
for t in range(len(T)):
    plt.annotate('Tin=%i \xb0C' %T[t],xy=(sp1[t][2]/1000,sp1[t][0]/1e+05),xytext=((sp1[t][2]/1000)+2.5,((sp1[t][0])/1e+05)-8),size=5.5,arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.05"))            
    
plt.rcParams.update({'font.size': 16})
plt.legend()        
