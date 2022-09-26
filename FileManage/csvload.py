import pandas as pd
from itertools import product
import easygui
import os


def load(path=None, filelist_path=None):
    """
    This function import AVATAR csv file as a DataFrame
    :param path: The folder path
    :param filelist_path: csv file name list (ex. ["C/Users/~~/mouse1.csv", "C/Users/~~/mouse2.csv"]
    :return: dictionary -> [0]=data list, [1]=folder name analyzed, [2]=file name analyzed
    """
    if path is None:
        path = easygui.diropenbox(title="Choose your data folder.")

    if filelist_path is None:
        filelist_path = easygui.fileopenbox(title="Select data files.", default=path, filetypes="*.csv", multiple=True)

    # Name indices of DataFrame to frame numbers.
    data_list = []
    data_namelist = []
    for i in range(len(filelist_path)):
        data_individual = pd.read_csv(filelist_path[i], header=None)
        index = list(range(1, data_individual.shape[0] + 1))
        data_individual.set_axis(index, axis='index', inplace=True)
        data_individual.index.name = "frame"
        data_list.append(data_individual)

        # Store data file name into a list.
        filename = os.path.basename(filelist_path[i])  # Extract only file name(not total path).
        data_namelist.append(filename)

    print(path)
    results = dict(data_list=data_list, path=path, data_namelist=data_namelist)
    return results


def labeler(results, label=None):
    """
    This function allocates specific column names to DataFrame
    :param results: csv data file list [DataFrame, DataFrame, ...]
    :param label: specific column names user wants to define
    :return: dictionary
    """
    data_list = results['data_list']
    data = data_list[0]  # First dataframe of a list is used for labeling columns.
    data_namelist = results['data_namelist']

    if label is not None:  # If users enter 'label' already.
        pass
    else:  # If 'label' is empty.
        msg = "Do you want your data columns to be labeled? \n \nIf click 'No', columns would be 0, 1, 2, ..."
        choices = ["Yes", "No"]
        reply = easygui.buttonbox(msg, choices=choices)
        if reply == "Yes":  # If users want their data columns have name.
            msg = "Do you want to label columns manually? \n\nIf you click 'No', you can use default labeling."
            choices = ["Yes, manually", "No, auto-labeling"]
            manual_tf = easygui.buttonbox(msg, choices=choices)
            if manual_tf == "Yes":
                msg = "Enter data column names you want to assign."
                title = "Manual labeling mode"
                fieldnames = data.columns.tolist()  # list of the original names of columns.
                label = easygui.multenterbox(msg, title, fieldnames)
            else:  # if users want to use default mode for labels.
                msg = "Is your data from AVATAR, having 27 columns?"
                title = "Auto-labeling mode"
                choices = ["Yes", "No"]
                avatar_tf = easygui.buttonbox(msg, title, choices=choices)
                if avatar_tf == "Yes":  # allocate each name of joint coordinate to column as AVATAR labeling.
                    label_joint = ['nose', 'head', 'anus', 'tail', 'torso', 'LH', 'RH', 'LF', 'RF']
                    label_coord = ['x', 'y', 'z']
                    separator = '_'
                    label = [separator.join(label_name) for label_name in list(product(label_joint, label_coord))]
                else:  # allocate each name of joint coordinate to column as 'joint_coordinate'.
                    msg = "How many joints and dimensions your data has.\nPlease write number only."
                    fieldnames = ["Number of joints", "Number of dimensions(x,y,z)"]
                    # users write down the number of joints and coord.
                    label_number = easygui.multenterbox(msg, title, fieldnames)
                    joint_number = int(label_number[0])
                    coord_number = int(label_number[1])
                    label_coord = [['x', 'y', 'z'][i] for i in range(coord_number)]
                    joint_numbering = [xx + 1 for xx in list(range(joint_number))]
                    joint_numbering2 = [str(x) for x in joint_numbering]
                    if coord_number > 3:
                        easygui.msgbox("Data dimension could not exceed 3.", "Warning")
                        pass
                    else:
                        msg = "Enter joints name your data has.\n\n For example, nose, head, ..."
                        # joint number to be filled in by users.
                        fieldnames = ['#'.join(x) for x in list(product(['Joint'], joint_numbering2))]
                        label_joint = easygui.multenterbox(msg, title, fieldnames)
                        if label_joint is not None:
                            if len(label_joint) == sum(x is not "" for x in label_joint):  # There should be no blank.
                                # Extract required amount of coord.
                                if len(label_joint) == len(set(label_joint)):  # There should be no duplicate elements.
                                    separator = '_'
                                    label = [separator.join(label_name) for label_name in
                                             list(product(label_joint, label_coord))]
                                else:
                                    easygui.msgbox("All joint names need to be different.", "Warning")
                                    pass
                            else:
                                easygui.msgbox("There should be no blank in the joint list.", "Warning")
                                pass

    # Finally check whether label list is compatible with data columns.
    if label is not None:
        if len(label) == sum(x is not "" for x in label):  # There should be no blank.
            if len(label) == len(set(label)):  # There should be no duplicate elements.
                success_number = 0
                for filenumber in range(len(data_namelist)):
                    if len(data_list[filenumber].columns) == len(
                            label):  # The number of label should be same with that of columns.
                        data_list[filenumber].columns = label  # Execute column labeling
                    else:
                        easygui.msgbox(f'{data_namelist[filenumber]} '
                                       f'has different column numbers with manual label numbers.', "Warning")
                        pass
                        break
                    success_number = success_number + 1
                if success_number == range(len(data_namelist)):
                    easygui.msgbox("Your data columns have labels now! \n\nIf you want to reset all labels, "
                                   "\nplease delete the second parameter of this function.", "Success")
                    pass
            else:
                easygui.msgbox("All column names need to be different.", "Warning")
                pass
        else:
            easygui.msgbox("There should be no blank element in the label list.", "Warning")
            pass

    print("data columns name:", data.columns.tolist())
    results['data_list'] = data_list  # upgrade data with labels.
    results['label'] = label  # add label key to dictionary.
    return results
