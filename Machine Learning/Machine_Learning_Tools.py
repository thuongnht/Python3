# load data
# run LR with Gradient descent
# run LR with Normal Equation
import pandas as pd
import numpy as np
from scipy import *
import threading
import time

from Linear_Regression.Linear_Regression_Helper import Linear_Regression_Helper

import wx
from Linear_Regression.ML_Frame import ML_Frame


class Machine_Learning_Tools(object):

    def __init__(self, plotting_helper):
	    self.ph = plotting_helper
	    self.loadData('./Linear_Regression/ex1data2.txt')
	
    def loadData(self, filename):
	    dataFromFile = pd.read_csv(filename, delimiter=",", header=None)
	    numOfColumn = len(dataFromFile.axes[1])
	    self.data = dataFromFile.iloc[:,:(numOfColumn-1)]
	    self.target = dataFromFile.iloc[:,(numOfColumn-1):]
	
    def lrByGradientDescent(self, data=None, target=None):
	    lrh = Linear_Regression_Helper()
	    # plotting data
	    self.ph.make_figure('gd')

	    if (not data or not target):
		    print("Using the default dataset!!!")
	    else:
		    if (type(data) in (list, tuple, np.ndarray) and type(target) in (list, tuple, np.ndarray)):
		        print("Dataset is OK!")
		        self.data = data
		        self.target = target
		    else:
		        print("Dataset is not OK! Must be array or ndarray")
		        return
	    
	    self.ph.plot_data_gradient_descent(self.data.iloc[:,0], self.target.iloc[:,0], {"color": "red", "label": "Training Data"})
	    result = lrh.fit(self.data, self.target, 'gd')
	    self.ph.plot_all_gradient_descent(result)
	
    def lrByNormalEquation(self, data=None, target=None):
	    lrh = Linear_Regression_Helper()
	    # plotting data
	    self.ph.make_figure('ne')
		
	    if (not data or not target):
		    print("Using the default dataset!!!")
	    else:
		    if (type(data) in (list, tuple, np.ndarray) and type(target) in (list, tuple, np.ndarray)):
		        print("Dataset is OK!")
		        self.data = data
		        self.target = target
		    else:
		        print("Dataset is not OK! Must be array or ndarray")
		        return
		
	    self.ph.plot_data_normal_equation(self.data.iloc[:,0], self.target.iloc[:,0], {"color": "red", "label": "Training Data"})
	    result = lrh.fit(self.data, self.target, 'ne')
	    self.ph.plot_all_normal_equation(result)
		
    def do_stuff(self, stuff):
	    start = time.time()
	    if (stuff == 'gd'):
		    self.lrByGradientDescent()
	    elif (stuff == 'ne'):
		    self.lrByNormalEquation()
	    end = time.time()
	    print("%s: %s sec" % ( stuff, end-start ))
	

if __name__ == '__main__':
    app = wx.PySimpleApp()
    mlframe = ML_Frame(parent=None, id=-1)
    app.SetTopWindow(mlframe)
    mlt = Machine_Learning_Tools(mlframe.panel_plotting_helper)
    try:
	    jobs = []
	    thread = threading.Thread(target=mlt.do_stuff('gd'))
	    jobs.append(thread)
	    thread = threading.Thread(target=mlt.do_stuff('ne'))
	    jobs.append(thread)
	    # Start the threads (i.e. calculate the random number lists)
	    for j in jobs:
		    j.start()
	    # Ensure all of the threads have finished
	    for j in jobs:
		    j.join()
	    mlframe.Show()
	    app.MainLoop()
	    print("List processing complete.")
    except ValueError:
	    print("Error: unable to start thread %r" % ValueError)


