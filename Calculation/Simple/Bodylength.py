import numpy as np

def bodylength(dataframe):
    workingframe = dataframe.loc[:,['Nose_x','Anus_x','Nose_y','Anus_y','Nose_z','Anus_z']]
    length = np.sqrt(((workingframe.iloc[:,0]-workingframe.iloc[:,1])**2 + (workingframe.iloc[:,2]-workingframe.iloc[:,3])**2 + (workingframe.iloc[:,4]-workingframe.iloc[:,5])**2))
    return length

