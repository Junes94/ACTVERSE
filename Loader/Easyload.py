import Loader.avatarcsvloader
import Loader.generalcsvloader
import tkinter
from tkinter import filedialog
import pandas as pd

# tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
# folder_path = filedialog.askdirectory()

# # assign dataset names
# list_of_names = ['crime', 'username']
#
# # create empty list
# dataframes_list = []
#
# # append datasets into the list
# for i in range(len(list_of_names)):
#     temp_df = pd.read_csv("./csv/" + list_of_names[i] + ".csv")
#     dataframes_list.append(temp_df)

tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
folder_path = filedialog.askdirectory()
def Easyload(mode,path=folder_path):
    csvnamelist = []
    dataframe_list = []
    for i in range(len(csvnamelist)):
        if mode == 'Avatar':
            tmpdf = Loader.avatarcsvloader()
        elif mode == 'General':
            tmpdf = Loader.generalcsvloader()
        dataframe_list.append(tmpdf)