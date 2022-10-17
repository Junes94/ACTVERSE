import ctypes


def vel(centerpoint):
    """
    This function calculates velocity at each frame from AVATAR csv file
    :param centerpoint: DataFrame users want to calculate (must have specific columns from output of 'load' function)
    :return: moving distance at each frame(velocity) of the cols. (format: Series)
    """
    if len(centerpoint.columns) > 3:   # Data point should be less than 3D.
        ctypes.windll.user32.MessageBoxW(0, u"Data columns could not have more than 3.", u"Error", 0)

    data_diff_sq = centerpoint.diff(axis=0) ** 2   # (frame(N+1)-frame(N))^2
    velocity = data_diff_sq.sum(axis=1, skipna=False) ** (1 / 2)  # (dx^2+dy^2)^(1/2)
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
    acceleration = data_ddiff_sq.sum(axis=1, skipna=False) ** (1 / 2)  # (dx^2+dy^2)^(1/2)
    return acceleration


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


def centerIndex(center_frame, radius=3):
    """
    This function(for AVATAR) returns indices that contain True values in center_frame
    :param center_frame: boolean results whether a mouse enters into the center zone
    :param radius: if radius=3, center zone would be (-3,-3)~(3,3) for x, y axis
    :return: list of indices of dataframe(center_frame that is the output of function centerFrameBool)
    """
    center_index = center_frame.index[center_frame].tolist()
    return center_index


def walkFrameBool(torso_velocity, head_2d, torso_2d, torso_z, vel_thres=0.2, dist_thres=5, moving_windows=7):
    """
    This function returns mouse walking frame as a boolean values. Walk should satisfy criteria below.
    criteria 1: Convolved velocity at each frame must exceed the value of vel_thres
    criteria 2: Moving distance of a walking bout (from the time it rises above the value until it falls again)
    must exceed dist_thres
    criteria 3:
    :param torso_velocity:
    :param head_2d:
    :param torso_2d:
    :param torso_z:
    :param vel_thres:
    :param dist_thres:
    :param moving_windows:
    :return:
    """
    velocity_conv = torso_velocity.rolling(moving_windows, center=True).mean()
    walk1 = velocity_conv > vel_thres
    dd = walk1[walk1 == 1].groupby((walk1 != 1).cumsum())
    for group_index in dd.dtype.index:
        if velocity_conv[dd.groups[group_index]].sum() < dist_thres:
            walk1[dd.groups[group_index]] = False






