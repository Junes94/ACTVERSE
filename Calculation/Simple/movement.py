import numpy as np

def movement(dataframe):
    # try:
    #     #     (type(coi) == list) & (type(foi) == list)
    #     # except KeyError(key):
    #     #     print('Columns and frames of interest must be a list')
    #     # wanted to check whether the coi and foi where list beforehand; does not print; instead raised KeyError, but cannot catch that either


    # Come to think of it, user can just use a slice of dataframe as input and not go through this shithole.
    # = unnecessary.
    # if coi is None:
    #     coi = ['Bodycenter_x', 'Bodycenter_y', 'Bodycenter_z']
    # if foi is None:
    #     workingframe = dataframe.loc[:, coi]
    # else:
    #     workingframe = dataframe.loc[foi, coi]

    workingframe = dataframe.loc
    difference = np.diff(workingframe,axis=0)
    # squared = np.square(difference)
    # sumofsquared = np.sum(squared,axis=1)
    # distance = math.sqrt(sumofsquared)
    distance = np.sqrt(np.sum(np.square(difference),axis=1))
    return distance
