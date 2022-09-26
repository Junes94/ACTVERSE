import FileManage.csvload as acl
import Calculation.calculate_basic as ccb

path = "C:/Users/MyPC/Desktop/실험실/아바타/ACTNOVA회사/"
results = acl.load(path)

# If user fill this variable (ex. ['head_x','head_y',...]), data column will be automatically labeled.
label = None
results_labeled = acl.labeler(results, label)

data_list = results_labeled[0]
analysis_col = [['head_x', 'head_y'], ['torso_x', 'torso_y']]

velocity = ccb.cal_vel(data_list, analysis_col)
acceleration = ccb.cal_accel(data_list, analysis_col)
