#!/usr/bin/env python3

# systray icon用
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image, ImageDraw, ImageFont
import PIL
# icon用画像作成用
import cv2 as cv
import numpy as np
# batteryなど取得用
import psutil
# system monitor window用
import PySimpleGUI as sg
# Threading
import threading
import time

thread_loop = True
g_bat = "1"
g_window_flag = True
thread_timer = ""
thread_window = ""

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
    global thread_window

    thread_loop = False
    thread_timer.join()
    thread_window.join()
    icon.stop()

def on_debug(icon, item):
    icon.icon =  cv2pil(get_battery_image())

def on_timer():
    global thread_loop
    global g_icon
    while thread_loop is True:
        g_icon.icon = cv2pil(get_battery_image_simple())
        time.sleep(1)

def toggle_system_monitor():
    global g_window_flag
    if g_window_flag is True:
        hide_system_monitor()
    else: # g_window_flag is False
        show_system_monitor()

def show_system_monitor():
    global g_window_flag
    g_window_flag = True

def hide_system_monitor():
    global g_window_flag
    g_window_flag = False

def main():
    global g_icon
    global thread_timer
    global thread_window

    _menu = menu(
        item('Toggle SystemMonitor', toggle_system_monitor, default=True),
        item('Show SystemMonitor', show_system_monitor),
        item('Hide SystemMonitor', hide_system_monitor),
        item('Exit', on_exit),
    )
    g_icon = icon('test', cv2pil(get_battery_image_simple()), menu=_menu)
    thread_timer = threading.Thread(target=on_timer)
    thread_timer.start()
    thread_window = threading.Thread(target=popup_monitor)
    thread_window.start()
    g_icon.run()

def popup_monitor():
    global thread_loop
    global g_window_flag

    alpha_val = 0.5 # 0~1
    layout = [
        # [sg.B('Exit', size = (12,3))],
        [sg.Text("your_titlebar_text", key='Row1')],
        [sg.Text("Counter", key='Row2')],
    ]
    # right_click_menu = ['&Right', ['Exit', 'PopupTest', 'invisible']]
    right_click_menu = ['&Right', ['PopupTest', 'invisible']]
    window = sg.Window('My window',
                        layout,
                        use_custom_titlebar = True,
                        no_titlebar=True,
                        size = (None, None),
                        resizable = False,
                        grab_anywhere=True,
                        keep_on_top=True,
                        right_click_menu=right_click_menu,
                        background_color='black',
                        transparent_color='black',
                        alpha_channel=alpha_val,
                        )

    while True:
        ### event proc ###
        event, values = window.read(timeout=1000) # msec
        if event in (None,'Exit') or thread_loop is False:
            break
        elif event in (None, 'PopupTest'):
            sg.popup('This is my first popup')
        elif event in (None, 'invisible'):
            g_window_flag = False
        elif event in (sg.TIMEOUT_KEY):
            ### Update text ###
            _cpu = psutil.cpu_percent()
            _mem = psutil.virtual_memory().percent
            _disk = psutil.disk_usage('/').percent
            _disk_free_g = str(psutil.disk_usage(path='/').free/1024/1024//1024)+" GB"
            _row1 = f"CPU: {_cpu}% RAM: {_mem}%"
            _row2 = f"Disk: {_disk}%({_disk_free_g} free)"

            window['Row1'].update(f"{_row1}")
            window['Row2'].update(f"{_row2}")
        
        # windows display config
        if g_window_flag is True:
            window.reappear()
        elif g_window_flag is False:
            window.disappear()

    window.close()

if __name__ == '__main__':
    main()
