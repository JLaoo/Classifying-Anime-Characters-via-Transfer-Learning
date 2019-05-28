import cv2
import os
import sys

#create folders
if not os.path.exists('images/resized'):
    os.makedirs('images/resized')
folder_names = ['ahagon_umiko', 'hazuki_shizuku', 'lijima_yun', 'sakura_nene', 'suzukaze_aoba', 'takimoto_hifumi', 'toyama_rin', 'yagami_kou']
for name in folder_names:
    if not os.path.exists('images/resized/'+str(name)):
        os.makedirs('images/resized/'+str(name))

#function to resize and save images
def resize(save_as, path):
    image = cv2.imread(path)
    resized = cv2.resize(image, (96, 96), interpolation=cv2.INTER_AREA)
    cv2.imwrite(save_as, resized)

#resize and save images
dir_names = ['ahagon_umiko', 'hazuki_shizuku', 'lijima_yun', 'sakura_nene', 'suzukaze_aoba', 'takimoto_hifumi', 'toyama_rin', 'yagami_kou']
for dir_name in dir_names:
    rootdir = 'images/cropped/'+dir_name
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            resize('images/resized/'+dir_name+'/'+str(file), os.path.join(subdir, file))

