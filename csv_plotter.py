# -*- coding: cp1251 -*-

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import matplotlib.pyplot as plt

Tk().withdraw()

# importing part of file
openlist = askopenfilenames(  # fixme не работает путь с кириллицей
    title="Выберите *.csv файл",
    filetypes=(("csv files", "*.csv"),
               ("all files", "*.*")))

# openlist = ['C:/Users/Evgeny/PycharmProjects/ffprocessing/test.csv']  # testing version of openlist

# # for cyrillic tests:
# openlist = ['C:/Users/Evgeny/YandexDisk/!ИЗМИРАН/Сентябрьские магнитограммы/SPB_20180900_60pp.csv']


# main part of file
def csv_plot(filename):  # reading and plotting function
    print('Now processing:  %s' % filename.split('/')[-1])
    df = pd.read_csv(filename, sep=';', engine='python', encoding='utf8',
                     index_col='date and time', parse_dates=True)
    # "engine" and "encoding" parameters was added to solve the problem with cyrillic path to file
    # todo make a filter for invalid values (10 sigma for example)
    print(df)
    print(df.info())
    df.plot()
    plt.show()


# executive part
for file in openlist:
    csv_plot(file)

print('Done')  # fixme why running does not stop?
