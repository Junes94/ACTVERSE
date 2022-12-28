import seaborn as sns
import numpy as np
import pandas as pd
import easygui
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
#sns.set(rc={'figure.figsize': (7, 13)})
import openpyxl
import scipy

sns.set_theme(style="ticks", font_scale=3.8)
qualitative_colors = sns.color_palette("Set3", 10)
sns.set_palette(qualitative_colors)

# import data_pre
path = r'C:\Users\MyPC\Desktop\실험실\2.실험데이터\AVATAR-SDSBD\analysis\python\''
filelist_path_pre = easygui.fileopenbox(title="Select data_pre files.", default=path, multiple=True)
data_pre = pd.read_excel(filelist_path_pre[0])

# import data_post
filelist_path_post = easygui.fileopenbox(title="Select data_post files.", default=path, multiple=True)
data_post = pd.read_excel(filelist_path_post[0])

# import column names
path_columnName = r'C:\Users\MyPC\Desktop\실험실\2.실험데이터\AVATAR-SDSBD\analysis\python\column_name.txt'
column_name = pd.read_csv(path_columnName, header=None)
index_SIratio = 2   # index of SI_ratio in the DataFrame 'data_pre' & 'data_post'

# For plotting mean and individual values
i = 0
for column in data_pre.columns[index_SIratio:]:
    fig, axes = plt.subplots(nrows=2, ncols=1, sharey=True, figsize=(12, 24))

    g_pre = sns.barplot(data=data_pre, x="group", y=column, ax=axes[0]).set(title='Pre-CSD')
    g_pre = sns.swarmplot(data=data_pre, x="group", y=column, color='grey', dodge=True, size=15, ax=axes[0])
    g_pre.set(xlabel="", ylabel=column_name.iloc[i, 0])
    plt.tight_layout()

    g_post = sns.barplot(data=data_post, x="group", y=column, ax=axes[1]).set(title='Post-CSD')
    g_post = sns.swarmplot(data=data_post, x="group", y=column, color='grey', dodge=True, size=15, ax=axes[1])
    g_post.set(xlabel="", ylabel=column_name.iloc[i, 0])

    sns.despine()
    plt.tight_layout()
    i = i+1
    plt.savefig(r'C:\Users\MyPC\Desktop\실험실\2.실험데이터\AVATAR-SDSBD\analysis\python\plot\''
                + column + '.png', dpi=300)


# For plotting correlation between SI ration & each column
def line(x, y):
    """Fit a line in a scatter based on slope and intercept"""
    """https://medium.com/@vince.shields913/econometrics-with-python-pt-3-3-9e16d88dbe87"""
    slope, intercept = np.polyfit(x, y, 1)
    line_values = [slope * ii + intercept for ii in x]
    #plt.plot(x, line_values, 'grey')
    return line_values


data_pre_onlyDefeat = data_pre[data_pre["group"] != 'control']      # extract resil, suscep mice only
data_post_onlyDefeat = data_post[data_post["group"] != 'control']      # extract resil, suscep mice only

iii = 0
sns.set_theme(style="ticks", font_scale=3.8)
for column in data_pre_onlyDefeat.columns[index_SIratio+1:]:
    iii = iii+1
    analysis_param = column_name.iloc[iii, 0]

    # pre-CSD
    fig = plt.subplots(nrows=1, ncols=1, figsize=(12, 12))
    RSscatter_pre = sns.scatterplot(data=data_pre_onlyDefeat, x="SI_ratio", y=column, hue="group", palette="deep",
                                    legend=False, s=350)
    RSscatter_pre.set(xlabel="Social interaction ratio", ylabel=analysis_param)
    correlLine_pre = line(data_pre_onlyDefeat.SI_ratio, data_pre_onlyDefeat[column])
    sns.lineplot(x=data_pre_onlyDefeat.SI_ratio, y=correlLine_pre, color='grey', lw=5, linestyle='--')
    sns.despine()
    plt.tight_layout()
    plt.savefig(r'C:\Users\MyPC\Desktop\실험실\2.실험데이터\AVATAR-SDSBD\analysis\python\plot\'pre_Correl_'
                + column + '.png', dpi=300)

    # post-CSD
    fig = plt.subplots(nrows=1, ncols=1, figsize=(12, 12))
    RSscatter_post = sns.scatterplot(data=data_post_onlyDefeat, x="SI_ratio", y=column, hue="group", palette="deep",
                                     legend=False, s=350)
    RSscatter_post.set(xlabel="Social interaction ratio", ylabel=analysis_param)
    correlLine_post = line(data_post_onlyDefeat.SI_ratio, data_post_onlyDefeat[column])
    sns.lineplot(x=data_post_onlyDefeat.SI_ratio, y=correlLine_post, color='grey', lw=5, linestyle='--')
    sns.despine()
    plt.tight_layout()
    plt.savefig(r'C:\Users\MyPC\Desktop\실험실\2.실험데이터\AVATAR-SDSBD\analysis\python\plot\'post_Correl_'
                + column + '.png', dpi=300)
    plt.close('all')

#matplotlib.pyplot.close('all')

# statistics
#scipy.stats.pearsonr(data_pre.column, y, *, alternative='two-sided')
