from pdb import set_trace

import sys
import os
import pandas as pd
import numpy as np

# Expected columns in the indata csv file are:
#  1. [Delivery date]
#  2. [Confirmed date]
#  3. [Order id]
#  4. [DeliveryAddressId]
#  5. [Delivery fee inc vat]
#  6. [Total discount value inc vat]
#  7. [memberid]
#  8. [Product id]
#  9. [Quantity]
# 10. [Procurement price]
# 11. [Price paid inc vat]
# 12. [Delivery address postalcode]

# Prodid examples
# prodid = 55482   # Entrecote i Bit ca 800g Scan
# prodid = 8200    # Fullkornsris 1kg Uncle Bens
# prodid = 2602    # Banan EKO Klass 1
# prodid = 78452   # Mellanmjölk 1.5% 1L Arla
# prodid = 15664   # Mellanmjölk 1.5% 1.5L Arla
# prodid = 16833   # Inlagd Sill 500g Abba
# prodid = 121612  # Signalkräftor Färska Svenska 500g Smålandskräftan


class UniqueDates(object):
    """Reads a .csv file and finds the unique dates.
    Stores the resulting dataframe to another .csv file."""

    def __init__(self, ifile=None, prodid=None):
        if ifile is None:
            print("Error: ifile must be given.")
            return
        else:
            self.ifile = ifile
        if prodid is None:
            print("Error: prodid must be given.")
            return
        else:
            self.prodid = prodid

    def read_csv(self):
        print("Reading " + self.ifile)
        # Read columns 1, 3, 8, 9
        self.df = pd.read_csv(self.ifile, header=None, nrows=None,
                              usecols=[0, 2, 7, 8],
                              names=['delivery_date', 'orderid',
                                     'prodid', 'quantity'])

    def sum_columns(self):
        print("Finding unique dates...")
        # Find all unique dates in sorted order
        date_array = np.unique(self.df['delivery_date'].values)

        # Setup an empty dataframe to store results
        cols = ['delivery_date', 'num_of_orders', 'num_of_orderlines',
                'prodid_quantity', 'prodid_orderlines']
        self.df_out = pd.DataFrame(columns=cols)

        for i, date in enumerate(date_array):
            print("processing : " + date)
            # Find indicies that corresponds to specific date
            idates = np.where(self.df['delivery_date'].values == date)[0]
            num_of_orderlines = len(idates)

            # Find unique orders for specific date
            order_array = np.unique(self.df['orderid'].values[idates])
            # Number of orders for specific date
            num_of_orders = len(order_array)

            # Find indicies of specific prodid
            iprodid = np.where(self.df['prodid'].values[idates] == self.prodid)[0]
            prodid_orderlines = len(iprodid)
            quantity_array = self.df['quantity'].values[idates][iprodid]
            prodid_quantity = np.sum(quantity_array)

            # Append result to dataframe
            self.df_out.loc[len(self.df_out)] = [date, num_of_orders,
                                                 num_of_orderlines,
                                                 prodid_quantity,
                                                 prodid_orderlines]
            #if i > 20:
            #    break

    def write_csv(self):
        path = os.path.dirname(self.ifile)
        ofile = os.path.join(path, "prodid-" + str(self.prodid) + ".csv")

        # Format dates before saving dataframe to file
        self.df_out['delivery_date'] = pd.to_datetime(self.df_out.delivery_date)

        self.df_out.to_csv(ofile, index=False, date_format='%Y-%m-%d')
        print("Saved to file " + ofile)


def unique_dates():
    if len(sys.argv) > 2:
        ifile = sys.argv[1]
        prodid = int(sys.argv[2])
    else:
        print("Error: Too few input arguments are given.")
        return

    if not (os.path.exists(ifile)):
        print("Error: File was not found.")
        return

    ud = UniqueDates(ifile, prodid)
    ud.read_csv()
    ud.sum_columns()
    ud.write_csv()


if __name__ == "__main__":
    unique_dates()

