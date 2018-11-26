# -*- coding: cp1251 -*-

import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename


Tk().withdraw()

df = pd.read_csv(askopenfilename(initialdir=dir(0),
                                 filetypes=(("csv files", "*.csv"),
                                            ("all files", "*.*"))),
                                 sep=';')   # index_col='Date', parse_dates=True
print(df)
print(df.info())

# openlist = [each[:-3] for each in askopenfilenames(
#     title="Выберите *.ffd или *.ffh файл",
#     filetypes=(("ffd files", "*.ffd"), ("ffh files", "*.ffh"), ("X-files", "X.*")))]