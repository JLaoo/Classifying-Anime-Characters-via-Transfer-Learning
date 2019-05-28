
import os
import requests
import shutil
import numpy as np
import pandas as pd
from lxml import html

#make image folders
if not os.path.exists('images'):
    os.makedirs('images')
if not os.path.exists('images/raw'):
    os.makedirs('images/raw')
folder_names = ['ahagon_umiko', 'hazuki_shizuku', 'lijima_yun', 'sakura_nene', 'suzukaze_aoba', 'takimoto_hifumi', 'toyama_rin', 'yagami_kou']
for name in folder_names:
    if not os.path.exists('images/raw/'+str(name)):
        os.makedirs('images/raw/'+str(name))

#scraping locations of images from safebooru
pages = [0, 40, 80]
hifumi_base = 'https://safebooru.org/index.php?page=post&s=list&tags=takimoto_hifumi+sort%3Ascore+-animated&pid='
kou_base = 'https://safebooru.org/index.php?page=post&s=list&tags=yagami_kou+sort%3Ascore+-animated&pid='
aoba_base = 'https://safebooru.org/index.php?page=post&s=list&tags=suzukaze_aoba+sort%3Ascore+-animated&pid='
umiko_base = 'https://safebooru.org/index.php?page=post&s=list&tags=ahagon_umiko+sort%3Ascore+-animated&pid='
shizuku_base = 'https://safebooru.org/index.php?page=post&s=list&tags=hazuki_shizuku+sort%3ascore+-animated&pid='
nene_base = 'https://safebooru.org/index.php?page=post&s=list&tags=sakura_nene+sort%3Ascore+-animated&pid='
rin_base = 'https://safebooru.org/index.php?page=post&s=list&tags=tooyama_rin+sort%3Ascore+-animated&pid='
yun_base = 'https://safebooru.org/index.php?page=post&s=list&tags=iijima_yun+sort%3Ascore+-animated&pid='
base_lst = [hifumi_base, kou_base, aoba_base, umiko_base, shizuku_base, nene_base, rin_base, yun_base]
location_urls = [[] for x in range(8)]
current_waifu = 0
for base in base_lst:
    for page in pages:
        url = base+str(page)
        page = requests.get(url)
        tree = html.fromstring(page.content)
        for href in tree.xpath('//a/@href'):
            if len(href) > 30 and href[:30] == 'index.php?page=post&s=view&id=':
                location_urls[current_waifu].append('https://safebooru.org/index.php?page=post&s=view&id='+href[30:])
    current_waifu += 1

#downloading images
img_urls = [[] for x in range(8)]
hifumi_count, kou_count, aoba_count, umiko_count, shizuku_count, nene_count, rin_count, yun_count = 0, 0, 0, 0, 0, 0, 0, 0
for i in np.arange(8):
    for loc in location_urls[i]:
        page = requests.get(loc)
        tree = html.fromstring(page.content)
        img = 'http:'+tree.xpath('//*[@id="image"]/@src')[0]
        pic_request = requests.get(img)
        response = requests.get(img, stream=True)
        if i == 0:
            with open('images/raw/takimoto_hifumi/'+str(hifumi_count)+'.jpg' , 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            hifumi_count += 1
        elif i == 1:
            with open('images/raw/yagami_kou/'+str(kou_count)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            kou_count += 1
        elif i == 2:
            with open('images/raw/suzukaze_aoba/'+str(aoba_count)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            aoba_count += 1
        elif i == 3:
            with open('images/raw/ahagon_umiko/'+str(umiko_count)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            umiko_count += 1
        elif i == 4:
            with open('images/raw/hazuki_shizuku/'+str(shizuku_count)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            shizuku_count += 1
        elif i == 5:
            with open('images/raw/sakura_nene/'+str(nene_count)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            nene_count += 1
        elif i == 6:
            with open('images/raw/toyama_rin/'+str(rin_count)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            rin_count += 1
        else:
            with open('images/raw/lijima_yun/'+str(yun_count)+'.jpg', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            yun_count += 1