import copy
import pandas as pd
import numpy as np
import FileManager.csvload as acl
import Project.package_june as ppj
import Calculator.openfield as cof
import FileManager.preprocess as app
from Project.SDSBD import params
import seaborn as sns
import matplotlib
import time

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

path = r'C:\Users\MyPC\Desktop\실험실\2.실험데이터\AVATAR-SDSBD\''
# filepath = ["C:/Users/MyPC/Desktop/실험실/아바타/ACTNOVA회사/dataForTest/C_403.mp4.txt.csv"]
results = acl.load(path)

# If user fill this variable (ex. ['head_x','head_y',...]), data_pre column will be automatically labeled.
label = ['nose_x', 'nose_y', 'nose_z', 'head_x', 'head_y', 'head_z', 'anus_x', 'anus_y',
         'anus_z', 'torso_x', 'torso_y', 'torso_z', 'LH_x', 'LH_y', 'LH_z', 'RH_x', 'RH_y', 'RH_z',
         'LF_x', 'LF_y', 'LF_z', 'RF_x', 'RF_y', 'RF_z', 'tail_x', 'tail_y', 'tail_z']

results = acl.labeler(results, label)
data_list = copy.deepcopy(results['data_list'])  # list that contains DataFrame from csv files.

# Parameter settings = see the file 'Project.SDSBD.params.py'
start = params.start
end = params.end

# Calculation
ID = 0
results_total = pd.DataFrame([])
start_time = time.process_time()  # 시작 시간 저장

for data in data_list:
    results_center = ppj.Avatar(data, 'center', start, end)  # center analysis
    results_walk = ppj.Avatar(data, 'walk', start, end)  # walking analysis

    # rearing analysis
    rearing = cof.rearingBool(data)
    rearing = rearing.iloc[start:end]
    rearing_boutNum = cof.boolBout(rearing)
    results_rearing = dict(rearing_bout=rearing_boutNum)

    # Results update
    mouse = results['data_namelist'][ID]

    results_walk.update(results_rearing)
    results_center.update(results_walk)
    results_mouse = pd.DataFrame(results_center, index=[mouse])
    results_total = pd.concat([results_total, results_mouse])

    ID = ID + 1

results_total.to_csv(results['path']+r'\proj_SDSBD_221226.csv')
end_time = time.process_time()
print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")  # 현재시각 - 시작시간 = 실행 시간
