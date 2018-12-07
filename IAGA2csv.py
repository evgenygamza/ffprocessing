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
        arr.append(string.split())
    df = pd.DataFrame(arr)


    # df = pd.read_csv(filename, sep=' ', engine='python', encoding='utf8',
    #                  parse_dates=True,  # index_col='date and time'
    #                  skiprows=19)
    # # "engine" and "encoding" parameters were added to solve the problem with cyrillic path to file
    # # todo make a "window" filter for invalid values (00100) (someday)
    print(df.info())
    # df.index.name = 'date and time'

    # 4. finally we make *.csv
    outfile = open(filename[:-3] + 'csv', 'w')
    df.to_csv(outfile, sep=';')
    outfile.close()


# executive part
for file in openlist:
    IAGA2csv(file)

print('Done')
