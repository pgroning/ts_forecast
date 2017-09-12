from pdb import set_trace

import pandas as pd


def read_csv():
    df = pd.DataFrame()
    df['var1'] = [x for x in range(10)]
    #df['var2'] = [x for x in range(50, 60)]
    return df

def ts_shift(data, n_in=1, n_out=1, dropnan=True):
    n_vars = data.shape[1]
    df = pd.DataFrame(data)

    cols = []
    header = []
    # input sequence (t-n, ... , t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        for j in range(n_vars):
            header.append('var{:d}(t-{:d})'.format(j + 1, i))

    # forecast sequence (t, t+1, ... , t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        for j in range(n_vars):
            if i == 0:
                header.append('var{:d}(t)'.format(j + 1))
            else:
                header.append('var{:d}(t+{:d})'.format(j + 1, i))

    agg = pd.concat(cols, axis=1)
    agg.columns = header
    # drop rows containing NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg

def main():
    df = read_csv()
    ts = df.values  # numpy array
    n_in = 1
    n_out = 2
    df2 = ts_shift(ts, n_in, n_out)
    #df2 = ts_shift(ts)
    print(df2)

if __name__ == "__main__":
    main()
