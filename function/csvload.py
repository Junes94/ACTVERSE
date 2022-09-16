import pandas as pd


def load(givenpath, pathrest, filename):
    """
    This function import AVATAR csv file as a DataFrame
    :param pathrest: folder outside the csv file
    :param filename: csv file name
    :param givenpath: the rest of the folder path
    :return:
    """
    fullname = givenpath + pathrest + filename + '.csv'

    # allocate each name of joint coordinate to column
    label_joint = ['nose', 'head', 'anus', 'tail', 'torso', 'LH', 'RH', 'LF', 'RF']
    label_xyz = ['_x', '_y', '_z']
    label_total = []
    for joint in label_joint:
        for xyz in label_xyz:
            label_total.append(joint + xyz)

    my_data = pd.read_csv(fullname, header=None, names=label_total)

    # name indices of DataFrame to frame numbers
    index = []
    for index_num in range(1, my_data.shape[0]+1):
        index.append(f'{index_num}')
    my_data.set_axis(index, axis='index', inplace=True)

    return my_data
