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
import julian


Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

# next block takes full-path names of files without extension to openlist
openlist = [each[:-3] for each in askopenfilenames(
    title="Выберите *.ffd или *.ffh файл",
    filetypes=(("ffd files", "*.ffd"), ("ffh files", "*.ffh"), ("X-files", "X.*")))]

# openlist = ['C:/Users/Evgeny/PycharmProjects/ffprocessing/test.']  # testing version of openlist


# here's the main part of file:
def binff2csv(filename, jtc=False):  # converting function
    # filename = 'C:/***/*...*/**.' with dot in the end
    # 'jtc' means 'julian time code'

    # 1. first we should get info from header files
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
        if '----' in strin:
            break
        elif 'RECORD' in strin:
            recsize = int(value)
        elif 'COLUMNS' in strin:
            Ncols = int(value)
        elif 'ROWS' in strin:
            Nrows = int(value)
        elif 'MISSING' in strin:
            Missvs = numpy.float64(value)  # todo check out header file for other parameters
    ffh.readline()
    # then we read the rest of the header file
    colheaders = []  # headers of our csv-table
    for strin in ffh:
        if strin.find('<') >= 0:
            colheaders.append(strin.split('<')[1].split('>')[0])
        else:
            break
    ffh.close()  # end of header reading

    print('file length is: %d counts' % Nrows)
    print('number of colheaders: %d' % (Ncols + 1))
    print('estimated file size: %d' % (recsize * Nrows))

    # 2. then we open binary file
    try:
        ffd = open(filename + 'ffd', 'r')
    except:  # todo посмотреть в викиверсити экзит коды
        print('something wrong with *.ffd files')
        raise SystemExit
    dt = numpy.dtype([('time', 'f8'), ('data', repr(Ncols) + 'f4')])  # template for reading binary file
    n1 = 0  # first count
    n2 = Nrows  # last count
    a = numpy.fromfile(ffd, dtype=dt, count=int(n2 - n1))  # primary array
    b = []  # list in list todo make the numpy array
    for row in a:  # convert array format to simple table
        rowlist = [row[0]]
        for value in row[1]:
            rowlist.append(value)
        b.append(rowlist)
    ffd.close()  # end of ffd reading

    # 3. and now we're going to convert our list to dataframe
    if jtc:
        timecode = [i[0] for i in b]  # we can use julian timecode
    else:
        timecode = [julian.from_jd(i[0], 'mjd').strftime('%Y-%m-%d %H:%M:%S') for i in b]
    data = [i[1:] for i in b]
    df = pd.DataFrame(data, index=timecode, columns=colheaders[1:])  # todo missing to None
    df.index.name = 'timecode' if jtc else 'date and time'
    df = df.replace({Missvs: None, -1.0000000331813535e+32: None})  # it's time to remove missing values

    # 4. finally we make *.csv
    outfile = open(filename + 'csv', 'w')
    df.to_csv(outfile, sep=';')
    outfile.close()


# executing part of file
for file in openlist:
    binff2csv(file)

print('Done')
