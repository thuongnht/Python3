# load data
# run LR with Gradient descent
# run LR with Normal Equation
import pandas as pd
import numpy as np
from scipy import *

from Linear_Regression.Linear_Regression_Helper import Linear_Regression_Helper
from Logistic_Regression.Logistic_Regression_Helper import Logistic_Regression_Helper


class Machine_Learning_Tools(object):

    def __init__(self):
        self.methods = {
            'Linear_Regression': ['LrByGradientDescent', 'LrByNormalEquation'],
            'Logistic_Regression': ['LrByMinimizeCost', 'LrByMinimizeCostRegular']
        }
        pass

    def Setting(self, plotting_helper):
        self.ph = plotting_helper

    def LoadData(self, filename):
        dataFromFile = pd.read_csv(filename, delimiter=",", header=None, dtype=np.float32)
        numOfColumn = len(dataFromFile.axes[1])
        self.data = dataFromFile.iloc[:, :(numOfColumn-1)]
        self.target = dataFromFile.iloc[:, (numOfColumn-1):]
        self.features = [i for i in range(len(self.data.axes[1]))]
        print('New Dataset is loaded...')

    def LrByGradientDescent(self, data=None, target=None, apha=None, deg=None):
        lrh = Linear_Regression_Helper()
        # plotting data
        self.ph.make_figure('gd')

        self.Check_Data(data, target)

        self.ph.plot_data_gradient_descent(self.data.iloc[:, 0], self.target.iloc[:, 0], {"color": "red", \
                                                                                          "label": "Training Data"})
        self.result = lrh.Fit(self.data, self.target, 'gd')
        self.ph.plot_all_gradient_descent(self.result)

    def LrByNormalEquation(self, data=None, target=None, apha=None, deg=None):
        lrh = Linear_Regression_Helper()
        # plotting data
        self.ph.make_figure('ne')

        self.Check_Data(data, target)

        self.ph.plot_data_normal_equation(self.data.iloc[:, 0], self.target.iloc[:, 0], {"color": "red", \
                                                                                         "label": "Training Data"})
        self.result = lrh.Fit(self.data, self.target, 'ne')
        self.ph.plot_all_normal_equation(self.result)

    def LrByMinimizeCost(self, data=None, target=None, lbda=None, deg=None):
        lrh = Logistic_Regression_Helper()
        # plotting data
        # self.ph.make_figure('mc')

        self.Check_Data(data, target)

        # self.ph.plot_data_normal_equation(self.data.iloc[:, 0], self.target.iloc[:, 0], {"color": "red", \
        #                                                                                  "label": "Training Data"})
        self.result = lrh.Fit(self.data, self.target, 'mc')
        # self.ph.plot_all_normal_equation(self.result)
        pass

    def LrByMinimizeCostRegular(self, data=None, target=None, lbda=None, deg=None):
        lrh = Logistic_Regression_Helper()
        # plotting data
        #self.ph.make_figure('mc')

        self.Check_Data(data, target)

        #self.ph.plot_data_normal_equation(self.data.iloc[:, 0], self.target.iloc[:, 0], {"color": "red", \
        #                                                                                 "label": "Training Data"})
        if lbda and deg:
            self.result = lrh.Fit(self.data, self.target, 'mcr', lbda, deg)
        else:
            self.result = lrh.Fit(self.data, self.target, 'mcr', 1.0, 6)
        #self.ph.plot_all_normal_equation(self.result)


        pass

    def Check_Data(self, data=None, target=None):
        if not data or not target:
            print("Using the loaded dataset!!!")
        else:
            if type(data) in (list, tuple, np.ndarray) and type(target) in (list, tuple, np.ndarray):
                print("Dataset is OK!")
                self.data = data
                self.target = target
            else:
                print("Dataset is not OK! Must be array or ndarray")
                return


if __name__ == '__main__':
    mlt = Machine_Learning_Tools()
    mlt.LoadData('Machine_Learning/Logistic_Regression/ex2data1.txt')
    mlt.LrByMinimizeCost()
    mlt.LoadData('Machine_Learning/Logistic_Regression/ex2data2.txt')
    mlt.LrByMinimizeCostRegular(None, None, 1.0, 6)
