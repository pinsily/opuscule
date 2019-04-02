import urllib.request
import re
import sys
import os
import time
import json
import win32api, win32con, win32gui
from PIL import Image
import random

# 根目录位置
base_path = "D:\\Wallpaper\\"

# 设置桌面时需要用到bmp位图
bmp_file = ""


def get_bing_backphoto():
    """get and save biying photo


    必应图片信息url ：/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1361089515117&FORM=HYLH1
    通过修改 idx 参数值随机生成图片链接
    """
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    # 加入循环，防止链接失效
    for i in range(0,10):
        num = random.randint(1,10)
        url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx='+str(num)+'&n=1&nc=1361089515117&FORM=HYLH1'
        resp = urllib.request.urlopen(url)
        html = resp.read()
        resp.close()        # 防止多个连接导致服务器识别到爬虫

        # 链接失效，重新循环爬取图片信息
        if html == 'null':
            print( 'open & read bing error!')
            continue

        # 返回的图片信息是 json 格式
        photo_info = json.loads(html)
        photo_url = photo_info['images'][0]['url'].replace('/az/','http://cn.bing.com/az/')
        photo_marked = photo_info['images'][0]['copyright']
        

        # 使用链接来获取名字
        photo_name = photo_url[photo_url.rindex("/")+1:photo_url.index("_")]
        bmp_file = "{0}.bmp".format(photo_name)
        photo_name = "{0}.jpg".format(photo_name)

        jpg_name = base_path+photo_name
        bmp_name = base_path+bmp_file

        print('-'*20)
        print("\n")
        print("---- photo downloading ----")
        print("---- photo_address is {0}".format(photo_url))
        print("---- photo_name is {0}".format(photo_name))
        # print(photo_marked)
        # print(jpg_name)

        if os.path.exists(jpg_name) == False:
            urllib.request.urlretrieve(photo_url, jpg_name)
            print("---- Photo download success ----\n")
        else:
            print("---- file is existing, skip download ----\n")
        

        img = Image.open(jpg_name)
        # print(img)
        img.save(bmp_name)

        print('-'*20)

        set_wallpaper(bmp_name)
        break

        

        # else:
        #     html = html.decode('utf-8')
        #     html = html.replace('/az/','http://cn.bing.com/az/')
        #     reg = re.compile('"url":"(.*?)","urlbase"',re.S)
        #     text = re.findall(reg,html)

        #     for imgurl in text:
        #         right = imgurl.rindex('/')
        #         print(imgurl)
        #         name = imgurl.replace(imgurl[:right+1],'')
        #         savepath = 'pictures/'+ name
        #         urllib.request.urlretrieve(imgurl, savepath)
        #         print (name + ' save success!')

        time.sleep(5)

def set_wallpaper(bmpFile):
    print("\n\n")
    print("*"*20)
    print('\n**** setting wallpaper ****\n')
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    #2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmpFile, 1+2)
    print('**** set wallpaper success ****\n')
    print("*"*20)

get_bing_backphoto()