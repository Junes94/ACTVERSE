import copy
import FileManager.csvload as acl
import FileManager.preprocess as app
import Calculator.openfield as cof


path = "C:/Users/MyPC/Desktop/실험실/아바타/ACTNOVA회사/"
results = acl.load(path)

# If user fill this variable (ex. ['head_x','head_y',...]), data column will be automatically labeled.
label = None
results = acl.labeler(results, label)
data_list = copy.deepcopy(results['data_list'])     # list that contains DataFrame from csv files.

# Set head-torso middle point as a body center point
# ['nose', 'head', 'anus', 'torso', 'LH', 'RH', 'LF', 'RF', 'tail']
joint1 = [3, 4, 5]
joint2 = [9, 10, 11]
centerpoint_list = list(map(app.centerPoint, data_list, [joint1] * len(data_list), [joint2] * len(data_list)))

# extract specific rows
fps = 30
start = round(fps*5)
end = round(fps*400-fps*5)

data_analysis_list = list(map(app.extract, centerpoint_list, [start] * len(data_list), [end] * len(data_list)))

# Center zone analysis
center_frame_list = list(map(cof.centerFrameBool, data_analysis_list))
center_duration_list = list(map(lambda x: x.sum()/len(x), center_frame_list))

# Basic calculation
velocity_list = list(map(cof.vel, data_analysis_list))
acceleration_list = list(map(cof.accel, data_analysis_list))


