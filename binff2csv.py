# -*- coding: cp1251 -*-
#
# this program makes from *.ffh and binary *.ffd files
# one *.csv file in the same directory.
# *.ffd and *.ffh must have same names
#
import numpy
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import pandas as pd

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

# next block takes full-path names of files without extension to openlist
openlist = [each[:-3] for each in askopenfilenames(
    title="Выберите *.ffd или *.ffh файл",
    filetypes=(("ffd files", "*.ffd"), ("ffh files", "*.ffh"), ("X-files", "X.*")))]

# openlist = ['C:/Users/Evgeny/PycharmProjects/ffprocessing/test.']  # testing version of openlist


# here's the main part of file:
def binff2csv(filename):  # converting function
    # try to open files
    try:
        ffh = open(filename + 'ffh', 'r')
    except:  # todo посмотреть в викиверсити экзит коды
        print('selected files are not suitable')
        raise SystemExit

    # reading first part of header file
    recsize = 0  # number of bytes in a single measure count
    Nrows = 0  # number of measurements
    Ncols = 0  # number of colheaders
    Missvs = 0  # value flagging missing data
    for strin in ffh:  # reading
        value = strin.split('=')[-1]  # variable takes parameters while passing cycle
        if strin.find('----') >= 0:
            break
        elif strin.find('RECORD') >= 0:
            recsize = int(value)
        elif strin.find('COLUMNS') >= 0:
            Ncols = int(value)
        elif strin.find('ROWS') >= 0:
            Nrows = int(value)
        elif strin.find('MISSING') >= 0:
            Missvs = float(value)  # todo check out header file for other parameters
    ffh.readline()
    colheaders = []  # headers of our csv-table
    for strin in ffh:
        if strin.find('<') >= 0:
            colheaders.append(strin.split('<')[1].split('>')[0])
        else:
            break
    ffh.close()

    print('file length is: %d counts' % Nrows)
    print('number of colheaders: %d' % (Ncols + 1))
    print('estimated file size: %d' % (recsize * Nrows))

    # open binary file
    ffd = open(filename + 'ffd', 'rb')
    dt = numpy.dtype([('time', 'f8'), ('data', repr(Ncols) + 'f4')])  # format of first array
    n1 = 0  # first count
    n2 = Nrows  # last count
    a = numpy.fromfile(ffd, dtype=dt, count=int(n2 - n1))  # primary array
    b = []  # flat array
    for row in a:  # convert array format to simple table
        rowlist = [row[0]]
        for value in row[1]:
            rowlist.append(value)
        b.append(rowlist)

    df = pd.DataFrame(b, columns=colheaders)
    print(df)

    # making .csv
    outfile = open(filename + 'csv', 'w')
    df.to_csv(outfile, sep=';')
    outfile.close()

# executing part of file
for file in openlist:
    binff2csv(file)

print('Done')
