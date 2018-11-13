# -*- coding: cp1251 -*-
#  plot Messenger data     отметить регионы SW  вход выход из магнитосферы
import matplotlib
from matplotlib.pylab import *
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from matplotlib import gridspec
import os
import numpy as N
import time
from ff_utils3 import *
import winsound
rcParams['figure.figsize'] = 16, 7
t=0; d=0

#----------------------------------------------
def press(event):
    global t,d,exi,plmi
#mark messenger
    try:
        ni=t.searchsorted(event.xdata)
        print(mjd2str(t[ni]))
        if event.key=='i'   :    # mark In
          d[ni,6]=16
          updateff1(0,ni+n1,d[ni])
          winsound.Beep(4000, 100)
        if event.key=='o'   :    # mark Out
          d[ni,6]=-16
          updateff1(0,ni+n1,d[ni])
          winsound.Beep(4000, 100)
        if event.key=='w'   :    # mark in Sw
          d[ni,6]=8
          updateff1(0,ni+n1,d[ni])
          winsound.Beep(4000, 100)
    except:
        pass
#    print(event.key)
    if event.key=='q':
        exi=True
        matplotlib.pyplot.close("all")
    if event.key=='+' or event.key=='=':
        plmi=3600
        matplotlib.pyplot.close("all")
    if event.key=='-':
        plmi=-3600
        matplotlib.pyplot.close("all")
    if event.key=='n':
        plmi=3600*12
        matplotlib.pyplot.close("all")
    if event.key=='_':
        print(mjd2str(d[ni],d[ni,6]))
    if event.key=='e'   :    # Erase
          d[ni,6]=0
          updateff1(0,ni+n1,d[ni])
          winsound.Beep(4000, 100)
#    if event.key==' ':
#          figtext(0.80,0.05,mjd2str(t[ni]))    #event.xdata),color='r')
#          show()

def pw(n1,n2,titl):
    global t,d,exi,plmi
    def time_axes(text,tm,top=False):
      t1=tm[0];t2=tm[-1]; dt=t2-t1
      dt1=ceil(24*dt/8)/24.
      lp0=dt1*int(t1/dt1)
      lp=arange(lp0,t2,dt1)
      lt=[]
      for t in lp:
          tt=mjd2dt(t+0.000001)
          lt.append('%02d'%tt[3]+':'+'%02d'%tt[4])
      s1=mjd2str(t1)
      s2=mjd2str(t2)
      gca().set_xlim(tm[0],tm[-1])
      gca().xaxis.set_minor_locator(MultipleLocator(10.0/1440))
      xticks(lp,lt)
      if top: gca().xaxis.set_ticks_position('top')
      if text=='':   xlabel(s1[:10]+' - '+s2[:10],)
      if len(text)>2: xlabel(text)
#=========================================================
    font = {'family': 'Verdana','weight': 'normal'}
    rc('font', **font)
    rcParams['font.size']=12.0  #?

    tm=N.zeros((1440,3))
    dm=N.zeros((1440,3,3))
    vmin=N.zeros((3,3))
    vmax=N.zeros((3,3))
    toRm=1/2439.700
    plmi=0
    ct=time.gmtime(time.time()-30*86400)
    k=0
    t,d,vmin,vmax=readffa(0,n1,n2)
    rmin=toRm*min(vmin[0:3]);rmax=toRm*max(vmax[0:3])
    vd=vmax-vmin
    v0=0.5*(vmax+vmin)
    scl=0.55*N.max(vd)
    gs = gridspec.GridSpec(3, 1, hspace=0,height_ratios=[1,2, 1])
    gcf().canvas.mpl_connect('key_press_event', press)
 #   fig, ax = plt.subplots()




#   subplot(3,1,1)
#    tight_layout(pad=0.3, w_pad=0.001, h_pad=0.001)
#    plt.subplots_adjust(wspace=0, hspace=0)
    ax0 = plt.subplot(gs[0])

    plot(t,toRm*d[:,0],'r',t,toRm*d[:,1],'b',t,toRm*d[:,2],'g')
    plot([t[0],t[-1]],[0,0],'k:')
    axis([t[0],t[-1],rmin,rmax],'tight')
    time_axes(titl,t,True)
    ylabel('Dist, Rm')

#    subplot(3,1,2)
    ax1 = plt.subplot(gs[1],sharex=ax0)
    rmin=min(vmin[3:6]);rmax=max(vmax[3:6])
    vd=vmax-vmin
    v0=0.5*(vmax+vmin)
    scl=0.55*N.max(vd)
    plot(t,d[:,0],'r',t,d[:,1],'b',t,d[:,2],'g',t,d[:,3], linewidth=1.0)
    plot([t[0],t[-1]],[0,0],'k:')
    gca().axes.get_xaxis().set_visible(False)
    axis([t[0],t[-1],rmin,rmax],'tight')

    ylabel('B, nT')
    figtext(0.80,0.65,'X',color='r')
    figtext(0.825,0.65,'Y',color='b')
    figtext(0.85,0.65,'Z',color='g')
#    subplot(3,1,3)
    ax2 = plt.subplot(gs[2],sharex=ax1)

    plot(t,d[:,1],'r',t,d[:,2],'k')
    axis([t[0],t[-1],-10,vmax[2]],'tight')
    time_axes(titl,t)
    ylabel('Sig, nT')


# savefig не работает под отладчиком
#    savefig(titl[:-3]+'pdf')
#    print ('All done')
    show()
#----------------------------------------------------
if __name__ == "__main__":
    namein='c:\\Users\\Evgeny\\YandexDisk\\!ИЗМИРАН\\Сентябрьские магнитограммы\\BEY_20180900_60pp.ffd'
#    'D:\CWORKS\MGU\Mercury\messenger__mbf_201104_01_hf51_s.ffh'
    ires=openrff(0,namein,True)
    exi=False
    n1=0*3600; n2=(0+4)*3600  #3600*2; n2=3600*4.5
    for i in range(300):
         if exi:
            quit()
         titl=''
         pw(n1,n2,titl)
         if plmi==0:
            n1=n1+86400//2; n2=n2+86400//2
         else:
            print(plmi)
            n1=n1+plmi; n2=n2+plmi
