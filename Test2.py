import copy
import numpy as np
import FileManager.csvload as acl
import FileManager.preprocess as app
import Calculator.openfield as cof
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

path = "C:/Users/MyPC/Desktop/실험실/아바타/ACTNOVA회사/"
#filepath = ["C:/Users/MyPC/Desktop/실험실/아바타/ACTNOVA회사/dataForTest/C_403.mp4.txt.csv"]
results = acl.load(path)

# If user fill this variable (ex. ['head_x','head_y',...]), data column will be automatically labeled.
# label = ['nose_x', 'nose_y', 'nose_z', 'head_x', 'head_y', 'head_z', 'anus_x', 'anus_y',
   #      'anus_z', 'torso_x', 'torso_y', 'torso_z', 'LH_x', 'LH_y', 'LH_z', 'RH_x', 'RH_y', 'RH_z',
     #    'LF_x', 'LF_y', 'LF_z', 'RF_x', 'RF_y', 'RF_z', 'tail_x', 'tail_y', 'tail_z']

results = acl.labeler(results)
data_list = copy.deepcopy(results['data_list'])     # list that contains DataFrame from csv files.

# Parameter settings
    # ['nose', 'head', 'anus', 'torso', 'LH', 'RH', 'LF', 'RF', 'tail']
joint1 = [3, 4, 5]      # Set head-torso middle point as a body center point
joint2 = [9, 10, 11]
fps = 30
start = round(fps * 5)              # start frame to be analyzed
end = round(fps * 400 - fps * 5)    # end frame to be analyzed
moving_windows = 6                  # window size(frame numbers) to be averaged

for data in data_list:

    centerpoint_3d = app.centerPoint(data, joint1, joint2)  # set head-torso middle point as a body center point.
    centerpoint_2d = centerpoint_3d.iloc[:, 0:2]
    velocity_3d = cof.vel(centerpoint_3d)
    velocity_2d = cof.vel(centerpoint_2d)

    # Extract specific rows
    data_analysis_3d = app.extract(centerpoint_3d, start, end)
    data_analysis_2d = app.extract(centerpoint_2d, start, end)

    # Center zone analysis
    center_frame = cof.centerFrameBool(data_analysis_2d)        # boolean dataframe where a mouse is in center zone.
    center_duration = (lambda x: x.sum()/len(x))(center_frame)  # duration (center/total)

    center_index = cof.centerIndex(center_frame)            # (list) find frame where a mouse enters the center zone.
    center_velocity_2d = velocity_2d.loc[center_index]

    total_distance = sum(velocity_2d.iloc[start:end])         # moving distance (total)
    center_distance = sum(center_velocity_2d)/total_distance  # moving distance ratio (center/total)

    velocity_conv = velocity_2d.rolling(moving_windows, center=True).mean()

    data_plot = velocity_conv[10:300]
    sns.lineplot(x=data_plot.index, y=data_plot.values)
    plt.show()
    # Walk analysis



    # Final results
    total_distance
    center_duration
    center_distance

