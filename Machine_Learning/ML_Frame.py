# plot 2d matplotlib
# plot 3d miyavi
import wx

from Linear_Regression.Panel_Plotting import Panel_Plotting_Helper as Linear_Plotting_Helper
from Logistic_Regression.Panel_Plotting import Panel_Plotting_Helper as Logistic_Plotting_Helper
from ML_Panel_Controller import Panel_Controller
from Machine_Learning_Tools import Machine_Learning_Tools


class ML_Frame(wx.Frame):

    def __init__(self, parent, id):
        self.w = 1080
        self.h = 720
        wx.Frame.__init__(self, parent, id, 'Machine Learning Frame',
                          style=wx.DEFAULT_FRAME_STYLE,
                          size=(self.w, self.h))

        self.menubar = wx.MenuBar()
        self.kindML = wx.Menu()
        menuitems = [
            [100, 'Linear_Regression'],
            [101, 'Logistic_Regression']
        ]
        for item in menuitems:
            menuitem = wx.MenuItem(self.kindML, item[0], text=item[1], kind=wx.ITEM_RADIO)
            self.kindML.AppendItem(menuitem)
            self.Bind(wx.EVT_MENU, self.on_menu_check, menuitem)

        self.menubar.Append(self.kindML, 'Choices For Machine Learning')
        self.SetMenuBar(self.menubar)

        self.mlt = Machine_Learning_Tools()
        self.set_panel('Linear_Regression')
        # self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        # self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_CLOSE, self.handle_close)

    def delete_attributes(self):
        if hasattr(self, 'sizer'):
            for child in self.GetChildren():
                child.Destroy()
                self.Layout()
            del self.sizer
            self.Refresh()
        else:
            pass
        if hasattr(self, 'panel_plotting_helper'):
            del self.panel_plotting_helper
        else:
            pass
        if hasattr(self, 'panel_controller'):
            del self.panel_controller
        else:
            pass
        if hasattr(self, 'statusbar'):
            del self.statusbar
        else:
            pass

    def set_panel(self, which):
        self.delete_attributes()
        if which == 'Linear_Regression':
            fileName = which + "/ex1data2.txt"
            self.panel_plotting_helper = Linear_Plotting_Helper(self)
        elif which == 'Logistic_Regression':
            fileName = which + "/ex2data1.txt"
            self.panel_plotting_helper = Logistic_Plotting_Helper(self)
        else:
            pass
        self.panel_controller = Panel_Controller(self)
        self.mlt.Setting(self.panel_plotting_helper)
        self.panel_controller.load_dataset(fileName)
        self.panel_controller.make_test_items(self.mlt.features)
        self.panel_controller.updated_algo_choice(self.mlt.methods[which])

        self.sizer = wx.FlexGridSizer(2, 1, 0, 0)
        self.sizer.Add(self.panel_plotting_helper, 1, wx.EXPAND | wx.ALL)
        self.sizer.Add(self.panel_controller, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.AddGrowableRow(0, 0)
        self.sizer.AddGrowableCol(0, 0)
        self.SetSizer(self.sizer)
        self.statusbar = self.CreateStatusBar()
        self.Layout()

    def handle_close(self, evt):
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
        else:
            pass

    def on_menu_check(self, evt):
        menu = evt.GetEventObject()
        menuitem = menu.FindItemById(evt.GetId())
        print(menuitem.GetText() + ' ...')
        self.set_panel(menuitem.GetText())

    def on_logistic_regression(self, evt):
        pass

    def on_motion(self, mouseevt):
        w, h = self.panel_plotting_helper.canvas.GetSize()
        print(w, mouseevt.x, h, mouseevt.y)
        if mouseevt.x in range(0, int(w+1)) and mouseevt.y in range(0, int(h+1)):
            pass
        else:
            self.panel_plotting_helper.status.SetValue('')

    def on_leave(self, mouseevt):
        self.panel_plotting_helper.status.SetValue('')


if __name__ == '__main__':
    mlframe = ML_Frame(parent=None, id=-1)
    print(mlframe)
