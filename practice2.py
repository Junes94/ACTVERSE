from Loader import csvloader
from Loader import adv_load
from Calculation.Simple import Angular as angle


# print(csvloader)
# data_pre = csvloader.avatarcsvloader('C:/Users/endyd/OneDrive/Onedrive-CK/OneDrive/Gradschool/Kaist/AVATAR/AVATAR_DATA_SET/1.OFT(WT-N=50)/raw/','H1.mat.csv_new')
# print(data_pre)

testdata = adv_load.Easyavatarload()
# testdata = adv_load.Easyfolderload('General')
# print(testdata)


# 3d
test3d = testdata.iloc[:,:9]
# print(test3d)
# print(angle.point2angleplane(test3d.iloc[:,:6]))
# print(angle.point2angleaxis(test3d.iloc[:,:6]))
# print(angle.point2lineangle(test3d))

# 2d
test2d = testdata.iloc[:,[0, 1, 3, 4, 6, 7]]
# print(test2d)
# print(angle.point2angleplane(test2d.iloc[:,:4]))
# print(angle.point2angleaxis(test2d.iloc[:,:4]))
# print(angle.point2lineangle(test2d))
