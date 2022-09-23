import numpy as np

def bodylength(dataframe):
    """
    Calculates the body length in the current frame;

    :param dataframe: must include columns with names 'Nose_x','Anus_x','Nose_y','Anus_y','Nose_z','Anus_z'
    :return: the body length of the animal in the current frame
    """
    workingframe = np.diff(dataframe.loc[:,['Nose_x','Anus_x','Nose_y','Anus_y','Nose_z','Anus_z']],axis=1)
    length = np.linalg.norm(workingframe[:,0::2],ord=2,axis=1)
    return length


def movement(dataframe):
    """
    Calculates the movement per frame;
    Can specify column names and calculate movement of certain body part;
    can input whole csv to findout freezing score

    :param dataframe: dataframe loaded by loader package
    :return: movement between frames
    """
    # try:
    #     #     (type(coi) == list) & (type(foi) == list)
    #     # except KeyError(key):
    #     #     print('Columns and frames of interest must be a list')
    #     # wanted to check whether the coi and foi where list beforehand; does not print; instead raised KeyError, but cannot catch that either


    workingframe = dataframe
    difference = np.diff(workingframe,axis=0)
    distance = np.linalg.norm(difference,axis=1)
    return distance
