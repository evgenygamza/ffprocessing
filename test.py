# -*- coding: cp1251 -*-
# import struct
import numpy
from matplotlib import pyplot as plt


# Ncols=0
# Nrows=0
# recsizes=0

#открываем файл заголовка
ffh=open('ALK_20180900_60pp.ffh','r')  
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
ffh.close()

print('file length is: %d' % Nrows)
print('number of columns: %d' % Ncols)

#открываем бинарный файл
ffd=open('ALK_20180900_60pp.ffd','rb') 
dt=numpy.dtype([('mjd','f8'),('data',repr(Ncols)+'f4')]) #Создает формат массива
n1=0; n2=Nrows

a = numpy.fromfile(ffd, dtype=dt, count=int(n2-n1)) #вытаскиваем массив int(n2-n1)
print(a)
# print(a[999])
# print(a[999][0], a[999][1][0])


#пишем в файл
# outfile = open('ALK_20180900_60pp.csv', 'w')
# for row in data:
#     for column in row:
#         outfile.write('%14.8f' % column)
#     outfile.write('\n')
# outfile.close()





# Дальше пока не точно

# t=[]
# h=[]
# d=[]
# z=[]
# for i in a:
#     t.append(i[0])
#     h.append(i[1][0])
#     d.append(i[1][1])
#     z.append(i[1][2])
#     
# # print(t)
# 
# 
# plt.plot(t[900:], h[900:], '-.')
# # plt.yticks(range(1, 100, 2))
# 
# 
# plt.show()

