# plot 2d matplotlib
# plot 3d miyavi
import wx
import numpy as np
import random

from Linear_Regression.ML_Panel import Panel_Plotting_Helper, Panel_Controller


class ML_Frame(wx.Frame):

    def __init__(self, parent, id):
	    self.w = 1080
	    self.h = 720
	    wx.Frame.__init__(self,parent, id, 'linear regression frame',
                style=wx.DEFAULT_FRAME_STYLE,
                size=(self.w, self.h))

	    #self.splitter = wx.SplitterWindow(self, size=self.GetSize())
		
	    self.panel_plotting_helper = Panel_Plotting_Helper(self)
	    self.panel_controller = Panel_Controller(self)


	    #self.splitter.SplitHorizontally(self.panel_plotting_helper, self.panel_controller)
	    sizer = wx.FlexGridSizer(2, 1, 10, 10)
	    sizer.Add(self.panel_plotting_helper, 1, wx.EXPAND | wx.ALL)
	    sizer.Add(self.panel_controller, 1, wx.EXPAND | wx.ALL)
	    sizer.AddGrowableRow(0, 0)
	    sizer.AddGrowableCol(0, 0)
	    self.SetSizer(sizer)
		
	    #self.Bind(wx.EVT_LEAVE_WINDOW, self.onLeave)	
	    #self.Bind(wx.EVT_MOTION, self.onMotion)	
	    self.Bind(wx.EVT_CLOSE, self.handle_close)
			
    def handle_close(self, evt):
        dlg = wx.MessageDialog(self, 
             "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
			
    def onMotion(self, mouseevt):
        w, h = self.panel_plotting_helper.canvas.GetSize()
        print(w, mouseevt.x, h, mouseevt.y)		
    	if mouseevt.x in range(0, int(w+1)) and mouseevt.y in range(0, int(h+1)):
            pass
        else:			
            self.panel_plotting_helper.status.SetValue('')	
			
    def onLeave(self, mouseevt):
        self.panel_plotting_helper.status.SetValue('')			
	

if __name__ == '__main__':
    mlframe = ML_Frame(parent=None, id=-1)
    print(mlframe)
    