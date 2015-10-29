import os

    def path_newIcon(self, nameIcon):
        suffix = 0
        pathIcon = 'icons/'+nameIcon + '.png'
        while os.path.isfile(pathIcon):
            #print os.path.isfile(pathIcon), suffix, pathIcon
            suffix += 1
            pathIcon = 'icons/'+nameIcon + '_' + str(suffix) + '.png'
        return pathIcon

path_newIcon('94')