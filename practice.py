import math
import numpy as np
import pandas
from itertools import product
import matplotlib.pyplot as plt
import seaborn as sns

def avatarcsvloader(pathrest, filename, givenpath ='C:/Users/endyd/OneDrive/문서/ACTVERSE/AVATAR_DATA_SET-20220913T084458Z-001/AVATAR_DATA_SET/'):
    fullname = givenpath+pathrest+filename+'.csv'
    # columnames = ['Nose_x', 'Nose_y', 'Nose_z', 'Head_x', 'Head_y', 'Head_z', 'Anus_x', 'Anus_y', 'Anus_z', 'Body_x', 'Body_y', 'Body_z', 'Leftfoot_x',
    #               'Leftfoot_y', 'Leftfoot_z', 'RightFoot_x', 'RightFoot_y', 'RightFoot_z', 'Lefthand_x', 'Lefthand_y', 'Lefthand_z', 'Righthand_x',
    #               'Righthand_y', 'Righthand_z', 'Tail_x', 'Tail_y', 'Tail_z']

    # testfile = pandas.read_csv('C:/Users/endyd/OneDrive/문서/ACTVERSE/AVATAR_DATA_SET-20220913T084458Z-001/AVATAR_DATA_SET/1.OFT(WT-N=50)/raw/H1.mat.csv_new.csv')
    # 1코 2머리 3항문 4몸통 5왼발 6오른발 7왼손 8오른손 9꼬리
    # xyz 순

    coord = ['_x', '_y', '_z']
    bodypart = ['Nose', 'Head', 'Anus', 'Bodycenter', 'RightFoot', 'LeftFoot', 'Righthand', 'Lefthand', 'Tailtip']
    testlist = list(product(bodypart, coord))
    columnames = [''.join(words) for words in testlist]
    output = pandas.read_csv(fullname, names=columnames)

    try:
        27 == output.shape[1]
    except:
        print('The number of columns are not 27; Check the data')
    else:
        return output

# functions to try
# V body center movement & Total movement(to use for freezing analysis)
# head angle
# V Total body length (exploration stretched posture)

def bodylength(dataframe):
    workingframe = dataframe.loc[:,['Nose_x','Anus_x','Nose_y','Anus_y','Nose_z','Anus_z']]
    length = np.sqrt(((workingframe.iloc[:,0]-workingframe.iloc[:,1])**2 + (workingframe.iloc[:,2]-workingframe.iloc[:,3])**2 + (workingframe.iloc[:,4]-workingframe.iloc[:,5])**2))
    return length


def movement(dataframe, coi=None, foi=None):
    # try:
    #     #     (type(coi) == list) & (type(foi) == list)
    #     # except KeyError(key):
    #     #     print('Columns and frames of interest must be a list')
    #     # wanted to check whether the coi and foi where list beforehand; does not print; instead raised KeyError, but cannot catch that either
    if coi is None:
        coi = ['Bodycenter_x', 'Bodycenter_y', 'Bodycenter_z']
    if foi is None:
        workingframe = dataframe.loc[:, coi]
    else:
        workingframe = dataframe.loc[foi, coi]
    # workingframe = dataframe.loc[:, coi]
    difference = np.diff(workingframe,axis=0)
    # squared = np.square(difference)
    # sumofsquared = np.sum(squared,axis=1)
    # distance = math.sqrt(sumofsquared)
    distance = np.sqrt(np.sum(np.square(difference),axis=1))
    return distance

# def angle(dataframe):

testfile = avatarcsvloader('1.OFT(WT-N=50)/raw/','H1.mat.csv_new')
testlength = bodylength(testfile)
testtotalmovement = movement(testfile)
testbodymovement = movement(testfile,coi=['Bodycenter_x','Bodycenter_y','Bodycenter_z'])

fig, axs = plt.subplots(3)
axs[0].plot(testlength)
axs[0].set_title('Body Length')
axs[1].plot(testtotalmovement)
axs[1].set_title('Total movement (bases for freezing analysis)')
axs[2].plot(testbodymovement)
axs[2].set_title('Body center movement (bases for speed analysis)')