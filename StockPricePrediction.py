import matplotlib

#'Google': 'goog',
    #'Apple': 'aapl',
    #'Yahoo': 'yhoo',
    #'HP': 'hpq',
    #'Facebook': 'fb',
    #'Amazon': 'amzn',
    #'Twitter': 'twtr'

import tkMessageBox
import sys
from tkinter import *
matplotlib.use("TkAgg")
import datetime
import urllib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy




try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk



f = Figure(figsize=(10, 10), dpi=100)
a = f.add_subplot(111)
sixMonthAgo = datetime.date.today() - datetime.timedelta(6 * 365 / 12)

# Default values



class Quote(object):
    DATE_FMT = '%Y-%m-%d'
    TIME_FMT = '%H:%M:%S'

    def __init__(self):
        self.symbol = ''
        self.date, self.time, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(7))

    def append(self, dt, open_, high, low, close, volume):
        self.date.append(dt.date())
        self.time.append(dt.time())
        self.open_.append(float(open_))
        self.high.append(float(high))
        self.low.append(float(low))
        self.close.append(float(close))
        self.volume.append(int(volume))

    def to_csv(self):
        return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
                                                                                   self.date[bar].strftime('%Y-%m-%d'),
                                                                                   self.time[bar].strftime('%H:%M:%S'),
                                                                                   self.open_[bar], self.high[bar],
                                                                                   self.low[bar], self.close[bar],
                                                                                   self.volume[bar])
                        for bar in xrange(len(self.close))])

    def write_csv(self, filename):
        with open(filename, 'w') as f:
            f.write(self.to_csv())

    def read_csv(self, filename):
        self.symbol = ''
        self.date, self.time, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(7))
        for line in open(filename, 'r'):
            symbol, ds, ts, open_, high, low, close, volume = line.rstrip().split(',')
            self.symbol = symbol
            dt = datetime.datetime.strptime(ds + ' ' + ts, self.DATE_FMT + ' ' + self.TIME_FMT)
            self.append(dt, open_, high, low, close, volume)
        return True

    def __repr__(self):
        return self.to_csv()


class Yahoo(Quote):
    ''' Daily quotes from Yahoo. Date format='yyyy-mm-dd' '''

    def __init__(self, symbol, start_date, end_date=datetime.date.today().isoformat()):
        super(Yahoo, self).__init__()
        self.symbol = symbol.upper()
        start_year, start_month, start_day = start_date.split('-')
        start_month = str(int(start_month) - 1)
        end_year, end_month, end_day = end_date.split('-')
        end_month = str(int(end_month) - 1)
        url_string = "http://ichart.finance.yahoo.com/table.csv?s={0}".format(symbol)
        url_string += "&a={0}&b={1}&c={2}".format(start_month, start_day, start_year)
        url_string += "&d={0}&e={1}&f={2}".format(end_month, end_day, end_year)
        csv = urllib.urlopen(url_string).readlines()
        csv.reverse()
        for bar in xrange(0, len(csv) - 1):
            ds, open_, high, low, close, volume, adjc = csv[bar].rstrip().split(',')
            open_, high, low, close, adjc = [float(x) for x in [open_, high, low, close, adjc]]
            if close != adjc:
                factor = adjc / close
                open_, high, low, close = [x * factor for x in [open_, high, low, close]]
            dt = datetime.datetime.strptime(ds, '%Y-%m-%d')
            self.append(dt, open_, high, low, close, volume)


class Gui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container, self.tk)

        self.frames[StartPage] = frame

        frame.grid()

        self.show_frame(StartPage)

    def show_frame(self, count):
        frame = self.frames[count]
        frame.tkraise()


def calculation_plots():
    q = Yahoo(str(code), str(sixMonthAgo))  # download six month ago data
    q.write_csv('db.csv')  # save it to disk

    pullData = open("db.csv", "r").read()  # read data
    dataList = pullData.split('\n')  # split data
    xList = []
    yList = []

    yReg = []

    plt.xlabel("Date")
    plt.ylabel("Value")

    for line in dataList:
        if len(line) > 1:
            obj = line.split(',')
            # print (obj)
            # [0:Name, 1: Date, 2: Time, 3: Open, 4: High, 5: Low, 6: Close, 7: Volume]
            y = float(obj[6])
            x = datetime.datetime.strptime(obj[1], "%Y-%m-%d")
            xList.append(x)
            yList.append(y)


            y = float(obj[len(obj)-2])

            yReg.append(y)





    size = len(xList)
    xnum = range(0,size)
    coefficients = numpy.polyfit(xnum, yReg, 1)

    polynomial = numpy.poly1d(coefficients)

    reg = polynomial(xnum)


###############
    regArr = []
    for i in reg:
        regArr.append(i)

    sum = regArr[len(reg) -1]- regArr[len(reg) -2]

    for i in range(totalD.days):
        regArr.append(sum + regArr[len(regArr) -1])

    xnum = range(0, size + totalD.days)

    #####################################
    newY = []
    newReg = []
    newDate = []
    for i in range(0, size , 10):
        newY.append(yList[i])
        newReg.append(reg[i])
        newDate.append(xList[i])

    ####################################

    plt.plot( newDate, newReg, 'r-', newDate, newY, 'o')

    #######################

    tkMessageBox.showwarning(code,"the price for the date: "+ str(enterday) +" is \n"+  str(regArr[len(regArr)-1]))

    ##########################

    plt.legend(['regression', 'original'])
    plt.show()






def mprint():
    global enterday
    global totalD
    global comp, code

    y = int(year.get())
    m = int(month.get())
    d = int(day.get())
    enterday = datetime.date(y, m, d)

    tday = datetime.date.today()

    totalD = enterday - tday
    code = ment.get()
    calculation_plots()





class StartPage(tk.Frame):

    def __init__(self, parent, controller):





        global ment
        global year
        global month
        global day

        year = StringVar()
        month = StringVar()
        day = StringVar()

        ment = StringVar()

        tk.Frame.__init__(self, parent)


        tk.Label(self, text="Enter Company:").grid(row=0)
        tk.Label(self, text="Enter Year:").grid(row=1)
        tk.Label(self, text="Enter Month:").grid(row=2)
        tk.Label(self, text="Enter day:").grid(row=3)

        Entry(self, textvariable=ment).grid(row=0, column=1)
        Entry(self, textvariable=year).grid(row=1, column=1)
        Entry(self, textvariable=month).grid(row=2, column=1)
        Entry(self, textvariable=day).grid(row=3, column=1)

        Button(self, text='OK', command=mprint).grid(row=4, column=1, sticky=N, pady=4)
        Button(self, text='Quit', command=self.quit).grid(row=4, column=0, sticky=N, pady=4)


















if __name__ == '__main__':
    # # Gui installation
    run = Gui()
    run.mainloop()



