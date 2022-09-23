import FileManage.csvload as acl
import Calculation.calculate_basic as ccb
import easygui


givenpath = 'C:/Users/MyPC/Desktop/실험실/2.실험데이터/AVATAR-SDSBD/post/22.09.13.DataSet_SI1기준/'
pathrest = 'Control/'
filename = '01.mp4.txt'

data = acl.load(givenpath, pathrest, filename)

label = None
results = acl.labeler(data, label)
# data.columns = label
data = results[0]  # Data same with the above data, but has column labels.
label_manual = results[1]  # list of labels which users tried to allocate into data columns.

joint = 'head'
xyz = ('x', 'y')

velocity = ccb.cal_vel(data, joint, xyz)
acceleration = ccb.cal_accel(data, joint, xyz)
