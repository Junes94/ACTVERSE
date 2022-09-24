import pandas as pd
from itertools import product
import easygui


def load(path, filename):
    """
    This function import AVATAR csv file as a DataFrame
    :param path: The folder path
    :param filename: csv file name
    :return: DataFrame of csv file
    """
    fullname = path + filename + '.csv'
    data = pd.read_csv(fullname, header=None)
    # name indices of DataFrame to frame numbers
    index = []
    for index_num in range(1, data.shape[0] + 1):
        index.append(f'{index_num}')
    data.set_axis(index, axis='index', inplace=True)

    return data


def labeler(data, label=None):
    """
    This function allocates specific column names to DataFrame
    :param data: csv data file
    :param label: specific column names user wants to define
    :return: DataFrame with name defined
    """
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
                                    label = [separator.join(label_name) for label_name in list(product(label_joint, label_coord))]
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
                if len(data.columns) == len(label):  # The number of label should be same with that of columns.
                    easygui.msgbox("Your data columns have labels now! \n\nIf you want to reset all labels, "
                                   "\nplease delete the second parameter of this function.", "Success")
                    data.columns = label
                    pass
                else:
                    easygui.msgbox("The number of manual labels must match the number of data columns.", "Warning")
                    pass
            else:
                easygui.msgbox("All column names need to be different.", "Warning")
                pass
        else:
            easygui.msgbox("There should be no blank element in the label list.", "Warning")
            pass

    print("data columns name:", data.columns.tolist())
    return data, label
