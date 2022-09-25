import FileManage.csvload as acl
import Calculation.calculate_basic as ccb

path = "C:/Users/MyPC/Desktop/실험실/아바타/ACTNOVA회사/"
results = acl.load(path)
# data_list = results[0]
# data_namelist = results[2]

# If user fill this variable (ex. ['head_x','head_y',...]), data column will be automatically labeled.
label = None
results_labeled = acl.labeler(results, label)
# data.columns = label
# data_list = results_labeled[0]  # Data same with the above data, but has column labels.
# label_manual = results_labeled[1]  # list of labels which users tried to allocate into data columns.

joint = 'head'
xyz = ('x', 'y')

velocity = ccb.cal_vel(data_list, joint, xyz)
acceleration = ccb.cal_accel(data_list, joint, xyz)
