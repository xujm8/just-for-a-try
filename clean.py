import numpy as np
import os, csv
import argparse
from collections import Counter

def clean(datadir, newdatadir):
    path = os.getcwd()
    datadir = '/' + args.datadir + '/'
    newdatadir = '/' + args.newdatadir + '/'  # target path

    newdatapath = path + newdatadir
    datapath = path + datadir
    codelist = os.listdir(datapath)  # codelist get

    if not os.path.exists(datapath):
        print('Find error')

    if not os.path.exists(newdatapath):
        os.mkdir(newdatapath)  # create the dir if you don't have it

    newCodelistlen = []
    for code in codelist:
        with open(datapath + code, 'r') as f:
            readers = csv.reader(f)
            rows = [row for row in readers]
            newCodelistlen.append(len(rows))
            f.close()
    countMeg = dict(Counter(newCodelistlen))
    Maxrowlen = sorted(countMeg.items(), key=lambda item: item[1], reverse=True)[0][
        0]  # find the len which has appear  more

    for code in codelist:
        with open(datapath + code, 'r') as f:
            readers = csv.reader(f)
            rows = [row for row in readers]
            if len(rows) == Maxrowlen:
                with open(newdatapath + code, 'w') as ff:
                    writer = csv.writer(ff)
                    writer.writerows(rows)
                    ff.close()
            f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='csvClearner(this function) will clean the data in 5min')
    parser.add_argument(dest='datadir', metavar='datadir', type=str, nargs='?',
                        help='the source data dir name(dafault == 5min)', default='5min')
    parser.add_argument(dest='newdatadir', metavar='newdaradir', type=str, nargs='?',
                        help='the target data dir name(dafault == new5min)', default='new5min')
    args = parser.parse_args()
    clean(args.datadir, args.newdatadir)
