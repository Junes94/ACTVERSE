import pandas as pd


def cal_vel(data, joint='head', xyz=('x', 'y')):
    """
    this function calculates velocity at each frame from AVATAR csv file
    :param data: raw data, csv file from AVATAR
    :param joint: (tuples) joint you want to calculate
    :param xyz: (tuples) coordinates you want to calculate
    :return: moving distance at each frame(velocity) of the joint+xyz
    """
    data_diff_sq = data.diff(axis=0) ** 2

    cols = []  # joints plotted
    velocity = pd.DataFrame()
    if type(joint) == str:
        for ii in xyz:
            cols.append(joint + '_' + ii)
        # (dx^2+dy^2)^(1/2)
        velocity[joint + '-' + ''.join(xyz)] = data_diff_sq[cols].sum(axis=1, skipna=False) ** (1 / 2)
    else:
        for i in joint:
            for ii in xyz:
                cols.append(i + '_' + ii)
            # (dx^2+dy^2)^(1/2)
            velocity[i + '-' + ''.join(xyz)] = data_diff_sq[cols].sum(axis=1, skipna=False) ** (1 / 2)

    return velocity


def cal_accel(data, joint='head', xyz=('x', 'y')):
    """
    this function calculates acceleration at each frame from AVATAR csv file
    :param data: raw data, csv file from AVATAR
    :param joint: (tuples) joint you want to calculate
    :param xyz: (tuples) coordinates you want to calculate
    :return: acceleration at each frame of the joint+xyz
    """
    data_ddiff_sq = data.diff(axis=0).diff(axis=0) ** 2

    cols = []  # joints plotted
    accel = pd.DataFrame()
    if type(joint) == str:
        for ii in xyz:
            cols.append(joint + '_' + ii)
        # (ddx^2+ddy^2)^(1/2)
        accel[joint + '-' + ''.join(xyz)] = data_ddiff_sq[cols].sum(axis=1, skipna=False) ** (1 / 2)
    else:
        for i in joint:
            for ii in xyz:
                cols.append(i + '_' + ii)
            # (ddx^2+ddy^2)^(1/2)
            accel[i + '-' + ''.join(xyz)] = data_ddiff_sq[cols].sum(axis=1, skipna=False) ** (1 / 2)

    return accel
