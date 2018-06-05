import pickle
import os

class CacheData(object):

    DATA_DIRECTORY_PATH = "../data/"

    def __init__(self):
        pass

    def save(self, data, ticker, tag):
        if not os.path.exists(self.DATA_DIRECTORY_PATH):
            os.makedirs(self.DATA_DIRECTORY_PATH)
        outfile = open(self.filename(ticker, tag), "wb")
        pickle.dump(data, outfile)
        outfile.close()

    def open(self, ticker, tag):
        infile = open(self.filename(ticker, tag), "rb")
        data = pickle.load(infile)
        infile.close()
        return data

    def filename(self, ticker, tag):
        return self.DATA_DIRECTORY_PATH + ticker + tag


