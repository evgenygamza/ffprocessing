# -*- coding: cp1251 -*-
#
# this program makes from *.ffh and binary *.ffd files
# one *.csv file in the same directory.
# *.ffd and *.ffh must have same names
#
import numpy
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()[:-3]  # show an "Open" dialog box and return the path to the selected file
print('full filename is:  ' + filename)

# open header file
try:
    ffh = open(filename + 'ffh', 'r')
except:  # посмотреть в викиверсити экзит коды
    print('there is no suitable file')
    raise SystemExit

# reading first part of .ffh
recsizes = 0  # number of bytes in a single measure count
Nrows = 0  # number of measurements
Ncols = 0  # number of columns
Missvs = 0  # value flagging missing data
for strin in ffh:  # reading first part of .ffh
    value = strin.split('=')[-1]  # variable takes parameters while passing cycle
    if strin.find('----') >= 0:
        break
    elif strin.find('RECORD') >= 0:
        recsizes = int(value)
    elif strin.find('COLUMNS') >= 0:
        Ncols = int(value)
    elif strin.find('ROWS') >= 0:
        Nrows = int(value)
    elif (strin.find('MISSING') >= 0):
        Missvs = float(value)
ffh.close()
print('file length is: %d counts' % Nrows)
print('number of columns: %d' % Ncols)
print('estimated file size: %d' % (recsizes*Nrows))

# open binary file
ffd = open(filename + 'ffd', 'rb')
dt = numpy.dtype([('time', 'f8'), ('data', repr(Ncols) + 'f4')])  # format of first array
n1 = 0
n2 = Nrows

a = numpy.fromfile(ffd, dtype=dt, count=int(n2 - n1))  # take array
b = []
for row in a:  # convert array format to simple table
    rowlist = []
    rowlist.append(row[0])
    for value in row[1]:
        rowlist.append(value)
    b.append(rowlist)

# пишем в файл
outfile = open(filename + 'csv', 'w')
for row in b:
    outfile.write('%14.8f;' % row[0])
    for n in range(1, Ncols + 1):
        if str(row[n]) == str(Missvs):  # "elegant" decision, doesn't work without coverting to str
            outfile.write(';')
        else:
            outfile.write('%f;' % row[n])
    outfile.write('\n')
outfile.close()
