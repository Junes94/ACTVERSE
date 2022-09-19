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

