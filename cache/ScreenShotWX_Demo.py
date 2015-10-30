
"""
Demo app for ScreenShotWX.py

1) Capture the entire main screen; 
2) Capture 4 arbitrary (1/16th area) portions of the main screen.


Ray Pasco
pascor(at)verizon.net
2011-06-06

"""
import sys
import wx

import ScreenShotWX as ssw

#------------------------------------------------------------------------------

def WhatsInstalled() :

    # What Python and wxPython versions are installed ?
    import os, platform
    
    if os.name == 'nt' :
        print 'Windows  ', platform.win32_ver()[1]
    else :
        print 'Platform ', platform.system()
    #end if
    print 'Python   ', sys.version
    addon_pkgs = [ ('Wx Version',  'wx.VERSION_STRING'),
                   ('Wx Platform', 'wx.PlatformInfo'),  ]
                   
    for addonStr, attribute in addon_pkgs :
        try :
            print addonStr, eval( attribute )
        except NameError :
            print
    #end for
    
#end WhatsInstalled def

#==============================================================================

if __name__ == '__main__' :
    """
    1) Capture the entire main screen; 
    2) Capture 4 arbitrary (1/16th area) portions of the main screen.
    Save all shots to separate files.
    """
    WhatsInstalled()    # Print this platform's Python and wxPython versions.
    
    # Need to access WX functionality without using MainLoop().
    thisApp = wx.App( redirect=False )
    
    """
    The primary desktop screen area excluding the Taskbar.
    This isn't implemented in MSW WX Version 2.8.11.0
        captureBmapSize = wx.Display( 1 ).GetClientArea()   
    """
    
    # Capture the entire primary Desktop screen.
    captureBmapSize = (wx.SystemSettings.GetMetric( wx.SYS_SCREEN_X ), 
                       wx.SystemSettings.GetMetric( wx.SYS_SCREEN_Y ) )
    print '>>>>  Screen Size ', captureBmapSize
    
    captureStartPos = (0, 0)    # Arbitrary U-L position anywhere within the screen
    bitmap = ssw.ScreenCapture( captureStartPos, captureBmapSize )
    
    fileBasename = 'ScreenShotWX_Demo'
    fileExt = '.png'
    filename = fileBasename + '_WholeScreen' + fileExt
    print '     ', filename
    bitmap.SaveFile( filename, wx.BITMAP_TYPE_PNG )
    
    #----------------------------------
    
    """
    Take 4 small screenshots for demonstration purposes. 
    Each will be 1/16th of the screen area
      on a diagonal path from the U-L to the Lower-Right of the main screen.
    
    Apparently, wx.SYS_SCREEN_X and  wx.SYS_SCREEN_Y only apply to the main screen
      and not to any Exrended Desktop. 
      Use wx.Display( n ) to query any extended Desktop screen sizes.
    """
    numShots = 4
    shotBitmapSize = (wx.SystemSettings.GetMetric( wx.SYS_SCREEN_X ) / numShots,
                      wx.SystemSettings.GetMetric( wx.SYS_SCREEN_Y ) / numShots  )
    print '\n>>>>  shotBitmapSize', shotBitmapSize
    
    ## On my system there's an extended Desktop screen above the primary screen.
    ## It happens to have the same geometry as the main screen (but this isn't required).
    ## So, screen shots can be made there simply by using negative Y ordinate values:
    #startPos = (0, -800)     # First shot will start in the upper-left extension screen corner.
    
    # Capture portions of the main screen:
    startPos = (0, 0)     # First shot origin is at the upper-left corner of the main screen.
    for shotCtr in range( numShots ) :
        
        print '----  startPos', startPos
        
        bitmap = ssw.ScreenCapture( startPos, shotBitmapSize )
        
        filename = "%s_%i%s" % (fileBasename, shotCtr, fileExt)
        print '     ', filename
        bitmap.SaveFile( filename, wx.BITMAP_TYPE_PNG )
        
        # Increment the starting Coordinate.
        startPos = tuple( [i + j for i, j  in zip( startPos, shotBitmapSize ) ] ) 
        print
        
    #end for
    
#end if __name__
