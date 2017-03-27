#!/usr/bin/python


from time import gmtime, strftime
import os
from tkinter import *
import win32gui
import win32ui
import win32con
from win32gui import GetWindowText, GetForegroundWindow


class Area(object):

    def __init__(self, point1 = 0, point2 = 0):
        
        self.start = point1
        self.end = point2

    def startCoord(self, event):
        
        self.start = [event.x, event.y]

    def endCoord(self, event):
        
        self.end = [event.x, event.y]
        
        if (self.start[0] > self.end[0]):
            self.end[0], self.start[0] = self.start[0], self.end[0]
            
        if (self.start[1] > self.end[1]):
            self.end[1], self.start[1] = self.start[1], self.end[1]


        name = GetWindowText(GetForegroundWindow())

        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        global cDC
        cDC = dcObj.CreateCompatibleDC()
        global dataBitMap
        dataBitMap = win32ui.CreateBitmap()
            
        areaSize = GetSize(area.start, area.end)
        dataBitMap.CreateCompatibleBitmap(dcObj, areaSize.width, areaSize.height)
            
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (areaSize.width, areaSize.height), dcObj, (area.start[0], area.start[1]), win32con.SRCCOPY)
        
        d = Dialog(frame, "Save")
    
        # Free Resources
        win32gui.DeleteObject(dataBitMap.GetHandle())
        cDC.DeleteDC()
        dcObj.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
    ##    win32gui.DeleteObject(dataBitMap.GetHandle())   

class Dialog(Toplevel):

    def __init__(self, parent, title = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        
        return 1 # override

    def apply(self):

        SaveBmp(dataBitMap, cDC)
        pass # override

def GetSize(point1, point2):
    
    wHeight = point2[0] - point1[0]
    wWidth = point2[1] - point1[1]
    
    return WindowSize(wWidth, wHeight)

def hwndGetSize(hwnd):
    
    wSize = win32gui.GetWindowRect(hwnd)
    
    wHeight = wSize[2] - wSize[0]
    wWidth = wSize[3] - wSize[1]
    
    return WindowSize(wWidth, wHeight)

class WindowSize(object):
    
    height = 0
    width = 0

    def __init__(self, X, Y):
        
        self.height = X
        self.width = Y

def close(event):

    root.iconify()       

def SaveBmp(dataBitMap, cDC):

    bmpfilenamename =  strftime("%Y_%m_%d %H-%M-%S", gmtime()) + ".jpg" ## ".bmp"
    dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)





path = os.path.dirname(os.path.realpath(__file__)) + "/screenshots"

if not os.path.exists(path):
    os.makedirs(path)
    
os.chdir(path)

hwnd = win32gui.GetDesktopWindow()
wSize = hwndGetSize(hwnd)

root = Tk()
root.wm_title("scissors")
root.attributes("-alpha", 0.002)
root.attributes("-fullscreen", True)
##root.wm_attributes("-topmost", True)
##root.wm_attributes("-disabled", True)
##root.wm_attributes("-transparentcolor", "white")

frame = Frame(root, width= wSize.width, height= wSize.height)
area = Area()
frame.focus_set()
frame.bind("<Escape>", close)
frame.bind("<ButtonPress-1>", area.startCoord)
frame.bind("<ButtonRelease-1>", area.endCoord)
frame.pack()

root.mainloop()
