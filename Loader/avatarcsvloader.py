import pandas
from itertools import product

def avatarcsvloader(path, filename):
    """
    Function that loads csv files from AVATAR system.
    Bodypart name - 'Nose', 'Head', 'Anus', 'Bodycenter', 'RightFoot', 'LeftFoot', 'Righthand', 'Lefthand', 'Tailtip'
    dimensions - x, y, z
    Importing file must have 27 columns.

    :param path: path
    :param filename: filename excluding extention
    :return: Pandas dataframe
    """

    fullname = path+filename+'.csv'
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
   # import tkinter
    # from tkinter import filedialog
    #
    # tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
    #
    # folder_path = filedialog.askdirectory()

# # import module
# import pandas as pd
#
# # assign dataset names
# list_of_names = ['crime', 'username']
#
# # create empty list
# dataframes_list = []
#
# # append datasets into the list
# for i in range(len(list_of_names)):
#     temp_df = pd.read_csv("./csv/" + list_of_names[i] + ".csv")
#     dataframes_list.append(temp_df)