# -*- coding: cp1251 -*-
import string
import struct
import math
import time
import numpy

#  ------------------------------------functions--------------
#  mjd2dt(mjulian_day):
# DayOfYear(year,month, day):
# dt2mjd(year,month=1, day=1,hh=0,mn=0,ss=0.0):
# mjd2str(jd):
# mjd2str(jd)
# openrff(Nh,fname):
# readff(Nh):
# at,ad,minv,maxv=readffa(Nh,n1=0,n2=0,cset=[])       cset=[1,2,3...]
# openwff(Nh,fname,n_dc):
# closeff(Nh):
# copyffh(n1,n2):
#-----global variables-----------
# Recsizes=[0]*5
# Nrows=[0]*5
# Ncols=[0]*5
# Missvs=[0.0]*5
# Cods=[[],[],[],[],[]]
# Endians=[[],[],[],[],[]]
# Comments=[[],[],[],[],[]]
# Expl_txts=[[],[],[],[],[]]
# Types=[[],[],[],[],[]]
# Units=[[],[],[],[],[]]
# ffh=[1,1,1,1,1]
# ffd=[1,1,1,1,1]
# FFnames=['','','','','']
# Sampleperiods=[0.0]*5
# Starttimes=[0,0,0,0,0]
# Endtimes=[0,0,0,0,0]
# frmts=['','','','','']
# Expl_txts=['','','','','']
#---------------------------------------------------
def mjd2dt(mjulian_day):
    jd = mjulian_day+2400001.0
    Z = int(jd)
    F = jd - Z
    A = Z
    if Z >= 2299161:
        alpha = int((Z - 1867216.26)/36254.25)
        A = Z + 1 + alpha - int(alpha/4)
    B = A + 1524
    C = int((B - 122.1)/365.25)
    D = int(365.25 * C)
    E = int((B - D)/30.6001)
    day = B - D - int(30.6001 * E)  # + F
    hh=int(24*F)
    t=(1440*(F-hh/24.))
    mn=int(t)
    ss=60*(t-mn)
    if E < 13.5:
        month = int(E - 1)
    else:
        month = int(E - 13)
    if month > 2.5:
        year = int(C - 4716)
    else:
        year = int(C - 4715)
    return year,month, day,hh,mn,ss
#---------------------------------------------------
def DayOfYear(year,month, day):
    if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
        n = int((275*month)//9 -   ((month + 9)//12) + int(day) - 30)
    else:
        n = int((275*month)//9 - 2*((month + 9)//12) + int(day) - 30)
    if n < 1 or n > 366:
        print('Dayoftheyear Internal Error')
#         raise "Internal error"
    return n
#---------------------------------------------------
def dt2mjd(year,month=1, day=1,hh=0,mn=0,ss=0.0):
    if month < 3:
        year  = year - 1
        month = month + 12
    julian = int(365.25*year) + int(30.6001*(month+1)) + day + 1720994.5
    tmp = year + month / 100.0 + day / 10000.0
    if tmp >= 1582.1015:
        A = year // 100
        B = 2 - A + A//4
        jul = int(julian + B+0.55)-2400001
#    jul=int(JulianAstro(year,month, day) + 0.55)
    return jul+hh/24.+mn/1440.+ss/86400.
#---------------------------------------------------
def mjd2str(jd):
    jd=int(86400000*jd+0.5)/86400000.
    yy,mm,dd,hh,mn,ss=mjd2dt(jd)
    return '%04d'%yy+'-'+'%02d'%mm+'-'+'%02d'%dd+' '+'%02d'%hh+':'+'%02d'%mn+':'+'%05.2f'%ss
#---------------------------------------------------
def openrff(Nh,fname,update=False): #функция открытия .ffh и .ffd -файла
    #Загадочная Nh - какая-то переменная int, возможно используется в плоте, fname - имя файла, строка, возможность обновления  
# open Flat File for reading  or updating (if update=True)
    FF2=''
    Cods[Nh]=[];Units[Nh]=[];Comments[Nh];Types[Nh] #все переменные - списки из 5 пустых списков

    i=fname.find('.')   #Возвращает позицию точки в названии файла
    if i>0:
        fname=fname[:i]
    try:
        ffh[Nh]=open(fname+'.ffh','r')  #открывает файл заголовка
    except:
        return -1   
    FFnames[Nh]=fname #список из пяти пустых строк
    rab=ffh[Nh].readline()
    if (rab.find('VERSION')>=0):    #New version
        FF2='VERSION3'  #Видимо, если в первой строке файла написано слово Version, то версия третья
#    print('test1:'+rab)
    if FF2!='':
        while 1 :   #Запускает цикл для файлов версии 3
            if rab.find('------')>=0:
                break
            try:    # пытается выудить всю инфу из файла в соответствующие переменные
                s1,s2=rab.split('=')
                s1=s1.upper()
                if (s1.find('RECORD')>=0):
                    Recsizes[Nh]=int(s2)
                if (s1.find('ROWS')>=0):
                    Nrows[Nh]=int(s2)
                if (s1.find('COLUMNS')>=0):
                    Ncols[Nh]=int(s2)
                if (s1.find('MISSING')>=0):
                    Missvs[Nh]=float(s2)
                if (s1.find('RESOLUTION')>=0):
                    Sampleperiods[Nh]=float(s2)
                if (s1.find('ENDIAN')>=0):
                    Endians[Nh]=s2
                rab=ffh[Nh].readline() #Переход к следующему файлу
            except:
                return -2
        rab=ffh[Nh].readline()
        while 1:  #цикл прохода по второму блоку файла заголовка
            rab=ffh[Nh].readline()
            try:
                s1 =rab.split('<') #делаем список из заголовков столбцов
                Cods[Nh].append(s1[1][0:s1[1].index('>')])      #Заполняем Nh-элементы в соответствующих переменных
                Units[Nh].append(s1[2][0:s1[2].index('>')])     #заполняем елементами строк, отрезая ">" и пробелы за ним
                Comments[Nh].append(s1[3][0:s1[3].index('>')])
                Types[Nh].append(s1[4][0:s1[4].index('>')])
            except:
                break
    else:     # old header format
        i=rab.find('SP=')
        if i>0 :  Sampleperiods[Nh]=float(rab[i+3:].split()[0])
        rab=ffh[Nh].readline()
        rab=ffh[Nh].readline()
        Recsizes[Nh]=int(rab[22:])
        rab=ffh[Nh].readline()
        Ncols[Nh]=int(rab[40:])-1
        rab=ffh[Nh].readline()
        Nrows[Nh]=int(rab[40:])
        rab=ffh[Nh].readline()  #-------------
        rab=ffh[Nh].readline()  #name
        rab=ffh[Nh].readline()  #name
        rab=ffh[Nh].readline()  #name
        for i in range(Ncols[Nh]+1):
            rab=ffh[Nh].readline().split()
            print(rab)
            Cods[Nh].append(rab[1])
            Units[Nh].append(rab[2])
            Comments[Nh].append(rab[3])
    try: #Собственно, открываем файл
        if update:
            ffd[Nh]=open(fname+'.ffd','rb+') 
        else:
            ffd[Nh]=open(fname+'.ffd','rb')
    except:
        return -3
    frmts[Nh]='<d'+repr(Ncols[Nh])+'f' #переменная хранит информацию о структуре файла # '<d_f', где _ - число столбцов
    rl=struct.calcsize(frmts[Nh])
    Starttimes[Nh]=readff1(Nh,0)[0]
    Endtimes[Nh]=readff1(Nh,Nrows[Nh]-1)[0]
    ffh[Nh].close()
    return 0
#---------------------------------------------------
def readff1(Nh,Nrec): #Функция возвращает единичный отсчет с порядковым номером Nrec из файла Nh
#    try:
    ffd[Nh].seek(Recsizes[Nh]*Nrec)
    r=ffd[Nh].read(Recsizes[Nh])
    if len(r)==Recsizes[Nh]:
        return numpy.array(struct.unpack(frmts[Nh],r))
    else:
        return None
#----------------------------------------------------------
##def readffa_old(Nh,n1=0,n2=0,cset=[]):  # cset start from 1
##     if n2==0: n2=Nrows[Nh]
##     if cset==[]: cset=range(1,Ncols[Nh]+1)
##     selection=cset[:]
##     selection=numpy.array(selection)
##     tm=numpy.zeros((n2-n1), numpy.float64)
##     dm=numpy.zeros(((n2-n1),(len(cset))), numpy.float32)
##     ffd[Nh].seek(n1*Recsizes[Nh])
##     for i in xrange(n2-n1):
##         r1=ffd[Nh].read(Recsizes[Nh])
##         if len(r1)==Recsizes[Nh]:
##              tbuf=numpy.array(struct.unpack(frmts[Nh],r1))
##         else:
##              return None
##         tb=tbuf[selection]
##         tb[tb<-1.0E+31]=numpy.nan
##         tm[i]=tbuf[0]
##         dm[i,:]=tb[:]
##     vmin=numpy.nanmin(dm,axis=0)
##     vmax=numpy.nanmax(dm,axis=0)
##     return tm,dm,vmin,vmax

def readffa(Nh,n1=0,n2=0,cset=[]): #Функция чтения бинарного файла 
    # cset start from 1 
    if n2==0: n2=Nrows[Nh]
    if cset==[]: cset=list(range(1,Ncols[Nh]+1))
    selection=cset[:]
    selection=numpy.array(selection)
    selection=selection-1
    ffd[Nh].seek(n1*Recsizes[Nh])
#     dt=numpy.dtype([('mjd','f8'),('data','f4')])
    dt=numpy.dtype([('mjd','f8'),('data',repr(Ncols[Nh])+'f4')]) #задание структуры массива
#     a = numpy.fromfile(ffd[Nh],numpy.dtype('f8,'repr(Ncols[Nh])+'f4'),count=int(n2-n1))
    a = numpy.fromfile(ffd[Nh],dtype=dt,count=int(n2-n1))
    tm=a[:]['mjd']
#     if numpy.size(selection)>0:  dm=a[:]['data'][:,selection]
#     else:
#           dm=a[:]['data']
#           dm=numpy.resize(dm,(numpy.size(tm),1))
    dm=a[:]['data']
    t=numpy.where(dm<-1.0E+31)
    dm[t]=numpy.nan
    if len(numpy.shape(dm))==1 :      # 1 dimensional array? add false column
        dm=numpy.column_stack([dm, dm])
    vmin=numpy.nanmin(dm,axis=0)
    print(vmin)
    vmax=numpy.nanmax(dm,axis=0)
    print(vmax)
    return tm,dm,vmin,vmax

#-----------------------------------------------------
def openwff(Nh,fname,n_dc):
# open Flat File for writing
    try:
        ffh[Nh]=open(fname+'.ffh','w')
    except:
        return -1
    try:
        ffd[Nh]=open(fname+'.ffd','wb')
    except:
        return -1
    Ncols[Nh]=n_dc
    FFnames[Nh]=fname
    Cods[Nh]=['Time']
    Units[Nh]=['Days']
    Comments[Nh]=['Modify Julian Day=JD-2400000.5']
    Types[Nh]=['T']
    Nrows[Nh]=0
    for i in range(n_dc):
        Cods[Nh].append('')
        Units[Nh].append('')
        Comments[Nh].append('')
        Types[Nh].append('')
    frmts[Nh]='<d'+repr(Ncols[Nh])+'f'
    Recsizes[Nh]=struct.calcsize(frmts[Nh])
    return 0
#---------------------------------------------------
# update data (but save old time) in 1 record
def updateff1(Nh,Nrec,dat):
# dat -numpy array
    missv=numpy.isnan(dat)
#       dat[missv]=-1.0E+32
    outstr=struct.pack(frmts[Nh][2:],*dat)
    ffd[Nh].seek((Nrec)*Recsizes[Nh]+8)
    ffd[Nh].write(outstr)
#       ffd[Nh].flush()
#----------------------------------------------------
# add  record to new FF
def writeff1(Nh,dat):
    missv=numpy.isnan(dat)
    dat[missv]=-1.0E+32
    outstr=struct.pack(frmts[Nh],*dat)
    ffd[Nh].write(outstr)
    Nrows[Nh]=Nrows[Nh]+1

#---------------------------------------------------
def closeff(Nh):
    ffd[Nh].close()
    ffd[Nh]=open(FFnames[Nh]+'.ffd','rb')
    Recsizes[Nh]=8+4*Ncols[Nh]
    r=ffd[Nh].read(8)
    t1,=struct.unpack('d',r)
    ffd[Nh].seek(Recsizes[Nh]*(Nrows[Nh]-1))
    r=ffd[Nh].read(8)
    t2,=struct.unpack('d',r)
    Sampleperiods[Nh]=86400*(t2-t1)/(Nrows[Nh]-1)
    ffd[Nh].close()
    ffh[Nh].write('FLAT FILE VERSION=3.0\n')
    ffh[Nh].write('DATE FILES CREATED='+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'\n')
    ffh[Nh].write('RECORD LENGTH, BYTES= '+repr(Recsizes[Nh])+'\n')
    ffh[Nh].write('NUMBER OF DATA COLUMNS=  '+repr(Ncols[Nh])+'\n')
    ffh[Nh].write('NUMBER OF ROWS= '+repr(Nrows[Nh])+'\n')
    ffh[Nh].write('FLAG FOR MISSING DATA= -1.00E+32\n')
    ffh[Nh].write('TIME RESOLUTION, SEC= '+'%.4f'%Sampleperiods[Nh]+'\n')
    ffh[Nh].write('ENDIAN=LITTLE\n')
    ffh[Nh].write('------------------------------------------------------------------------------\n')
    ffh[Nh].write('NNN <name>     <units>    <description>                   <type><offset>\n')
    ffh[Nh].write('000 <Time>     <Days>     <Modify Julian Day=JD-2400000.5>  <T> <0000>\n')
    for i in range(1,Ncols[Nh]+1):
        ffh[Nh].write('%03d'%i+(' <'+Cods[Nh][i]+'>').ljust(12,' ')+('<'+Units[Nh][i]+'>').ljust(10,' ')+('<'+Comments[Nh][i]+'>').ljust(35,' ')+'<R> <'+'%04d'%(4*(i+1))+'>\n')
    ffh[Nh].write('\n')
    ffh[Nh].write('NOTES:')
    ffh[Nh].write('\n')
    ffh[Nh].write('Start time='+mjd2str(t1)+'\n')
    ffh[Nh].write('End   time='+mjd2str(t2)+'\n')
    if len(Expl_txts[Nh])>0:
        ffh[Nh].write(Expl_txts[Nh])
    ffh[Nh].write('END\n')
    ffh[Nh].close()
#---------------------------------------------------------------------
def copyffh(n1,n2):
# use after call openwff(n2)
    Missvs[n2]=Missvs[n1]
    Cods[n2]=Cods[n1]
    Endians[n2]=Endians[n1]
    Comments[n2]=Comments[n1]
    Expl_txts[n2]=Expl_txts[n1]
    Types[n2]=Types[n1]
    Units[n2]=Units[n1]

#---------------------------------------------------------------------------
global Nrows,Recsizes,Ncols,Missvs,Cods,Endians,Comments,Types,Units,Expl_txts
Recsizes=[0]*5 #Показывает размер единичной записи в бинарном файле
Nrows=[0]*5
Ncols=[0]*5
Missvs=[-1E+32]*5
Cods=[[],[],[],[],[]]
Endians=[[],[],[],[],[]]
Comments=[[],[],[],[],[]]
Expl_txts=[[],[],[],[],[]]
Types=[[],[],[],[],[]]
Units=[[],[],[],[],[]]
ffh=['','','','','']
ffd=['','','','','']    #переменная хранит открытый файл № Nh (до пяти штук)
FFnames=['','','','','']
Sampleperiods=[0.0]*5
frmts=['','','','','']
Starttimes=[0,0,0,0,0]
Endtimes=[0,0,0,0,0]
Expl_txts=['','','','','']
#-------------------------------------------
###ires=openrff(0,r'D:\Python\MyProgs\thmpos-E_20070801.ffd')
##ires=openrff(0,r'Z:\DBN\2005\12\MAG\SPM_20051200_01vp.ffh')
###ires=openrff(0,r'Z:\DBN\2006\01\mag\P02_20060100_60vp.ffd')
##t1=os.times()[1]
##tm,dm,vmin,vmax=readffa(0,0,Nrows[0],[1])
##pass
##t2=os.times()[1]
##print t2-t1
##plot(tm,dm[:,0])
##ax=gca()
##ax.set_ylim(vmin[0],vmax[0])
##show()
##pass
##pass
##print '****'


