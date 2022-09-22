from Loader import csvloader
from Loader import adv_load

# print(csvloader)
# data = csvloader.avatarcsvloader('C:/Users/endyd/OneDrive/Onedrive-CK/OneDrive/Gradschool/Kaist/AVATAR/AVATAR_DATA_SET/1.OFT(WT-N=50)/raw/','H1.mat.csv_new')
# print(data)

# testdata = adv_load.Easyavatarload(mode='Avatar')
testdata = adv_load.Easyfolderload('General')
print(testdata[3])