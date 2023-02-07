# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 15:05:38 2022

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
import numpy as npy
from CoolProp.CoolProp import PhaseSI, PropsSI, get_global_param_string
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots.SimpleCycles import StateContainer
from CoolProp import AbstractState
CP.set_config_string(CP.ALTERNATIVE_REFPROP_PATH, "C:\Program Files (x86)\REFPROP")
N=int(input('Enter no of Temp. points in temp:'))
# fluid=input('Enter the working fluid (Water/CO2):')
rp0,rpn=input('Enter the range of pressure ratios (initial,end):').split()
P0,Pn,np=input('Enter the range of inlet pressures (initial,end,interval):').split()
#%%
import plotly.graph_objects as go
from plotly.subplots import make_subplots

rp0=int(rp0);rpn=int(rpn);P0=int(P0);Pn=int(Pn);np=int(np);
Pin=list(range(P0,(Pn+np),np));rp=list(range(rp0,rpn+1,1))
Tsat=[0]*len(Pin);Tmlt=[0]*len(Pin);Pout=[0]*len(Pin);dT=[0]*len(Pin);Tin=[0]*len(Pin);WD=[0]*len(Pin);PR=[0]*len(Pin)
Sin=[[0 for i in range(N+1)] for j in range(len(Pin))];Hin=[[0 for i in range(N+1)] for j in range(len(Pin))]
rho1=[[0 for i in range(N+1)] for j in range(len(Pin))];Hout=[0]*len(Pin)

for p in range(len(Pin)):
    Pin[p]=Pin[p]*100000
    Tsat[p]=(PropsSI('T','P',Pin[p],'Q',0,'CO2')-273.15)
    state=CP.AbstractState('REFPROP','CO2')
    Tmlt[p]=(state.melting_line(CP.iT, CP.iP, Pin[p]))-273.15
    Tmlt[p]=float(math.ceil(Tmlt[p]))
    Tsat[p]=float(math.floor(Tsat[p]))
    dT[p]=(abs(Tsat[p]-Tmlt[p]))/N
    Tin[p]=list(npy.arange(Tmlt[p],Tsat[p]+dT[p],dT[p]))    
    for t in range(len(Tin[p])):
        Sin[p][t]=(PropsSI('S','P',Pin[p],'T',Tin[p][t]+273.15,'CO2'))
        Hin[p][t]=(PropsSI('H','P',Pin[p],'T',Tin[p][t]+273.15,'CO2'))
        rho1[p][t]=(PropsSI('D','P',Pin[p],'T',Tin[p][t]+273.15,'CO2'))
        
        
for p in range(len(Pin)):
    Pout[p]=[0]*(N+1)
    Hout[p]=[0]*(N+1)
    WD[p]=[0]*(N+1)
    PR[p]=[0]*(N+1)
    for t in range(N+1):
        Pout[p][t]=[0]*len(rp)
        Hout[p][t]=[0]*len(rp)
        WD[p][t]=[0]*len(rp)
        PR[p][t]=[0]*len(rp)
        for r in range(len(rp)):
            Pout[p][t][r]=(Pin[p]*rp[r])
            Hout[p][t][r]=(PropsSI('H','P',Pout[p][t][r],'S',Sin[p][t]+273.15,'CO2'))
            WD[p][t][r]=Hout[p][t][r]-Hin[p][t]
            PR[p][t][r]=Pout[p][t][r]/Pin[p]

X=[0]*len(Pin);Y=[0]*len(Pin);Z=[0]*len(Pin)  
for i in range(len(Pin)):
    X[i],Y[i]=npy.meshgrid(Tin[i],PR[i][0])
    Z[i]=npy.array(WD[i])/1000
    Z[i]=Z[i].T
    tit=(Pin[i]/1e+05)
    fig = make_subplots(
    rows=2, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}],
           [{'type': 'surface'}, {'type': 'surface'}]])
    fig.add_trace(
    go.Surface(x=X[i], y=Y[i], z=Z[i], colorscale='jet', showscale=False),
    row=1, col=1)
    fig.update_traces(contours_y=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_y=True))
    fig.update_traces(contours_x=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_x=True))
    fig.update_scenes(xaxis_title_text='Inlet Temperature \xb0C',  
                  yaxis_title_text='Pressure Ratio',  
                  zaxis_title_text='Work Done (kJ/kg)')
    fig.update_layout(title='PH Plot(Inlet Pressure=%i bar)' %tit, autosize=False,
              width=1600, height=1600,
              margin=dict(l=400, r=50, b=20, t=30))
    fig.write_html("Test_%i.html"%tit)
    fig.show()
    
    # ax = plt.subplot(projection='3d')
    # from matplotlib import cm
    
    # ax.contour(X[i], Y[i], Z[i], zdir='y', offset=8, cmap=cm.jet)
    # ax.contour(X[i], Y[i], Z[i], zdir='x', offset=-56, cmap=cm.jet)
    # ax.set_xlim(-56,25)
    # ax.set_ylim(0,8)
    # # ax.set_zlim(10)
    # ax.set_xlabel('Inlet Temperature \xb0C')
    # ax.set_ylabel('Pressure Ratio')
    # ax.set_zlabel('Work Done (kJ/kg)')



            
        
            