import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class PlotData(object):

    plotindex = 0

    def __init__(self, nrows):
        self.nrows = nrows
        self.fig = plt.figure()
        self.grid = plt.GridSpec(self.nrows, 1, hspace=0.2, wspace=0.2)

    def plot(self, data, title, xlabel, ylabel):
        data.dropna()
        print "Data for %s" % (title)
        print data
        #print "PlotIndex is %d" % (self.plotindex)
        ax = self.fig.add_subplot(self.grid[self.plotindex:, 0:])
        ax.plot(data)

        #plt.subplot(self.nrows, self.ncol, self.plotindex)
        #plt.plot(data)
        #plt.legend(loc='best')
        self.plotindex += 1
        #plt.title(title)
        #plt.xlabel(xlabel)
        #plt.ylabel(ylabel)



    def show(self):
        plt.interactive(False)
        plt.show()