# -*- coding: cp1251 -*-

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import matplotlib.pyplot as plt

root = Tk()  # Tkinter window
root.withdraw()  # We make it invisible

# importing part of file
openlist = askopenfilenames(
    title="Выберите *.csv файл",
    filetypes=(("csv files", "*.csv"),
               ("all files", "*.*")))

# # some openlists for testing:
# # short single file:
# openlist = ['C:/Users/Evgeny/PycharmProjects/ffprocessing/test.csv']

# # file with cyrillic path:
# openlist = ['C:/Users/Evgeny/YandexDisk/!ИЗМИРАН/Сентябрьские магнитограммы/SPB_20180900_60pp.csv']

# # list of three files:
# openlist = ['C:/Users/Evgeny/YandexDisk/!ИЗМИРАН/Сентябрьские магнитограммы/SPB_20180900_60pp.csv',
#             'C:/Users/Evgeny/YandexDisk/!ИЗМИРАН/Сентябрьские магнитограммы/ALK_20180900_60pp.csv',
#             'C:/Users/Evgeny/PycharmProjects/ffprocessing/test.csv']

root.destroy()  # closing the invisible window


# main part of file
def csv_plot(filename):  # reading and plotting function
    print('Now processing:  %s' % filename.split('/')[-1])
    df = pd.read_csv(filename, sep=';', engine='python', encoding='utf8',
                     index_col='date and time', parse_dates=True)
    # "engine" and "encoding" parameters was added to solve the problem with cyrillic path to file
    # todo make a filter for invalid values (10 sigma for example)
    print(df)
    print(df.info())
    # df.plot(subplots=True, figsize=(10, 5))
    # # todo попробовать этим
    df.filter(regex=r'ALK_H').plot(ax=axes[0])
    df.filter(regex=r'ALK_E').plot(ax=axes[1], sharex=True)
    df.filter(regex=r'ALK_Z').plot(ax=axes[2], sharex=True)


# executive part
fig, axes = plt.subplots(3, 1, figsize=(10, 5))
for file in openlist:
    csv_plot(file)
plt.show()

print('Done')
