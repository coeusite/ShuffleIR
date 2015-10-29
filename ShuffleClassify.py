# -*- coding: utf-8 -*-
# python ShuffleClassify.py samples/WVW69ig4O90367uQIN.jpg

from PIL import Image           # PIL module. Only if you use the PIL library.
from ShuffleClassifier import ShuffleClassifier
import sys

import config

filepath = sys.argv[1]

image = Image.open(filepath)

image = image.crop(config.varBox)

# Load Classifier
mac = ShuffleClassifier()

#========================================

from dataNationalDex import list as listNationDex
import os

def try_support(nameIcon, namePokemon, typeIced='false'):
    pathIcon = 'icons/'+nameIcon + '.png'
    if os.path.isfile(pathIcon):
        varSupportList.append((nameIcon, namePokemon, typeIced))
        print("Loaded " + namePokemon + ": " +nameIcon)
    else:
        print("No icon found for path: "+pathIcon)
    # Try to Load Additional Icons
    
    pathIcon = 'icons/'+nameIcon + '_1.png'
    if os.path.isfile(pathIcon):
        varSupportList.append((nameIcon, namePokemon, typeIced))
        print("Loaded " + namePokemon + ": " +nameIcon + '_1')
        

# 自动生成实际资源列表
varSupportList = []

# 普通版Icon
for tmp in config.listSupport:
    try_support(tmp, listNationDex.get(tmp), 'false')
    # 载入冰封?
    if config.varIceSupport != 0:
        try_support(tmp + '-i', listNationDex.get(tmp), 'true')


#========================================

# Load Reference Icons
for tmp in varSupportList:
    mac.add_reference(tmp[0],tmp[1],tmp[2])

# Classify

# Import Image to Classifer
mac.load_image2(image)
mac.classify()
mac.write_board(config.varStageID, config.pathBoard)


quit()
