import threading
from win32api import *
from win32gui import *
from _winreg import *
import win32con
import sys, os
import time,random
import win32console,win32gui,ctypes

class WindowsBalloonTip:
    def __init__(self, title, msg):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "balloontip.ico" ))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(self.hwnd)

        # must unregister class if you want to open more than 1 balloon tip
        classAtom = UnregisterClass(classAtom, hinst)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.
    

def main():
    threading.Timer(1200, main).start()
    data=[
    "Boss close your eyes for 10 seconds and look some where else :)",
    "Hey dude, close your eyes",
    "Relax dude, close your eyes",
    "Abe yar, relax",
    "Get up and walk for a minute",
    "Go and drink some water"
    ]
    w=WindowsBalloonTip("Eye Care", random.choice(data))

def addStartup():
    fp=os.path.dirname(os.path.realpath(__file__))
    file_name=sys.argv[0].split("\\")[-1]
    new_file_path=fp+"\\"+file_name
    keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'

    key2change= OpenKey(HKEY_CURRENT_USER,
    keyVal,0,KEY_ALL_ACCESS)

    SetValueEx(key2change, "Eye Care",0,REG_SZ, new_file_path)

def hide():
    window = win32console.GetConsoleWindow()
    win32gui.ShowWindow(window,0)
    ctypes.windll.kernel32.SetConsoleTitleA("Eye Care")

if __name__ == '__main__':
    addStartup()
    hide()
    main()