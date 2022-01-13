#!/usr/bin/env python3

# systray icon用
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageFont
import PIL
# icon用画像作成用
import cv2 as cv
import numpy as np
# battery取得用
import psutil
# Threading
import threading
import time

thread_loop = True
g_bat = "1"

def cv2pil(image_cv):
    image_cv = cv.cvtColor(image_cv, cv.COLOR_BGRA2RGBA)
    image_pil = Image.fromarray(image_cv)
    image_pil = image_pil.convert('RGBA')
    return image_pil

def get_battery_image():
    size = (64, 64*1, 4) # 64(高さ) x 64(幅)　4レイヤー(BGRA)を定義
    img = np.zeros(size, dtype=np.uint8) # 空の配列
    
    #バッテリー残量
    btr = psutil.sensors_battery()
    try:
        battery = btr.percent # 0~100
    except:
        print("No battery on this system.")
        quit()
    bat_text = "{:d}".format(battery)
    color=(0,0,0)
    if battery >= 60:
        color = (50, 200, 50, 255) # green
    elif battery <= 30:
        color = (10, 10, 220, 255) # red 
    else:
        color = (30, 200, 200, 255) # yellow
    # img, center radius, base_angle, start, end, color, (thickness) 
    bat = 360*battery//100
    fontcolor = (200,200,200, 255)
    if btr.power_plugged == True: # 充電中は色を変える
        fontcolor = (100,240,240, 255)
    cv.ellipse(img, (32, 32), (30, 30), 270-bat, 0, bat, color, 6)
    
    # 画像，テキスト，位置（左下），フォント，スケール，色，線太さ，種類
    if len(bat_text) == 3: ## 3桁(100)
        cv.putText(img, bat_text, ( 1,43), cv.FONT_HERSHEY_SIMPLEX, 1.0, fontcolor, 3, cv.LINE_AA)
    elif len(bat_text) == 2: ## 2桁
        cv.putText(img, bat_text, ( 8,45), cv.FONT_HERSHEY_SIMPLEX, 1.2, fontcolor, 4, cv.LINE_AA)
    elif len(bat_text) == 1: ## 1桁
        cv.putText(img, bat_text, ( 20,45), cv.FONT_HERSHEY_SIMPLEX, 1.2, fontcolor, 4, cv.LINE_AA)
    return img

def get_battery_image_simple():
    global g_bat
    size = (64, 64*1, 4) # 64(高さ) x 64(幅)　4レイヤー(BGRA)を定義
    img = np.zeros(size, dtype=np.uint8) # 空の配列
    
    #バッテリー残量
    btr = psutil.sensors_battery()
    try:
        battery = btr.percent # 0~100
    except:
        print("No battery on this system.")
        quit()
    bat_text = "{:d}".format(battery)
    color=(0,0,0)
    if battery >= 60:
        color = (50, 200, 50, 255) # green
    elif battery <= 30:
        color = (10, 10, 220, 255) # red 
    else:
        color = (30, 200, 200, 255) # yellow
    # img, center radius, base_angle, start, end, color, (thickness) 
    bat = 360*battery//100
    fontcolor = (200,200,200, 255)
    if btr.power_plugged == True: # 充電中は色を変える
        fontcolor = (100,240,240, 255)
    # cv.ellipse(img, (32, 32), (30, 30), 270-bat, 0, bat, color, 6)
    
    # 画像，テキスト，位置（左下），フォント，スケール，色，線太さ，種類
    if len(bat_text) == 3: ## 3桁(100)
        cv.putText(img, bat_text, ( -14,43), cv.FONT_HERSHEY_SIMPLEX, 1.3, fontcolor, 3, cv.LINE_AA)
    elif len(bat_text) == 2: ## 2桁
        cv.putText(img, bat_text, ( 8,45), cv.FONT_HERSHEY_SIMPLEX, 1.5, fontcolor, 4, cv.LINE_AA)
    elif len(bat_text) == 1: ## 1桁
        cv.putText(img, bat_text, ( 20,45), cv.FONT_HERSHEY_SIMPLEX, 1.5, fontcolor, 4, cv.LINE_AA)
    return img

def on_exit(icon, item):
    global thread_loop
    global thread_timer
    thread_loop = False
    thread_timer.join()
    icon.stop()

def on_debug(icon, item):
    icon.icon =  cv2pil(get_battery_image())

def on_timer():
    global thread_loop
    global g_icon
    while thread_loop is True:
        g_icon.icon = cv2pil(get_battery_image_simple())
        time.sleep(1)

_menu = menu(
    item('Debug', on_debug),
    item('Exit', on_exit)
)
g_icon = icon('test', cv2pil(get_battery_image_simple()), menu=_menu)
thread_timer = threading.Thread(target=on_timer)
thread_timer.start()
g_icon.run()
