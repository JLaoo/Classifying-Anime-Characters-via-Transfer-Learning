import cv2
import sys
import os.path

#create folders
if not os.path.exists('images/cropped'):
    os.makedirs('images/cropped')
folder_names = ['ahagon_umiko', 'hazuki_shizuku', 'lijima_yun', 'sakura_nene', 'suzukaze_aoba', 'takimoto_hifumi', 'toyama_rin', 'yagami_kou']
for name in folder_names:
    if not os.path.exists('images/cropped/'+str(name)):
        os.makedirs('images/cropped/'+str(name))

#function to detect, crop, and save faces
def detect(save_as, filename, cascade_file = "lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    if image is not None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor = 1.1,
                                         minNeighbors = 5,
                                         minSize = (24, 24))
        for (x, y, w, h) in faces:
            crop_img = image[y:y+h, x:x+w]
            cv2.imwrite(save_as, crop_img)

#use detect to crop and save images
dir_names = ['ahagon_umiko', 'hazuki_shizuku', 'lijima_yun', 'sakura_nene', 'suzukaze_aoba', 'takimoto_hifumi', 'toyama_rin', 'yagami_kou']
for dir_name in dir_names:
    rootdir = 'images/raw/'+dir_name
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            detect('images/cropped/'+dir_name+'/'+str(file), os.path.join(subdir, file))

