# load data
# run LR with Gradient descent
# run LR with Normal Equation
import pandas as pd
import numpy as np
from scipy import *
import threading
import time

import wx
from Linear_Regression.Linear_Regression_Helper import Linear_Regression_Helper


class Machine_Learning_Tools(object):

    def __init__(self, plotting_helper):
	    self.ph = plotting_helper
	    self.loadData('./Linear_Regression/ex1data2.txt')
	    self.algo_choices = [ 'lrByGradientDescent', 'lrByNormalEquation']
	
    def loadData(self, filename):
	    dataFromFile = pd.read_csv(filename, delimiter=",", header=None)
	    numOfColumn = len(dataFromFile.axes[1])
	    self.data = dataFromFile.iloc[:,:(numOfColumn-1)]
	    self.target = dataFromFile.iloc[:,(numOfColumn-1):]
	    self.features = [ 'X'+str(i) for i in range(len(self.data.axes[1])) ]
	
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
	    self.result = lrh.fit(self.data, self.target, 'gd')
	    self.ph.plot_all_gradient_descent(self.result)
	
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
	    self.result = lrh.fit(self.data, self.target, 'ne')
	    self.ph.plot_all_normal_equation(self.result)
		
    def do_stuff(self, stuff):
	    start = time.time()
	    if (stuff == 'gd'):
		    self.lrByGradientDescent()
	    elif (stuff == 'ne'):
		    self.lrByNormalEquation()
	    end = time.time()
	    print("Time consumed of %s: %s sec" % ( stuff, end-start ))
	

if __name__ == '__main__':
    mlt = Machine_Learning_Tools()
    print(mlt)	


