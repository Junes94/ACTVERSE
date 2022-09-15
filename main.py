import pandas
from itertools import product

def avatarcsvloader(pathrest, filename, givenpath ='C:/Users/endyd/OneDrive/문서/ACTVERSE/AVATAR_DATA_SET-20220913T084458Z-001/AVATAR_DATA_SET/'):
    fullname = givenpath+pathrest+filename+'.csv'
    # columnames = ['Nose_x', 'Nose_y', 'Nose_z', 'Head_x', 'Head_y', 'Head_z', 'Anus_x', 'Anus_y', 'Anus_z', 'Body_x', 'Body_y', 'Body_z', 'Leftfoot_x',
    #               'Leftfoot_y', 'Leftfoot_z', 'RightFoot_x', 'RightFoot_y', 'RightFoot_z', 'Lefthand_x', 'Lefthand_y', 'Lefthand_z', 'Righthand_x',
    #               'Righthand_y', 'Righthand_z', 'Tail_x', 'Tail_y', 'Tail_z']
    coord = ['_x', '_y', '_z']
    bodypart = ['Nose', 'Head', 'Anus', 'Body', 'Leftfoot', 'RightFoot', 'Lefthand', 'Righthand', 'Tail']
    testlist = list(product(bodypart, coord))
    columnames = [''.join(words) for words in testlist]
    output = pandas.read_csv(fullname, names=columnames)

    try:
        27 == output.shape[1]
    except:
        print('The number of columns are not 27; Check the data')
    else:
        return output


#testfile = pandas.read_csv('C:/Users/endyd/OneDrive/문서/ACTVERSE/AVATAR_DATA_SET-20220913T084458Z-001/AVATAR_DATA_SET/1.OFT(WT-N=50)/raw/H1.mat.csv_new.csv')
#1코 2머리 3항문 4몸통 5왼발 6오른발 7왼손 8오른손 9꼬리
#xyz 순
