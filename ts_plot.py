from pdb import set_trace

import pandas as pd
import matplotlib.pylab as plt
import numpy as np


class ts_plot(object):
    def __init__(self, csvfile, prodid=None):
        self.infile = csvfile
        self.prodid = prodid
        self.read_csv(csvfile)

    def read_csv(self, csvfile):
        # Read data from csv file
        self.df = pd.read_csv(csvfile, nrows=None)
        self.df['delivery_date'] = pd.to_datetime(self.df.delivery_date.values)
        self.df = self.df.set_index(['delivery_date'])
        #set_trace()

    def resample(self, freq='W-MON'):
        print("resample data")

        df_w = pd.DataFrame()
        df_w['num_of_orders'] = self.df.num_of_orders.resample(freq).sum()
        df_w['num_of_orderlines'] = self.df.num_of_orderlines.resample(freq).sum()
        df_w['prodid_quantity'] = self.df.prodid_quantity.resample(freq).sum()
        df_w['prodid_orderlines'] = self.df.prodid_orderlines.resample(freq).sum()
        self.df = df_w

    def plot_quantity(self):
        x = self.df.index.values
        #x = self.df.delivery_date.values
        y = self.df.prodid_quantity.values
        #set_trace()
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        plt.plot(x, y)
        ax1.set_xlabel('Date')
        ax1.set_ylabel('quantity')
        plt.grid()
        if self.prodid is not None:
            ax1.set_title('prodid=' + str(self.prodid))

        ax2 = fig.add_subplot(212)
        y2 = y / self.df.num_of_orders.values
        plt.plot(x, y2)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('quantity / num_of_orders')
        plt.grid()
        plt.show()

def plot_y1y2(df):

    x = pd.to_datetime(df.delivery_date.values)
    y1 = df.prodid_quantity.values / df.num_of_orders.values
    y2 = df.prodid_quantity.values / df.num_of_orderlines.values

    plt.plot(x, y1)
    k = np.mean(df.num_of_orderlines.values) / np.mean(df.num_of_orders.values)
    plt.plot(x, y2*k)
    plt.show()

    print("sigma(y1) =", np.std(y1))
    print("sigma(y2*k) =", np.std(y2*k))


def main():
    #csvfile = "/media/pergro/DATA/Data/Myfiles/pocal/new_files/prodid-55482.csv"  # Entrecote i Bit ca 800g Scan
    #csvfile = "/media/pergro/DATA/Data/Myfiles/pocal/new_files/prodid-8200.csv"  # Fullkornsris 1kg Uncle Bens
    #csvfile = "/media/pergro/DATA/Data/Myfiles/pocal/new_files/prodid-2602.csv"   # Banan EKO Klass 1
    csvfile = "/media/pergro/DATA/Data/Myfiles/pocal/new_files/prodid-78452.csv"  # Mellanmjölk 1.5% 1L Arla
    #csvfile = "/media/pergro/DATA/Data/Myfiles/pocal/new_files/prodid-15664.csv"  # Mellanmjölk 1.5% 1.5L Arla
    #csvfile = "/media/pergro/DATA/Data/Myfiles/pocal/new_files/prodid-16833.csv"  # inlagd sill
    #csvfile = "/media/pergro/DATA/Data/Myfiles/pocal/new_files/prodid-121612.csv"  # Signalkräftor Färska Svenska 500g Smålandskräftan
    prodid = None

    ts = ts_plot(csvfile, prodid)
    ts.resample('w')
    ts.plot_quantity()


if __name__ == "__main__":
    main()
