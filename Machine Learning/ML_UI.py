# Test data
# Choose file loading and update LR
# Update Plotting with Traits UI
# Update y with Traits UI
from Machine_Learning_Tools import Machine_Learning_Tools
import threading
import wx
	
from Linear_Regression.ML_Frame import ML_Frame
	

class ML_UI(wx.App):
	
    def OnInit(self):
        self.mlframe = ML_Frame(parent=None, id=-1)
        self.SetTopWindow(self.mlframe)
        self.mlt = Machine_Learning_Tools(self.mlframe.panel_plotting_helper)
        return True
				
    #@on_trait_change()
    def update_target(self):
        pass
		
    def run_thread(self):
        try:
            jobs = []
            thread = threading.Thread(target=self.mlt.do_stuff('gd'))
            jobs.append(thread)
            #thread = threading.Thread(target=self.mlt.do_stuff('ne'))
            #jobs.append(thread)
            # Start the threads (i.e. calculate the random number lists)
            for j in jobs:
                j.start()
            # Ensure all of the threads have finished
            for j in jobs:
                j.join()
            print("List processing complete.")
        except ValueError:
            print("Error: unable to start thread %r" % ValueError)
	

if __name__ == '__main__':
    mlui = ML_UI()
    mlui.run_thread()
    mlui.mlframe.Show()
    mlui.MainLoop()
	