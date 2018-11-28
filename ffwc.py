# -*- coding: cp1251 -*-
# Flat file viever-correcter
import os
import wx
import wx.lib
import matplotlib

matplotlib.use("WXAgg")
matplotlib.interactive(False)
from pylab import *
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.backends.backend_wx import _load_bitmap
from ff_utils3 import *
import numpy as N

c_all = True
nT2min = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
nT2min0 = 0.203


##font = { 'fontname':'Times New Roman', 'fontsize':16 }
# -----------------------------------
class Tlocator(Locator):
    tmin = 0.0
    tmax = 0.0
    dd = 0.0

    def __call__(self):
        global markr, pp
        self.tmin, self.tmax = self.axis.get_view_interval()
        N = 86400 * (self.tmax - self.tmin) / Sampleperiods[0]
        #         print 'N', N, markr
        if N < 200 and markr == ' ':
            markr = 'o'
            for i in range(Nplot):  pp[i].set_marker('o')
            print('set x', 86400 * (self.tmax - self.tmin) / Sampleperiods[0])
        if N >= 200 and markr == 'o':
            markr = ' '
            for i in range(Nplot):  pp[i].set_marker(' ')
            print('set None', 86400 * (self.tmax - self.tmin) / Sampleperiods[0])
        d0 = floor(self.tmin)
        self.dd = self.tmax - self.tmin
        if self.dd > 30:
            lab = frange(d0, self.tmax, 5)
        if 30 >= self.dd > 5:
            lab = frange(d0, self.tmax, 2)
        if 5 >= self.dd > 1:
            lab = frange(d0, self.tmax, 1)
        ax.xaxis.set_minor_locator(MultipleLocator(1. / 4.))
        if 1 >= self.dd > 0.5:
            d0 = floor(12 * self.tmin) / 12
            lab = frange(d0, self.tmax, 0.5)
            ax.xaxis.set_minor_locator(MultipleLocator(1. / 12.))
        if 0.5 >= self.dd > 4. / 24.:
            d0 = floor(24 * self.tmin) / 24
            lab = frange(d0, self.tmax, 2.0 / 24.0)
            ax.xaxis.set_minor_locator(MultipleLocator(1. / 24.))
        if 4. / 24.0 >= self.dd:  # >1./6.:
            d0 = floor(240 * self.tmin) / 240
            lab = frange(d0, self.tmax, 1. / 24.0)
            ax.xaxis.set_minor_locator(MultipleLocator(1. / 24.))
        #         print 'Locator',self.tmin,self.tmax,self.dd
        ##         ch=gca().axes.get_children()
        ##         for c in ch:
        ##           if `c`.find('Line2D')>0:
        ##               break
        ##         print `c`
        ##         print c.get_linestyle()
        ##         c.set_linestyle('.')
        #         print lab
        return lab


# ----------------------------------
def timeformatter(mjd, unused):
    s = mjd2str(mjd)
    #         print 'Formatter',locator.tmin,locator.tmax,locator.dd
    if locator.dd > 3:
        sf = s[5:10]
    if 3 >= locator.dd > 1:
        sf = s[8:16]
    if 1 >= locator.dd > 6.0 / 24.:
        sf = s[11:19]
    if 6.0 / 24 >= locator.dd:  # >6.0/24.:
        sf = s[11:19]
    ##         if  15>dd>5:
    ##         if  5>dd>1:
    #         print s,sf
    return sf


# ----------------------------------
def frange(s, e=None, S=None):
    if e == None: e = s;s = 0.0
    if S == None: S = 1.0
    L = [];
    n = s
    if e > s:
        while n < e: L.append(n);n += S
    elif e < s:
        while n > e: L.append(n);n -= S
    return L


# --------------------------------------
def click(event):
    global kp, x1, x2, y1, y2, sbox, x, y, p1, npp, npy, ch, corrected
    if event.name == 'button_press_event':
        #      npy=2-(int(3*event.y/(fig.get_dpi()*fig.get_size_inches()[1])))
        npy = Nplot - 1 - (int(Nplot * event.y / (fig.get_dpi() * fig.get_size_inches()[1])))
        npp = npy
        ni = x.searchsorted(event.xdata)
        #      print ni, npp,
        vs = '%6.2f' % (y[ni][npp] * nT2min[npp])
        print(mjd2str(x[ni]), '     ', vs)  # print current value

        label.SetLabel(mjd2str(x[ni]) + '   ' + vs)
        fig.canvas.set_window_title(mjd2str(x[ni]))
        if event.button == 1 and event.inaxes and tb.mode == '':
            x1, y1 = event.xdata, event.ydata
            x2, y2 = x1, y1
            sbox, = sp[npp].plot([x1, x1, x2, x2, x1], [y1, y2, y2, y1, y1])
            kp = True

    if event.name == 'button_release_event' and kp:  # erase box
        if onShift:
            n1 = -1;
            n2 = -1;
            for i in range(len(x)):
                if x1 < x[i] < x2 and (y1 < y[i, npy] < y2 or y2 < y[i, npy] < y1):
                    y[i, npy] = N.NaN
                    if c_all:
                        for k in range(Nplot):
                            y[i, k] = N.NaN
                    ni = x.searchsorted(x[i])
                    corrected.add(ni)
            iscorrected = True
        #        print ni
        kp = False
        axe = sbox.axes
        sbox.remove()
        ch = axe.get_children()
        for c in ch:
            ######           if `c`.find('Line2D')>0:
            break
        c.set_data([x, y[:, npy]])
        draw()

    if kp and event.name == 'motion_notify_event':
        x2, y2 = event.xdata, event.ydata
        sbox.set_data([[x1, x1, x2, x2, x1], [y1, y2, y2, y1, y1]])
        draw()


##   draw()

def OnSaveClick(event):
    wx.Bell()
    print('Save', a)


# ----------------------------------------
def on_key(event):
    global onShift

    #      gca().axis().relim()
    #      gca().axis().autoscale_view(True,True,True)

    if event.key == u'shift':
        onShift = True
    if event.key == 'r':  # rescale
        s = gca().axis()
        ns = N.where((x >= s[0]) & (x <= s[1]))
        npy = Nplot - 1 - (int(Nplot * event.y / (fig.get_dpi() * fig.get_size_inches()[1])))

        amin = N.nanmin(y[ns, npy])
        amax = N.nanmax(y[ns, npy])
    #          s[2]=amin
    #          s[3]=amax
    if event.key == 'm':
        nT2min[1] = nT2min0
        pass
    if event.key == 'n':
        nT2min[1] = 1
        pass
    if event.key == 'w':  # write point to file
        wx.Bell()
        ftxt = open(fin[:-3] + 'txt', 'a')
        ni = x.searchsorted(event.xdata)
        print >> ftxt, mjd2str(x[ni])[:-3],
        for i in range(Nplot):
            print >> ftxt, '%6.2f' % (y[ni][i]),
        print >> ftxt, ''
        ftxt.close()


# ---------------------------
def re_key(event):
    global onShift
    if event.key == u'shift':
        onShift = False


##def tb_custom_pan_left(event):
##    print '!!'
# ------------------------------------
def savecor(event):
    global corrected, iscorrected
    wx.Bell()
    #    for tlw in wx.GetTopLevelWindows():
    #       tlw.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
    ncor = list(corrected);
    ncor.sort()
    for n in ncor:
        updateff1(0, n, y[n])
    corrected = set()
    iscorrected = False
    ffd[0].flush()


#    for tlw in wx.GetTopLevelWindows():
#         tlw.SetCursor(wx.StockCursor(wx.CURSOR_NORMAL))


# ========================================================================
markr = ' '
DATADIR = 'd:\\CMVS_DAT\\Nadym\\'  # only for raw data
Eps = [1.0, 1.0, 1.0, 1.0]
params0 = {'figure.figsize': [15, 7],
           'figure.subplot.left': 0.05,
           'figure.subplot.right': 0.99,
           'figure.subplot.top': 0.99,
           'figure.subplot.bottom': 0.03,
           'figure.subplot.wspace': 0.0001,
           'lines.marker': 'None'
           }
rcParams.update(params0)
fig = figure()
# fig.get_size_inches()[1]*fig.get_dpi()
w0 = wx.GetTopLevelWindows()
label = wx.StaticText(w0[0], -1, label='label', pos=(500, fig.get_size_inches()[1] * fig.get_dpi() + 10), name='label1')
label.SetBackgroundColour("yellow")
font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
label.SetFont(font)

# label=wx.StaticText(w0[0], -1, label='СОХРАНИТЬ', pos=(300,fig.get_size_inches()[1]*fig.get_dpi()+10), name='label1')
# Label=wx.panels
# label1=wx.Panel(w0[0], -1, pos=(300,fig.get_size_inches()[1]*fig.get_dpi()+10), name='label1')
# wx.EVT_LEFT_DOWN(label1, OnSaveClick)

# label1.Bind(wx.EVT_LEFT_UP,OnSaveClick)
# label1=wx.HyperlinkCtrl(w0[0], -1, label='Save',url='', pos=(400,fig.get_size_inches()[1]*fig.get_dpi()-100), name='label1')
# label1.AutoBrowse=False
# label1.Disable()
# print (label1.IsEnabled())
# label1.Bind(wx.EVT_HYPERLINK,OnSaveClick)

if len(sys.argv) > 1:
    fin = sys.argv[1]
else:
    fin = wx.FileSelector('Выберите файл', '', '*.*', '')

if len(fin) > 1:
    COD = fin[:4]
    if fin[-3:-1] == 'ff':  # FF file
        FT = 'F'
        ok = openrff(0, fin, False)
        if ok < 0:
            fin = wx.FileSelector('Выберите файл', '', '*.ffh', '')
            ok = openrff(0, fin, True)
        x, y, vmin, vmax = readffa(0)

    else:
        try:
            inif = open(DATADIR + COD + '_cmvspar.txt')
            sini = inif.readlines()[1].split()
            Eps[0] = float(sini[0]);
            Eps[1] = float(sini[1]);
            Eps[2] = float(sini[2])
        except:
            #            wx.MessageBox(DATADIR+COD+r'_cmvspar.txt не найден, мВ показаны', 'Info', wx.OK | wx.ICON_INFORMATION)
            pass

        Ncols[0] = 4
        Cods = [['Time', 'H', 'D', 'Z', 'Grad'], ['Time', 'H', 'D', 'Z', 'Grad']]
        Nrows[0] = os.stat(fin).st_size / (4 * Ncols[0] + 4)
        ffd[0] = open(fin, 'rb')
        if fin[-2:-1] == 'm': Sampleperiods[0] = 60
        if fin[-2:-1] == 's': Sampleperiods[0] = 1
        x, y, vmin, vmax = readffa(0)
        ffd[0].close()
        x = x + 15018
        y[:, 0] = Eps[0] * y[:, 0];
        y[:, 1] = Eps[1] * y[:, 1];
        y[:, 2] = Eps[2] * y[:, 2]  # raw data

if len(fin) <= 1:
    sys.exit()

if len(sys.argv) > 2:
    t0_f = sys.argv[2]
    print(t0_f)
if len(sys.argv) > 3:
    t0_t = sys.argv[3]
    print(t0_t)
if len(sys.argv) > 4:
    scol0 = sys.argv[4]
    print(scol0)

# x,y,vmin,vmax=readffa(0)
corrected = set()
iscorrected = False
font = {'fontname': 'Times New Roman', 'fontsize': 16}
x1 = -99999.9;
y1 = 0.0;
x2 = 0.0;
y2 = 0.0;
npp = 0;
npy = 0
ch = ''

kp = False
onShift = False

pp = [];
sp = []
tb = get_current_fig_manager().toolbar
tb.DeleteToolByPos(6)
tb.DeleteToolByPos(2)

ON_CUSTOM = wx.NewId()
# tb.AddSimpleTool(ON_CUSTOM,wx.Image('C:\\bin\\filesave.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Сохранить файл', 'Сохранить исправления')
tb.AddTool(ON_CUSTOM, 'der batton', wx.Image('C:\\bin\\filesave.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
           'Сохранить файл')
####wx.EVT_TOOL(tb,ON_CUSTOM, savecor)
# wx.EvtHandler.Bind(ON_CUSTOM, savecor, tb) # что не так с этой строчкой?
# Bind(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY)¶

# vfield= wx.StaticText(tb, -1, "Text Here")
# tb.AddSimpleTool(ON_CUSTOM,vfield)

tb.Realize()

locator = Tlocator()
formatter = FuncFormatter(timeformatter)

Nplot = N.size(y[0])
if Ncols[0] == 1: Nplot = 1
for Npl in range(Nplot):
    if Npl == 0: sp.append(subplot(Nplot, 1, Npl + 1))
    if Npl > 0: sp.append(subplot(Nplot, 1, Npl + 1, sharex=sp[0]))
    #     if len(N.shape(y))>1:
    #     matplotlib.pyplot.autoscale(enable=True, axis='y', tight=None)

    ymin = N.nanmin(y[:, Npl])
    #    ymin=N.nanmin(y[:])
    ymax = N.nanmax(y[:, Npl])
    #    ymax=N.nanmax(y[:])
    if N.isfinite(ymin):
        axis([1.01 * x[0] - 0.01 * x[-1], 1.01 * x[-1] - 0.01 * x[0], 1.1 * ymin - 0.1 * ymax, 1.1 * ymax - 0.1 * ymin])
        ylabel(Cods[0][Npl + 1])
        #         if Nplot>1:
        p, = sp[Npl].plot(x, y[:, Npl])
        #         else:
        #         p,=sp[Npl].plot(x,y[:])
        gca().xaxis.grid(True)
    ##     else:
    ##          ymin=N.nanmin(y[:])
    ##          ymax=N.nanmax(y[:])
    ##          if  N.isfinite(ymin):
    ##              axis([1.01*x[0]-0.01*x[-1],1.01*x[-1]-0.01*x[0],1.1*ymin-0.1*ymax,1.1*ymax-0.1*ymin])
    ##              p,=sp[Npl].plot(x,y[:])
    pp.append(p)

##sp.append(subplot(311))
##ymin=N.nanmin(y[:,0])
##ymax=N.nanmax(y[:,0])
##if  N.isfinite(ymin):
##    axis([1.01*x[0]-0.01*x[-1],1.01*x[-1]-0.01*x[0],1.1*ymin-0.1*ymax,1.1*ymax-0.1*ymin])
##    p,=sp[0].plot(x,y[:,0])
##    pp.append(p)
##
##
##sp.append(subplot(3,1,2,sharex=sp[0]))
##ymin=N.nanmin(y[:,1])
##ymax=N.nanmax(y[:,1])
##if  N.isfinite(ymin):
##    axis([1.01*x[0]-0.01*x[-1],1.01*x[-1]-0.01*x[0],\
##    1.1*ymin-0.1*ymax,1.1*ymax-0.1*ymin])
##    p,=sp[1].plot(x,y[:,1])
##    pp.append(p)
##
##sp.append(subplot(3,1,3,sharex=sp[0]))
##ymin=N.nanmin(y[:,2])
##ymax=N.nanmax(y[:,2])
##if N.isfinite(ymin):
##    axis([1.01*x[0]-0.01*x[-1],1.01*x[-1]-0.01*x[0],\
##    1.1*ymin-0.1*ymax,1.1*ymax-0.1*ymin])
##    p,=sp[2].plot(x,y[:,2])
##    pp.append(p)

connect('button_press_event', click)
connect('button_release_event', click)
connect('motion_notify_event', click)
connect('key_press_event', on_key)
connect('key_release_event', re_key)

ax = gca()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

draw()
fig.canvas.set_window_title(fin)
show()

print('*****')
