import pandas as pd
from itertools import product

def generalcsvloader(pathrest,filename,ndims,trackingpoints,customcolnames=None):
    fullname = pathrest + filename + '.csv'
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