# -*- coding: utf-8 -*-

# import libListWindowsX11 as libListWindows
# libListWindows.listVisibleWindows()
# 

from Xlib.display import Display
from Xlib import X

listWindows = []

def listVisibleWindowsHierrarchy(window, indent):
    children = window.query_tree().children
    for win in children:
        name = win.get_wm_name()
        attrs = win.get_attributes()
        if attrs.map_state == X.IsViewable:
            #print win.id, indent, name
            listWindows.append((win.id, indent, name))
            listVisibleWindowsHierrarchy(win, indent+'-')
    
def listVisibleWindows():
    listWindows= []
    
    display = Display()
    root = display.screen().root
    listVisibleWindowsHierrarchy(root, '-')
    

def getBox(winID):
    dpy = Display()
    data = dpy.create_resource_object('window', winID).get_geometry()
    boxWin = (data.x, data.y, data.x + data.width, data.y + data.height)
    return boxWin