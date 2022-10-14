import numpy as np
import pandas as pd

def point2angleplane(df):
    """
    Function calculating the angles of two points, projected on each plane

    :param df: input dataframe. Number of columns must be 6(3d) or 4(2d). First 3 or 2 columns (depending on the # of dimensions) are treated as the origin
    :return: dataframe of the angles projected on each plane at each frame.

    """

    # previous idea was angle between two 3d vectors; the intention was calculating vector of ONE point, as another becomes origin.
    # therefore, subtract one frome another, and calculate 3 angles - respect to x / y / z axis
    # question: xy,xz,yz plain projection or relative to x / y / z axis? are they the same thing?

    # Align to origin
    halfpoint = int(df.shape[1]/2)
    reposit = df.iloc[:,halfpoint:]-df.iloc[:,0:halfpoint].values

    # Check for dimensions and calculate accordingly
    if halfpoint == 3:
        xy = np.arctan2(reposit.iloc[:, 0], reposit.iloc[:, 1])
        yz = np.arctan2(reposit.iloc[:, 1], reposit.iloc[:, 2])
        xz = np.arctan2(reposit.iloc[:, 0], reposit.iloc[:, 2])
        angle = pd.DataFrame(np.transpose(np.vstack([xy, yz,xz])),columns=['xy','yz','xz'])
    elif halfpoint == 2:
        xy = np.arctan2(reposit.iloc[:, 0], reposit.iloc[:, 1])
        angle = pd.DataFrame(xy,columns=['Angle'])
    else:
        print('check the size of dataframe')
        return

    return angle

def point2angleaxis(df):
    """
    Function calculating the angles of two points regarding each axis

    :param df: input dataframe. Number of columns must be 6(3d) or 4(2d). First 3 or 2 columns (depending on the # of dimensions) are treated as the origin
    :return: dataframe of the angles in regards to each axis.
    """
    # need debugging on situations where x / y / z value is out of range
    # Align to origin
    halfpoint = int(df.shape[1] / 2)
    reposit = df.iloc[:, halfpoint:] - df.iloc[:, 0:halfpoint].values

    # Check for dimensions and calculate accordingly
    if halfpoint == 3:
        x = np.arccos(reposit.iloc[:, 0])
        y = np.arccos(reposit.iloc[:, 1])
        z = np.arccos(reposit.iloc[:, 2])
        angle = pd.DataFrame(np.transpose(np.vstack([x, y, z])), columns=['x', 'y', 'z'])
    elif halfpoint == 2:
        x = np.arccos(reposit.iloc[:, 0])
        y = np.arccos(reposit.iloc[:, 1])
        angle = pd.DataFrame(np.transpose(np.vstack([x, y])), columns=['x', 'y'])
    else:
        print('check the size of dataframe')
        return

    return angle

def point2lineangle(df):
    """
    Function that calculates the angle between two lines, formed by 3 bodypars.
    The second body part is treated as the origin point(0,0 or 0,0,0)
    :param df: input dataframe. Number of columns must be 9(3d) or 6(2d). In-between columns will be treated as the origin
    :return: dataframe of the angles at each frame
    """

    # both vectors start from origin, so second bodypart must be fixed at origin

    # fix at origin
    thirdpoint = int(df.shape[1]/3)
    df1 = df.iloc[:,0:thirdpoint] - df.iloc[:,thirdpoint:2*thirdpoint].values
    df2 = df.iloc[:,2*thirdpoint:] - df.iloc[:,thirdpoint:2*thirdpoint].values

    # np.sum(df1.values*df2.values,axis=1) acts as row-wise dot product
    # Custom function for ease of use
    rwdot = lambda x, y: np.sum(x * y, axis=1)

    # arccos(dotproduct / sqrt(x^2+y^2+z^2 of a) *sqrt(x^2+y^2+z^2 of b))
    # arccos(a * b / | a | * | b | );
    # arccos(dotp of a&b / dotp of (sqrt(dotp of a&a) & sqrt(dotp of b&b)))
    angle = pd.DataFrame(np.arccos(rwdot(df1.values, df2.values) / (np.sqrt(rwdot(df1.values, df1.values)) * np.sqrt(rwdot(df2.values, df2.values)))))

    return angle
