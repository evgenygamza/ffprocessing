# -*- coding: cp1251 -*-

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

root = Tk()  # Tkinter window
root.withdraw()  # We make it invisible

# importing part of file
openlist = askopenfilenames(
    title="�������� *.csv ����",
    filetypes=(("csv files", "*.csv"),
               ("all files", "*.*")))

root.destroy()  # closing the invisible window


llll = []
nnnn = ['AE', 'AU', 'AL']  # fixme ��� �������� ��� ���� ������. �������� ����� ���� ��������


# main part of file
def csv_plot(filename):  # reading and plotting function
    print('Now processing:  %s' % filename.split('/')[-1])
    df = pd.read_csv(filename, sep=';', engine='python', encoding='utf8',
                     index_col='date and time', parse_dates=True)
    # "engine" and "encoding" parameters were added to solve the problem with cyrillic path to file
    # todo make a "window" filter for invalid values (00100) (someday)
    print(df.info())

    if 'AU' in df:
        df.filter(regex=r'AE').plot(ax=axes[0]), df.filter(regex=r'AU').plot(ax=axes[0]), df.filter(regex=r'AL').plot(ax=axes[0])
        df.filter(regex=r'AE').plot(ax=axes[1]), df.filter(regex=r'AU').plot(ax=axes[1]), df.filter(regex=r'AL').plot(ax=axes[1])
        df.filter(regex=r'AE').plot(ax=axes[2]), df.filter(regex=r'AU').plot(ax=axes[2]), df.filter(regex=r'AL').plot(ax=axes[2])
        for i in range(len(axes[0].lines)):
            llll.append([])
            for j in [0, 1, 2]:
                llll[i].append(axes[j].lines[i])
    else:
        for col in df.columns:
            df[col] -= df[col].mean()  # subtract average value from column
            # df[col] -= df[col].loc[df[col].first_valid_index()]  # subtract first valid value from column
        df.filter(regex=r'..._[HX]').plot(ax=axes[0])  # add components to relevant subplots
        df.filter(regex=r'..._[EY]').plot(ax=axes[1])  # using regular expressions as a filter parameter
        df.filter(regex=r'..._Z').plot(ax=axes[2])


# executive part todo make a 3 or 4 subplots window
def func(label):
    for i in range(len(llll)):
        if label == nnnn[i]:
            for j in [0, 1, 2]:
                llll[i][j].set_visible(not llll[i][j].get_visible())
    plt.draw()


fig, axes = plt.subplots(3, 1, figsize=(10, 5), sharex=True)
plt.subplots_adjust(left=0.2)
for file in openlist:
    csv_plot(file)

rax = plt.axes([0.05, 0.4, 0.1, 0.15])
check = CheckButtons(rax, nnnn, (True for i in llll))
check.on_clicked(func)
plt.style.use('ggplot')
plt.show()

print('Done')
