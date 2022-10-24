def walkFrameBool(head_2d, torso_2d, torso_z, vel_thres=0.2, dist_thres=5, moving_windows=7):
    """
    This function returns mouse walking frame as a boolean values. Walk should satisfy criteria below.
    criteria 1: To rule out frames at which a mouse shows rearing or jumping behavior (torso_z coord. < mean of z coord)
    criteria 3: Convolved velocity at each frame must exceed the value of vel_thres
    criteria 4: Moving distance of a walking bout (from the time it rises above the value until it falls again)
    must exceed dist_thres
    :param head_2d:
    :param torso_2d:
    :param torso_z:
    :param vel_thres:
    :param dist_thres:
    :param moving_windows:
    :return:
    """

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

    # criteria 1
    walk2 = torso_z < (torso_z.mean(axis=0, skipna=False) * 2)  # boolean values satisfying criteria 2

    # criteria 3
    velocity_conv = torso_velocity.rolling(moving_windows, center=True).mean()
    walk3 = velocity_conv > vel_thres
    # criteria 4
    walk_bout = walk3[walk3 == 1].groupby((walk3 != 1).cumsum())    # walking bout as bool values satisfying crit3
    for group_index in walk_bout.dtype.index:
        if velocity_conv[walk_bout.groups[group_index]].sum() < dist_thres:
            walk3[walk_bout.groups[group_index]] = False