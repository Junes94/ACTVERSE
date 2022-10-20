import ctypes
import pandas as pd


def vel(centerpoint):
    """
    This function calculates velocity at each frame from AVATAR csv file
    :param centerpoint: DataFrame users want to calculate (must have specific columns from output of 'load' function)
    :return: moving distance at each frame(velocity) of the cols. (format: Series)
    """
    if len(centerpoint.columns) > 3:   # Data point should be less than 3D.
        ctypes.windll.user32.MessageBoxW(0, u"Data columns could not have more than 3.", u"Error", 0)

    data_diff_sq = centerpoint.diff(axis=0) ** 2   # (frame(N+1)-frame(N))^2
    velocity = data_diff_sq.sum(axis=1, skipna=False) ** (1/2)  # (dx^2+dy^2)^(1/2)
    return velocity


def accel(centerpoint):
    """
    This function calculates acceleration at each frame from AVATAR csv file
    :param centerpoint: DataFrame users want to calculate (must have specific columns from output of 'load' function)
    :return: acceleration at each frame of the cols. (format: Series)
    """
    if len(centerpoint.columns) > 3:   # Data point should be less than 3D.
        ctypes.windll.user32.MessageBoxW(0, u"Data columns could not have more than 3.", u"Error", 0)

    data_ddiff_sq = centerpoint.diff(axis=0).diff(axis=0) ** 2     # (frame_diff(N+1)-frame_diff(N))^2
    acceleration = data_ddiff_sq.sum(axis=1, skipna=False) ** (1/2)  # (dx^2+dy^2)^(1/2)
    return acceleration


def rearingBool(torso_z):
    """
    This function (for AVATAR) returns boolean values at which frames a mouse rears or jumps
    :param torso_z: DataFrame of z-coordinates of a mouse
    :return:
    """
    rearing = torso_z > (torso_z.mean(axis=0, skipna=False) * 2)
    return rearing


def centerFrameBool(centerpoint, radius=3):
    """
    This function(for AVATAR) returns frames when a mouse enters the center zone
    :param centerpoint: (x,y columns) DataFrame users want to calculate (must have specific columns)
    :param radius: if radius=3, center zone would be (-3,-3)~(3,3) for x, y axis
    :return: boolean results whether a mouse enters into the center zone
    """
    centerpoint_x = centerpoint.iloc[:, 0]    # x coordinates of the data
    centerpoint_y = centerpoint.iloc[:, 1]    # y coordinates of the data
    center_frame = (abs(centerpoint_x) < radius) & (abs(centerpoint_y) < radius)
    return center_frame


def centerIndex(center_frame):
    """
    This function(for AVATAR) returns indices that contain True values in center_frame
    :param center_frame: boolean results whether a mouse enters into the center zone
    :return: list of indices of dataframe(center_frame that is the output of function centerFrameBool)
    """
    center_index = center_frame.index[center_frame].tolist()
    return center_index


def walkFrameBool(torso_velocity, head_2d, torso_2d, torso_z, vel_thres=0.2, dist_thres=5, moving_windows=7):
    """
    This function returns mouse walking frame as a boolean values. Walk should satisfy criteria below.
    criteria 1: Moving forward not backward (head-torso distance at t frame > head(t frame)-torso(t+1 frame) distance)
    criteria 2: To rule out frames at which a mouse shows rearing or jumping behavior (torso_z coord. < mean of z coord)
    criteria 3: Convolved velocity at each frame must exceed the value of vel_thres
    criteria 4: Moving distance of a walking bout (from the time it rises above the value until it falls again)
    must exceed dist_thres
    :param torso_velocity:
    :param head_2d:
    :param torso_2d:
    :param torso_z:
    :param vel_thres:
    :param dist_thres:
    :param moving_windows:
    :return:
    """
    # criteria 1
    # make (t+1) frame torso coordinates from t frame
    row_None = pd.DataFrame([[None, None]], columns=torso_2d.columns)
    torso_2d_late = torso_2d.iloc[1:, :].append(row_None)
    torso_2d_late.columns = [str(torso_2d.columns[0])+"_late", str(torso_2d.columns[1])+"_late"]

    # calculate head-torso distance at t & (t+1) frame
    vec_late = pd.DataFrame(torso_2d_late.values[:] - head_2d.values[:],
                            columns=[str(torso_2d_late.columns[0])+"-"+str(head_2d.columns[0]),
                                     str(torso_2d_late.columns[1])+"-"+str(head_2d.columns[1])])
    vec_early = pd.DataFrame(torso_2d.values[:] - head_2d.values[:],
                             columns=[str(torso_2d.columns[0])+"-"+str(head_2d.columns[0]),
                                      str(torso_2d.columns[1])+"-"+str(head_2d.columns[1])])
    dist_late = (vec_late**2).sum(axis=1, skipna=False) ** (1/2)     # (vec_x^2+vec_y^2)^(1/2)
    dist_early = (vec_early**2).sum(axis=1, skipna=False) ** (1/2)

    walk1 = dist_late < dist_early  # boolean values satisfying criteria 1

    # criteria 2
    walk2 = torso_z < (torso_z.mean(axis=0, skipna=False) * 2)  # boolean values satisfying criteria 2

    # criteria 3
    velocity_conv = torso_velocity.rolling(moving_windows, center=True).mean()
    walk3 = velocity_conv > vel_thres
    # criteria 4
    walk_bout = walk3[walk3 == 1].groupby((walk3 != 1).cumsum())    # walking bout as bool values satisfying crit3
    for group_index in walk_bout.dtype.index:
        if velocity_conv[walk_bout.groups[group_index]].sum() < dist_thres:
            walk3[walk_bout.groups[group_index]] = False
