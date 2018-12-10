# -*- coding: cp1251 -*-

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import matplotlib.pyplot as plt

root = Tk()  # Tkinter window
root.withdraw()  # We make it invisible

# next block takes full-path names of files without extension to openlist
openlist = askopenfilenames(title="Выберите *.csv файл",
                            filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
root.destroy()  # closing the invisible window


# main part of file
def IAGA2csv(filename):  # reading and plotting function
    print('Now processing:  %s' % filename.split('/')[-1])
    file = open(filename, 'r')
    for i in range(14):
        file.readline()
    arr = []
    for string in file:
        x = string.split()
        x[0:2] = [' '.join(x[0:2])]
        arr.append(x)
    ind = [line[0] for line in arr[1:]]
    df = pd.DataFrame([l[1:] for l in arr[1:]], columns=arr[0][1:-1], index=[line[0] for line in arr[1:]])

    # todo read_scv instead readline and 'for' (someday)
    print(df.info())
    df.index.name = 'date and time'

    # 4. finally we make *.csv
    outfile = open(filename[:-3] + 'csv', 'w')
    df.to_csv(outfile, sep=';')
    outfile.close()


# executive part
for file in openlist:
    IAGA2csv(file)

print('Done')
