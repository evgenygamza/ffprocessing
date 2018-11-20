# -*- coding: cp1251 -*-
#
# this program makes from *.ffh and binary *.ffd files
# one *.csv file in the same directory.
# *.ffd and *.ffh must have same names
#
import numpy
from tkinter import Tk
from tkinter.filedialog import askopenfilenames


Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing


# Let's take full-path names of files without extension to openlist
openlist = [each[:-3] for each in askopenfilenames(
    title="Выберите *.ffd или *.ffh файл",
    filetypes=(("ffd files", "*.ffd"), ("ffh files", "*.ffh"), ("X-files", "X.*")))]


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
    Ncols = 0  # number of columns
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
    ffh.close()
    print('file length is: %d counts' % Nrows)
    print('number of columns: %d' % (Ncols + 1))
    print('estimated file size: %d' % (recsize * Nrows))

    # open binary file
    ffd = open(filename + 'ffd', 'rb')
    dt = numpy.dtype([('time', 'f8'), ('data', repr(Ncols) + 'f4')])  # format of first array
    n1 = 0
    n2 = Nrows
    a = numpy.fromfile(ffd, dtype=dt, count=int(n2 - n1))  # take array
    b = []
    for row in a:  # convert array format to simple table
        rowlist = [row[0]]
        for value in row[1]:
            rowlist.append(value)
        b.append(rowlist)

    # making .csv  todo check out header file for useful info and take it to new csv
    outfile = open(filename + 'csv', 'w')
    for row in b:
        outfile.write('%14.8f;' % row[0])
        for n in range(1, Ncols + 1):
            if str(row[n]) == str(Missvs):  # fixme "elegant" decision, doesn't work without converting to str
                outfile.write(';')
            else:
                outfile.write('%f;' % row[n])
        outfile.write('\n')
    outfile.close()


for file in openlist:
    binff2csv(file)

print('Done')
