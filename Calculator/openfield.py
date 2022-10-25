import copy
import ctypes
import pandas as pd
import Calculator.basics as ccb
from math import pi

def vel(centerpoint):
    """
    This function calculates velocity at each frame from AVATAR csv file
    :param centerpoint: DataFrame users want to calculate (must have specific columns from output of 'load' function)
    :return: moving distance at each frame(velocity) of the cols. (format: Series)
    """
    if len(centerpoint.columns) > 3:  # Data point should be less than 3D.
        ctypes.windll.user32.MessageBoxW(0, u"Data columns could not have more than 3.", u"Error", 0)

    data_diff_sq = centerpoint.diff(axis=0) ** 2  # (frame(N+1)-frame(N))^2
    velocity = data_diff_sq.sum(axis=1, skipna=False) ** (1 / 2)  # (dx^2+dy^2)^(1/2)
    return velocity


def accel(centerpoint):
    """
    This function calculates acceleration at each frame from AVATAR csv file
    :param centerpoint: DataFrame users want to calculate (must have specific columns from output of 'load' function)
    :return: acceleration at each frame of the cols. (format: Series)
    """
    if len(centerpoint.columns) > 3:  # Data point should be less than 3D.
        ctypes.windll.user32.MessageBoxW(0, u"Data columns could not have more than 3.", u"Error", 0)

    data_ddiff_sq = centerpoint.diff(axis=0).diff(axis=0) ** 2  # (frame_diff(N+1)-frame_diff(N))^2
    acceleration = data_ddiff_sq.sum(axis=1, skipna=False) ** (1 / 2)  # (dx^2+dy^2)^(1/2)
    return acceleration


def rearingBool(torso_z):
    """
    This function (for AVATAR) returns boolean values at which frames a mouse rears or jumps
    :param torso_z: DataFrame of z-coordinates of a mouse
    :return: (Series) bool values when a mouse rear or jumping
    """
    rearing = torso_z.iloc[:,0] > (torso_z.iloc[:,0].mean(axis=0, skipna=False) * 2)
    return rearing


def centerFrameBool(centerpoint, radius=3):
    """
    This function(for AVATAR) returns frames when a mouse enters the center zone
    :param centerpoint: (x,y columns) DataFrame users want to calculate (must have specific columns)
    :param radius: if radius=3, center zone would be (-3,-3)~(3,3) for x, y axis
    :return: boolean results whether a mouse enters into the center zone
    """
    centerpoint_x = centerpoint.iloc[:, 0]  # x coordinates of the data
    centerpoint_y = centerpoint.iloc[:, 1]  # y coordinates of the data
    center_frame = (abs(centerpoint_x) < radius) & (abs(centerpoint_y) < radius)
    return center_frame


def boolIndex(bool_frame):
    """
    This function(for AVATAR) returns indices that contain True values in bool_frame
    :param bool_frame: (pd.Series) boolean results (ex. 111000011111100000110)
    :return: list of indices of dataframe(center_frame that is the output of function centerFrameBool)
    """
    bool_index = bool_frame.index[bool_frame].tolist()
    return bool_index


def boolBout(bool_frame):
    """
    This function makes a group of consecutive True values (ex. [1111100011111] as two groups of 1)
    :param bool_frame: (pd.Series) boolean results (ex. 111000011111100000110)
    :return:
    """
    bool_bout = bool_frame[bool_frame == 1].groupby((bool_frame != 1).cumsum())
    return bool_bout

def walkFrameBool(head_2d, torso_2d, torso_z, vel_thres=0.1, angle_thres=90, dist_thres=5):
    """
    This function returns mouse walking frame as a boolean values. Walk should satisfy criteria below.
    criteria 1: To rule out frames at which a mouse shows rearing or jumping behavior (torso_z coord. < mean of z coord)
    criteria 2: Velocity of head and torso at each frame > vel_thres
    criteria 3: Angle btw torso-head and torso, head forward direction vector.
    criteria 4: Moving distance of a walking bout (from the time it rises above the value until it falls again)
    must exceed dist_thres
    :param head_2d:
    :param torso_2d:
    :param torso_z:
    :param vel_thres:
    :param angle_thres: False if angle > angle_thres
    :param dist_thres: True if total distance moved at each walk bout > dist_thres
    :return: boolean results whether a mouse walks
    """
    # Calculate vectors
    vector_head = head_2d.diff(axis=0)
    vector_torso = torso_2d.diff(axis=0)
    vector_torsoToHead = pd.DataFrame(head_2d.values[:] - torso_2d.values[:],
                                      columns=[name_A + '-' + name_B for name_A, name_B in
                                               zip(list(head_2d.columns), list(torso_2d.columns))],
                                      index=head_2d.index)
    # criteria 1
    walk1 = ~rearingBool(torso_z)  # boolean values not rearing or jumping

    # criteria 2
    velocity_head = (vector_head**2).sum(axis=1, skipna=False) ** (1/2)      # (dx^2+dy^2)^(1/2)
    velocity_torso = (vector_torso**2).sum(axis=1, skipna=False) ** (1/2)    # (dx^2+dy^2)^(1/2)
    walk2 = (velocity_head > vel_thres) & (velocity_torso > vel_thres)   # boolean values exceeding vel_thres

    # criteria 3
    angle_headForward = pd.Series(list(map(ccb.angle_between, vector_torsoToHead.values, vector_head.values[1:, :])),
                                     index=list(range(2, vector_torsoToHead.shape[0] + 1))) * 180/pi
    angle_torsoForward = pd.Series(list(map(ccb.angle_between, vector_torsoToHead.values, vector_torso.values[1:, :]
                                               )), index=list(range(2, vector_torsoToHead.shape[0] + 1))) * 180/pi
    walk3 = (angle_headForward < angle_thres) & (angle_torsoForward < angle_thres)

    # criteria 4
    walk123 = walk1 & walk2 & walk3   # bools satisfying crit1,2,3 based on indices(frame)
    walk_bout = walk123[walk123 == 1].groupby((walk123 != 1).cumsum())  # walking bout as bool values satisfying crit1,2,3
    walk4 = copy.deepcopy(walk123)
    for group_index in walk_bout.dtype.index:
        if velocity_torso[walk_bout.groups[group_index]].sum() < dist_thres:
            walk4[walk_bout.groups[group_index]] = False

    return walk4
