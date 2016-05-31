# Test data
# Choose file loading and update LR
# Update Plotting with Traits UI
# Update y with Traits UI
import sys

import wx

# Add the ptdraft folder path to the sys.path list
# sys.path.append('./../Machine_Learning')
# sys.path.append('./Linear_Regression')

from ML_Frame import ML_Frame


class ML_UI(wx.App):

    def OnInit(self):
        self.mlframe = ML_Frame(parent=None, id=-1)
        self.SetTopWindow(self.mlframe)
        return True


if __name__ == '__main__':
    mlui = ML_UI()
    mlui.mlframe.Show()
    mlui.MainLoop()
