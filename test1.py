# -*- coding: cp1251 -*-

import numpy
# from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)


#открываем файл заголовка
ffh=open(filename,'r')  
for strin in ffh: #цикл для чтения первой части файла .ffh
    value=strin.split('=')[-1]    #переменная цепляет значения того или иного параметра при проходе цикла
    if strin.find('----')>=0:
        break
    elif strin.find('RECORD')>=0:
        recsizes=int(value)
    elif strin.find('COLUMNS')>=0:
        Ncols=int(value)
    elif strin.find('ROWS')>=0:
        Nrows=int(value)
    elif (strin.find('MISSING')>=0):
        Missvs=float(value)
ffh.close()

print('file length is: %d counts' % Nrows)
print('number of columns: %d' % Ncols)

#открываем бинарный файл
ffd=open('ALK_20180900_60pp.ffd','rb') 
dt=numpy.dtype([('time','f8'),('data',repr(Ncols)+'f4')]) #Создает формат первичного массива
n1=0; n2=Nrows

a = numpy.fromfile(ffd, dtype=dt, count=int(n2-n1)) #вытаскиваем массив
b=[]
for row in a:                                       #причесываем массив
    rowlist=[]
    rowlist.append(row[0])
    for value in row[1]:
        rowlist.append(value)
    b.append(rowlist)
    
#пишем в файл
outfile = open('ALK_20180900_60pp.csv', 'w')
for row in b:
    outfile.write('%14.8f;' % row[0])
    for n in range(1, Ncols+1):
        if str(row[n])==str(Missvs):    #"элегантное решение", без преобразования в строку не работает
            outfile.write(';')
        else:
            outfile.write('%f;' % row[n])     
    outfile.write('\n')
outfile.close()