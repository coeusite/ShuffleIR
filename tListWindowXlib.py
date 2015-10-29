# -*- coding: utf-8 -*-

from Xlib.display import Display

def printWindowHierrarchy(window, indent):
    children = window.query_tree().children
    for w in children:
        print(indent, w.get_wm_name(),w.id)
        listWindowIDs.append(w.id)
        printWindowHierrarchy(w, indent+'-')

display = Display()
root = display.screen().root

listWindowIDs = []
#

printWindowHierrarchy(root, '-')