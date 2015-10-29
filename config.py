# -*- coding: utf-8 -*-
# ShuffleIR的设置文件
#===============================================
# ShuffleMove的安装路径
pathShuffleMove = '../../Shuffle-Move/'

# 当前关卡在ShuffleMove中的关卡ID
# 例如美梦天梯为 'SP_275', Mega超梦为'150'
# 注意要有英文单引号！
varStageID = 'SP_275'

# 支援精灵列表
# 格式为 listSupport = ('口袋妖怪的NationDex #',...)
# 注意要有英文单引号！
# 特殊的条目包括 空白'Air', 铁块'Metal', 木块'Wood', 金币'Coin'
# Mega 精灵请在Dex后加 -m, 例如Mega化石翼龙为 '142-m'
# 已支援图标列表请参考Supported_Icons.md
listSupport=['Air','Wood','150-m','249','488','494']

# 是否载入冰封版图标(0为不载入, 1为载入)
varIceSupport=True

# 铁块计数器
varMetalTimer=3
#===============================================
# 以下设置用于确定Miiverse截图选区

# 消消乐方块区域在窗口截图内部的相对坐标(x1, y1, x2, y2)
# 其中(x1, y1)为左上坐标，(x2, y2) 为右下坐标
#varBox = (46, 6, 274, 234) # Old 3DS XL
varBox = (38,376,494,832) # iPhone 6p + Airserver

#===============================================
# 以下内容最好不要修改


# Path to Mask
pathMask =  'images/block_mask76.png'


# Board实际路径
pathBoard = pathShuffleMove + '/config/boards/board.txt'


#BlockSize = 38

BlockSize = 76
