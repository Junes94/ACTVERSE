from Loader import csvloader
from Loader import adv_load
from Calculation.Simple import Angular as angle


# print(csvloader)
# data = csvloader.avatarcsvloader('C:/Users/endyd/OneDrive/Onedrive-CK/OneDrive/Gradschool/Kaist/AVATAR/AVATAR_DATA_SET/1.OFT(WT-N=50)/raw/','H1.mat.csv_new')
# print(data)

testdata = adv_load.Easyavatarload(mode='Avatar')
# testdata = adv_load.Easyfolderload('General')
print(testdata)

# 3d
print(angle.point2angleplane(testdata.iloc[]))
print(angle.point2angleaxis(testdata))
print(angle.point2lineangle(testdata))

# 2d
