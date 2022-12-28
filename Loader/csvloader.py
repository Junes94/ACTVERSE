import pandas
from itertools import product

def avatarcsvloader(filename):
    """
    Function that loads csv files from AVATAR system.
    Bodypart name - 'Nose', 'Head', 'Anus', 'Bodycenter', 'RightFoot', 'LeftFoot', 'Righthand', 'Lefthand', 'Tailtip'
    dimensions - x, y, z
    Importing file must have 27 columns.

    :param path: path
    :param filename: filename excluding extention
    :return: Pandas dataframe
    """

    fullname = filename

    coord = ['_x', '_y', '_z']
    bodypart = ['Nose', 'Head', 'Anus', 'Bodycenter', 'RightFoot', 'LeftFoot', 'Righthand', 'Lefthand', 'Tailtip']
    testlist = list(product(bodypart, coord))
    columnames = [''.join(words) for words in testlist]
    output = pandas.read_csv(fullname, names=columnames)

    try:
        27 == output.shape[1]
    except:
        print('The number of columns are not 27; Check the data_pre')
    else:
        return output

def generalcsvloader(filename, ndims=3, trackingpoints=9, customcolnames=None):
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
    fullname = filename
    coordnames = ['_x', '_y', '_z']
    points = [str(i) for i in range(0, trackingpoints)]

    if customcolnames is None:
        coord = coordnames[0:ndims]
        testlist = list(product(points, coord))
        columnames = [''.join(words) for words in testlist]
    else:
        columnames = customcolnames

    output = pandas.read_csv(fullname, names=columnames)
    return output
