# -*- coding: cp1251 -*-

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from monthdelta import monthdelta

root = Tk()  # Tkinter window
root.withdraw()  # We make it invisible

# importing part of file
openlist = [each[:-4] for each in askopenfilenames(
    title="Выберите *.csv файл",
    filetypes=(("csv files", "*.csv"),
               ("all files", "*.*")))]

root.destroy()  # closing the invisible window


# main part of file
def csv_slice(filename):  # reading and plotting function
    print('Now processing:  %s' % filename.split('/')[-1])
    df = pd.read_csv(filename+'.csv', sep=';', engine='python', encoding='utf8',
                     index_col='date and time', parse_dates=True)
    # "engine" and "encoding" parameters were added to solve the problem with cyrillic path to file
    print(df.info())

    for month in range(12):
        mon_df = df[df.index[0]+monthdelta(month):df.index[0]+monthdelta(month+1)]
        outfile = open('%s-%02d.csv' % (filename, month+1), 'w')
        mon_df.to_csv(outfile, sep=';')
        outfile.close()





        # print(df.index[0]:)
        # print(df[regex=':])
        # 2007-01-31 23:59:30


for file in openlist:
    csv_slice(file)

print('Done')
