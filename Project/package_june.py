import Calculator.openfield as cof
import FileManager.preprocess as app
from Project.SDSBD import params


def Avatar(data, eventType):
    """ This function is for AVATAR center entry analysis.
    This function is for AVATAR analysis
    :param data: AVATAR DataFrame (frame X 27 columns)
    :param start:
    :param end:
    :param fps:
    :return: 1. (Series) Boolean values when a mouse enters the center
    2. velocities
    """
    # basic variable settings
    start = params.start
    end = params.end
    torso_3d = data.iloc[:, 9:12]

    if eventType == 'center':
        joint1 = params.joint1
        joint2 = params.joint2
        radius = params.radius
        coord_3d = app.centerPoint(data, joint1, joint2)  # set head-torso middle point as a body center point.
    elif eventType == 'walk':
        vel_thres = params.vel_thres
        angle_thres = params.angle_thres
        dist_thres = params.dist_thres
        coord_3d = torso_3d   # torso coordinates

    # Velocity calculation
    coord_2d = coord_3d.iloc[:, 0:2]
    coord_z = coord_3d.iloc[:, [2]]
    velocity_2d = cof.vel(coord_2d)
    velocity_z = cof.vel(coord_z)

    # Event analysis
    if eventType == 'center':
        event_frame = cof.centerFrameBool(data, radius)  # boolean dataframe where a mouse is in center zone.
    elif eventType == 'walk':
        event_frame = cof.walkFrameBool(data, vel_thres, angle_thres, dist_thres)
    event_frame = event_frame.iloc[start:end]
    event_index = cof.boolIndex(event_frame)  # (list) find frame where a mouse enters the center zone.
    event_velocity_2d = velocity_2d.loc[event_index]
    event_velocity_z = velocity_z.loc[event_index]
    event_boutNum = cof.boolBout(event_frame)

    # General
    total_distance_2d = sum(velocity_2d.iloc[start:end])  # moving distance (total)
    total_distance_z = sum(velocity_z.iloc[start:end])

    # Results
    # Absolute values
    event_distance_2d = sum(event_velocity_2d)
    event_distance_z = sum(event_velocity_z)

    # Relative values
    event_duration = (lambda x: x.sum() / len(x))(event_frame)  # duration (center/total)
    event_distance_2d_ratio = event_distance_2d / total_distance_2d  # moving distance ratio (center/total)
    event_distance_z_ratio = event_distance_z / total_distance_z

    results = {eventType+'_duration': event_duration, eventType+'_distance_horiz': event_distance_2d,
               eventType+'_distance_horiz_ratio': event_distance_2d_ratio,
               eventType+'_distance_vertic': event_distance_z,
               eventType+'_distance_vertic_ratio': event_distance_z_ratio, eventType+'_bout': event_boutNum,
               'distance_horiz': total_distance_2d, 'distance_vertic': total_distance_z}

    return results
