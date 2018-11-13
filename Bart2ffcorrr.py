# -*- coding: cp1251 -*-
# с 13 декабря 206 создаёт файлы  MOS_  для замены Москва основная (Бурцева)

#       '  Преобразование  1 сек или 1 мин двоичных  файлов обс. Москва-1 во флэт'
#  в бинарном файле порядок данных DT H E Z  Temperat
#       '  mos1_2ff маска_входных [выходная_директория]'
# const baseA use to fit старым данным
# if dotc=True - do temperature correction

# example create both 1 sec and 1 min flat files
dotc=True  #dotc=True- выполнять температурную коррекцию,  =False - не выполнять

#----------------------------------------------------


import struct
import numpy as N
from ff_utils3 import *
import glob
import sys,os

t0=25     #  температура приведения
scount=0; cmin=0;td=0;ts=0
sv=N.zeros((90,3))
tv=90*[0]
phd=[0,0,0,0,0]
phd1=[0,0,0,0]
MP=[[1,0,0],[0,1,0],[0,0,1]]
eps=[]; base=[]; tk=[]       #;baseA=[]
cod='';
year=0
dotc=True  #dotc=True- выполнять температурную коррекцию,  =False - не выполнять
#------------------------------------------------------------------------


def opentf(dt):      # write temperature file
	fnameoutt=cod+repr(dt[0])+'_td'   #
	res=openrff(3,fnameoutt,True)    # try open temperature output
	if res==-1:  #file dos not exist, shall create empty
		res=openwff(3,fnameoutt,2)
		if res==-1:
			print('Error open file')
			sys.exit(-1)
		Cods[3][1]='Td'
		Units[3][1]='C'
		Cods[3][2]='Te'
		Units[3][2]='C'
		Comments[3][1]='CMVS-1  sensor temperature'
		Comments[3][2]='CMVS-1  electronic temperature'
		Expl_txts[3]='CMVS-1 temperature 1-min data\n'
		dd0=dt2mjd(dt[0],1,1)+0.5/1440
		dd1=DayOfYear(dt[0],12,31)
		for doy in xrange(1440*dd1):
			outstr=struct.pack(frmts[3],dd0+doy/1440.0,*[-1.0E+32,-1E+32])
			ffd[3].write(outstr)
			Nrows[3]=Nrows[3]+1
		Sampleperiods[3]=60.0           # temperature 1 min
		closeff(3)
		res=openrff(3,fnameoutt,True)    # open temperature output
	return res

#--------------------------------------------------------------
def savesdata(mjd):
	global td,ts,sv,scount,phd
	dt=mjd2dt(mjd)
	td=eps[3]*td/scount
	ns=int(1440*(DayOfYear(dt[0],dt[1],dt[2])-1)+60*dt[3]+dt[4])
	ffd[3].seek(ns*Recsizes[3]+8)
	outstr=struct.pack('f',td)
	ffd[3].write(outstr)
	tc=td-t0                         #  температура приведения 25 С
	for j in range(scount):
		for i in range(3):
			phd[i]=eps[i]*sv[j][i]
			if dotc: phd[i]=phd[i]+tk[i]*tc
		for i in range(3):   # sensor unit rotation
				phd1[i]=MP[i][0]*phd[0]+MP[i][1]*phd[1]+MP[i][2]*phd[2]+base[i]
		ns=int(86400*(dt[2]-1)+3600*dt[3]+60*dt[4]+tv[j][1])
		outstr=struct.pack('3f',phd1[0],phd1[1],phd1[2])
		ffd[1].seek((ns)*Recsizes[1]+8)
		ffd[1].write(outstr)
	scount=0;td=0;ts=0



#--------------------------------------------------------------
def m2ff(filein,outdir):
    global tv,sv,scount,td,ts,base,baseA,eps,tk,cod,cmin
    cdir=os.getcwd()
    if outdir=='':    #  по умолчанию создает в текущей
          outdir=cdir+'\\'
    dpath,npath=os.path.split(filein)
    if dpath!='': dpath=dpath+'\\'
    cod='BAR_'  #npath[0:4]
    cod=cod.upper()
    try:
        fpar=open(cod+'_cmvspar.txt ','r')    #
    except:
#        fpar=open(dpath+'MOS1'+'_cmvspar.txt ','r')  # data dir
        fpar=open('d:\\CMVS_DAT\\Bartington\\KLD2_cmvspar.txt','r')  # data dir

    s=fpar.readline()
    st=fpar.readline().split()
    eps=[float(st[0]),float(st[1]),float(st[2]),float(st[3])];
    st=fpar.readline().split()
    base=[float(st[0]),float(st[1]),float(st[2]),float(st[3])] #,float(sbase[3]),float(sbase[4])];
    st=fpar.readline().split()
    tk=[float(st[0]),float(st[1]),float(st[2])];
    st=fpar.readline().split()
    MP[0]=[float(st[0]),float(st[1]),float(st[2])]
    st=fpar.readline().split()
    MP[1]=[float(st[0]),float(st[1]),float(st[2])]
    st=fpar.readline().split()
    MP[2]=[float(st[0]),float(st[1]),float(st[2])]
    fpar.close()
    dinm=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    s1=1.0/86400.0     # 1 second
    sh=0.0;sd=0.0;sz=0.0; n=0
    count=0; sec=0

    flist=[]
    if fmask.find('.1m')>0 or   fmask.find('.min')>0 :  flist =glob.glob(fmask)  # get dir
    if len(flist)>0:    #   convert 1-min data
         hdz=N.zeros((30),N.float)
         for filein in flist:             #   1 min data
            fin=open(filein,'rb')
            s=fin.read(28)
            if len(s)<28: break
            tm =struct.unpack('d5f',s)
            tc=tm[1]*eps[3] - 25   # +base[3]
            dt=mjd2dt(tm[0]+15018 ) # -1.0/86400)  # first sec in data = 1
            year=dt[0]
            if year%4==0: dinm[2]=29

# open  1 min FF
            if  outdir.find('dbn')>0:
                outdir=outdir+repr(dt[0])+'\\'+'%02d'%dt[1]+'\\MAG\\'
            fnameout=outdir+cod+repr(dt[0])+'%02d'%dt[1]+'00_60pp'
            print(filein+'->'+fnameout)
            opentf(dt)
            res=openrff(1,fnameout,True)    # try open output
            if res==-1:  #file dos not exist, shall create empty
                res=openwff(1,fnameout,3)
                if res==-1:
                    print('Error open file')
                    sys.exit(-1)
                Cods[1][1:5]=[cod+'H',cod+'E',cod+'Z']
                Units[1][1:4]=['nT','nT','nT']
                Comments[1][1:4]=4*['MOS2 geomagnetic observatory, IZMIRAN']
                Expl_txts[1]='MOS1 observatory preliminary 1 min data\n'
                doy0=DayOfYear(dt[0],dt[1],1)+dt2mjd(dt[0])-1+0.5/1440.0
                for doy in xrange(1440*dinm[dt[1]]):    # fill 1 min FF by missing values
                     outstr=struct.pack(frmts[1],doy0+doy/1440.0,-1.0E+32,-1.0E+32,-1.0E+32)
                     ffd[1].write(outstr)
                     Nrows[1]=Nrows[1]+1
                Sampleperiods[1]=60.0
                closeff(1)
                res=openrff(1,fnameout,True)
                if res==-1:
                    print('Error open file')
                    sys.exit(-1)
            fin.seek(0)

            while True:
                s=fin.read(24)
                if len(s)<24: break
                tm =struct.unpack('d4f',s)
                td=tm[4]
#                te=tm[5]
                tc=td-t0
                dt=mjd2dt(tm[0]+15018 )   # -1.0/86400)  # first sec in data = 1
                phd=[0,0,0,0]
#                for i in range(3):
#                    phd[i]=eps[i]*tm[i+1]
#                    if dotc: phd[i]=phd[i]+tk[i]*tc

                phd[0]=eps[0]*tm[2]
                phd[1]=eps[1]*tm[1]
                phd[2]=eps[2]*tm[3]
#                    if dotc: phd[i]=phd[i]+tk[i]*tc

                for i in range(3):
                    phd1[i]=MP[i][0]*phd[0]+MP[i][1]*phd[1]+MP[i][2]*phd[2]+base[i]  # sensor rotation
                outstr=struct.pack('3f',phd1[0],phd1[1],phd1[2])
                ns=1440*(dt[2]-1)+60*dt[3]+dt[4]  #+dt[5]
                ffd[1].seek((ns)*Recsizes[1]+8)
                ffd[1].write(outstr)
#                ns=int(1440*(DayOfYear(dt[0],dt[1],dt[2])-1)+60*dt[3]+dt[4])
#                ffd[3].seek(ns*Recsizes[3]+8)
#                outstr=struct.pack('2f',td,te)
#                ffd[3].write(outstr)

# convert 1 sec  data
    flist=[]
    if fmask.find('.sec')>0  or fmask.find('.1sb')>0:  flist=glob.glob(fmask)  # get dir
    if len(flist)>0:
        for filein in flist:
            fin=open(filein,'rb')
            s=fin.read(24)
            if len(s)<24: break
            tm =struct.unpack('d4f',s)
            tc=tm[1]*eps[3] - 25   # +base[3]
            dt=mjd2dt(tm[0]+15018)   #-1.0/86400)  # first sec in data = 1
            year=dt[0]
            if year%4==0: dinm[2]=29
            opentf(dt)
            if  outdir.find('dbn')>0:
                outdir=outdir+repr(dt[0])+'\\'+'%02d'%dt[1]+'\\MAG\\'
            fnameout=outdir+cod+repr(dt[0])+'%02d'%dt[1]+'00_01pp'
            print(filein+'->'+fnameout)
            res=openrff(1,fnameout,True)    # try open output
            if res==-1:  #file dos not exist, shall create empty
                res=openwff(1,fnameout,3)
                if res==-1:
                    print('Error open file')
                    sys.exit(-1)
                Cods[1][1:4]=[cod+'H',cod+'E',cod+'Z']
                Units[1][1:4]=['nT','nT','nT']
                Comments[1][1:4]=3*['MOS1 geomagnetic observatory, IZMIRAN']
                Expl_txts[1]='MOS1 observatory preliminary 1 sec data\n'
                doy0=DayOfYear(dt[0],dt[1],1)+dt2mjd(dt[0])-1+0.5/1440.0/60.0
                for doy in xrange(60*1440*dinm[dt[1]]):    # fill 1 sec FF by missing values
                     outstr=struct.pack(frmts[1],doy0+doy/1440.0/60,-1.0E+32,-1.0E+32,-1.0E+32)
                     ffd[1].write(outstr)
                     Nrows[1]=Nrows[1]+1
                Sampleperiods[1]=1.0
                closeff(1)
                res=openrff(1,fnameout,True)
                if res==-1:
                    print('Error open file'+fnameout)
                    sys.exit(-1)
            fin.seek(0)
            cmin=0
            while True:
                s=fin.read(24)
                if len(s)<24: break
                tm =struct.unpack('d4f',s)
                dt=mjd2dt(tm[0]+15018 )   # -1.0/86400)  # first sec in data = 1
                mjd=tm[0]+15018
                dt=mjd2dt(mjd )   # -1.0/86400)  # first sec in data = 1
                if cmin!=dt[4] and  scount>0:   #new minute
                   savesdata(tv[0][0])
                   cmin=dt[4]
         #       sv[scount,:]=tm[1:4]
         
                sv[scount,0]=tm[2]; sv[scount,1]=tm[1]
                sv[scount,2]=tm[3]; #sv[scount,3]=tm[4]

                tv[scount]=[mjd,dt[5]]
                td=td+tm[4]
                scount=scount+1

            if scount>0:
                savesdata(tv[0][0])
    ffd[1].close()
#    ffd[3].close()


#=========================================
if __name__ == "__main__":
      if len(sys.argv)<2:
        print('  Moscow -1 1 sec or 1 min binary to Flat File converter')
        print( r'  mos1_2ff InputFileMask [Output_dir  E:\DBN\]')
#        sys.exit()

      fmask=sys.argv[1]
      outdir=''
      if len(sys.argv)>=3:   outdir=sys.argv[2]

      m2ff(fmask,outdir)
      print('All done')
