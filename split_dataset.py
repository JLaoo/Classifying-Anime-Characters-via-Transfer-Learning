import os
import cv2
import numpy as np

#create training and test folders
folder_names = ['ahagon_umiko', 'hazuki_shizuku', 'lijima_yun', 'sakura_nene', 'suzukaze_aoba', 'takimoto_hifumi', 'toyama_rin', 'yagami_kou']
if not os.path.exists('images/train_set'):
    os.makedirs('images/train_set')
for name in folder_names:
    if not os.path.exists('images/train_set/'+str(name)):
        os.makedirs('images/train_set/'+str(name))
if not os.path.exists('images/test_set'):
    os.makedirs('images/test_set')
for name in folder_names:
    if not os.path.exists('images/test_set/'+str(name)):
        os.makedirs('images/test_set/'+str(name))

#determine test set size
folder_names = ['ahagon_umiko', 'hazuki_shizuku', 'lijima_yun', 'sakura_nene', 'suzukaze_aoba', 'takimoto_hifumi', 'toyama_rin', 'yagami_kou']
num_files = []
for i in np.arange(8):
    folder_size = len(next(os.walk('./images/cleaned_resized/'+folder_names[i]))[2]) - 1
    num_files.append(folder_size)
train_size = [int(0.85 * x) for x in num_files]

#define function to resave images in specified path
def resave(save_as, path):
    image = cv2.imread(path)
    if image is not None:
        cv2.imwrite(save_as, image)

#populate test and train folders
for i in np.arange(len(folder_names)):
    rootdir = 'images/cleaned_resized/'+folder_names[i]
    img_count = 0
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if img_count < train_size[i]:
                resave('images/train_set/'+folder_names[i]+'/'+str(file), os.path.join(subdir, file))
            else:
                resave('images/test_set/'+folder_names[i]+'/'+str(file), os.path.join(subdir, file))
            img_count += 1

