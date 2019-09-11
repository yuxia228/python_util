#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# icon用
import wx
import wx.adv
# icon用画像作成用
import cv2 as cv
import numpy as np
# battery取得用
import psutil

class batIcon(wx.Frame):
    def __init__(self, *args, **kw):
        super(batIcon, self).__init__(*args, **kw)
        # taskbar_icon
        self.taskbar_icon = wx.adv.TaskBarIcon()
        self.taskbar_text = u"battery_indicator"
        ## 右クリックメニュー
        self.taskbar_menu = wx.Menu()
        self.EVENT_EXIT = 1
        self.taskbar_menu.Append( self.EVENT_EXIT, item="Exit", helpString="help")
        self.taskbar_menu.Bind(wx.EVT_MENU, self.OnMenu, id=self.EVENT_EXIT)
        self.taskbar_icon.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnTaskbarRightUp)
        # timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(3000)
        self.OnTimer(None)

        # window非表示
        self.Show(False)

    def OnTimer(self, event):
        img = get_battery_image()
        img = cv.cvtColor(img, cv.COLOR_BGR2RGBA)
        # bmp = wx.Bitmap.FromBuffer(img.shape[1], img.shape[0], img)
        bmp = wx.Bitmap.FromBufferRGBA(img.shape[1], img.shape[0], img)
        self.taskbar_icon.SetIcon( wx.Icon( bmp ), self.taskbar_text)
        pass

    def OnMenu(self, event):
        id = event.GetId()
        print("hello", id )
        if id == self.EVENT_EXIT:
            print("hello OnExit")
            self.OnClose(event)
        # self.Close()

    def OnClose(self, event):
        print("onClose")
        self.taskbar_icon.RemoveIcon()
        wx.Exit()

    def OnTaskbarRightUp(self, event):
        self.taskbar_icon.PopupMenu(self.taskbar_menu)
        pass
  
def get_battery_image():
    size = (64, 64*1, 4) # 64(高さ) x 64(幅)　4レイヤー(BGRA)を定義
    img = np.zeros(size, dtype=np.uint8) # 空の配列
    
    #バッテリー残量
    btr = psutil.sensors_battery()
    battery = btr.percent # 0~100
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


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = batIcon(None, title='battery_icon')
    # frm.Show(False) # True/False Show/Hide
    app.MainLoop()
