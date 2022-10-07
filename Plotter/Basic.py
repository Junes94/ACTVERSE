import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def avatarheatmap(df,nofgrid=6):

    # 3d mode, 2d mode, number of grids

    def remap(x, nofgrid):
        return np.floor((x - -9) * (nofgrid - 1) / (9 - -9) + 1)

    htmp = np.zeros((nofgrid,nofgrid))

    remapped = df.applymap(remap)
    heatmap = plt.hist2d(remapped.iloc[:,0],remapped.iloc[:,1],bins=[np.arange(0,nofgrid+1,1),np.arange(0,nofgrid+1,1)])
    # grouped = remapped.groupby([0, 1]).size()
    # newdf = grouped.to_frame(name='Instances').reset_index()

    # location = np.reshape(newdf['Instances'],(nofgrid,nofgrid)) # problematic when there are 0 counts.
    # sns.heatmap(location)
    plt.show()
    return heatmap

