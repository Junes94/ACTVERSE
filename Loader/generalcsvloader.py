import pandas as pd
from itertools import product

def generalcsvloader(path,filename,ndims,trackingpoints,customcolnames=None):
    """
    Function that can load csv from sources other than AVATAR system.
    ex)

    :param path: file path
    :param filename: file name excluding extension
    :param ndims: number of dimensions measured. integer 0 ~ 2
    :param trackingpoints: number of tracked bodyparts. positive integer
    :param customcolnames: can specify column names
    :return: pandas dataframe
    """
    fullname = path + filename + '.csv'
    coordnames = ['_x', '_y', '_z']
    points = [str(i) for i in range(0,trackingpoints)]

    if customcolnames is None:
        coord = coordnames[0:ndims]
        testlist = list(product(points, coord))
        columnames = [''.join(words) for words in testlist]
    else:
        columnames = customcolnames

    output = pd.read_csv(fullname,names=columnames)
    # import tkinter
    # from tkinter import filedialog
    #
    # tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
    #
    # folder_path = filedialog.askdirectory()


    return output