import ctypes
import pandas as pd


def extract(data, row_start=0, row_end=None, analysis_cols=None):
    # This function extracts specific rows and columns from data(iloc based).

    # Example below.
    # data_list = results['data_list']     # list that contains DataFrame from csv files.
    # analysis_cols = [3, 4, 5]
    # data_ext_list = list(map(app.extract, data_list, [analysis_cols] * len(data_list)))

    if analysis_cols is None:
        data_ext = data.iloc[row_start:row_end, :]
    else:
        data_ext = data.iloc[row_start:row_end, analysis_cols]
    return data_ext


def centerPoint(data, joint1, joint2):
    # This function makes other coordinates(center point, etc...) using specific columns from data(iloc based).

    # Example below.
    # data_list = results['data_list']     # list that contains DataFrame from csv files.
    # joint1 = [3, 4, 5]
    # joint2 = [9, 10, 11]
    # centerpoint_list = list(map(app.centerPoint, data_list, [joint1] * len(data_list), [joint2] * len(data_list)))

    if len(joint1) is not len(joint2):
        ctypes.windll.user32.MessageBoxW(0, u"joint1 and joint2 should be the same length of the list.", u"Error", 0)
        centerpoint = None
    else:
        centerpoint = pd.DataFrame()
        columnsName = []
        for i in range(len(joint1)):
            centerpoint[i] = data.iloc[:, [joint1[i], joint2[i]]].mean(axis=1, skipna=False)
            # To make centerpoint columns names.
            columnsName.append('Mean of ' + data.columns[joint1[i]] + ', ' + data.columns[joint2[i]])
        centerpoint.columns = columnsName
    return centerpoint
