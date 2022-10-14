import easygui
"""This folder is for function which is user-friendly. Users just put their data in the function."""


def vel(data, cols=None):
    """
    this function calculates velocity at each frame from AVATAR csv file
    :param data: raw data, csv file from AVATAR
    :param cols: columns that users want to analyze
    :return: moving distance at each frame(velocity) of the cols. (format: Series)
    """
    data_diff_sq = data.diff(axis=0) ** 2   # (frame(N+1)-frame(N))^2
    if cols is None:    # If users enter no specific columns name, multichoice box will pop up.
        msg = "Which data columns you want to use for calculating velocity ?"
        title = "Select columns for velocity"
        choices = data_diff_sq.columns
        cols = easygui.multchoicebox(msg, title, choices)

    if len(cols) > 3:
        easygui.msgbox("Number of 'cols' could not exceed 3.", "Warning")
        velocity = None
        pass
    else:
        velocity = data_diff_sq[cols].sum(axis=1, skipna=False) ** (1 / 2)  # (dx^2+dy^2)^(1/2)

    return velocity


def accel(data, cols=None):
    """
    this function calculates acceleration at each frame from AVATAR csv file
    :param data: raw data, csv file from AVATAR
    :param cols: columns that users want to analyze
    :return: acceleration at each frame of the cols. (format: Series)
    """
    data_ddiff_sq = data.diff(axis=0).diff(axis=0) ** 2     # (frame_diff(N+1)-frame_diff(N))^2
    if cols is None:    # If users enter no specific columns name, multichoice box will pop up.
        msg = "Which data columns you want to use for calculating acceleration ?"
        title = "Select columns for acceleration"
        choices = data_ddiff_sq.columns
        cols = easygui.multchoicebox(msg, title, choices)

    if len(cols) > 3:
        easygui.msgbox("Number of 'cols' could not exceed 3.", "Warning")
        acceleration = None
        pass
    else:
        acceleration = data_ddiff_sq[cols].sum(axis=1, skipna=False) ** (1 / 2)  # (dx^2+dy^2)^(1/2)

    return acceleration
