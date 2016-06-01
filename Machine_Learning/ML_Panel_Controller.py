import numpy as np
import os
import time

import matplotlib
matplotlib.interactive( True )
matplotlib.use( 'WXAgg' )

import wx
from wx.lib.stattext import GenStaticText
import wx.lib.scrolledpanel as scrolled


class Panel_Controller(scrolled.ScrolledPanel):

    def __init__(self, parent):
        w, h = parent.GetSize()
        scrolled.ScrolledPanel.__init__(self, parent=parent, size=(w, 0.2*h), style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour((210, 210, 210))

        self.parent = parent
        self.sample_algo_choice = []
        self.id = 0
        self.x_idx = -1
        self.kind = -1
        self.lbda = 1
        self.deg = 6

        self.make_items()

    def make_items(self):
        algo_title = GenStaticText(self, size=(150, -1), label=" Choose Algorithm: ", style=wx.ALIGN_RIGHT)
        algo_title.SetBackgroundColour((210, 210, 210))
        self.algo_choice = wx.ComboBox(self, self.id, choices=self.sample_algo_choice, style=wx.CB_READONLY)
        self.id += 1
        datasizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dataset = wx.Button(self, self.id, size=(150, -1), label="Load Dataset")
        self.id += 1
        datasizer.Add(self.dataset)
        self.subsizer1 = wx.BoxSizer(wx.VERTICAL)
        self.subsizer1.Add(datasizer, 0, wx.ALL, 5)
        subsubsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        subsubsizer1.Add(algo_title, 1)
        subsubsizer1.Add(self.algo_choice, 1)
        lambdasizer = wx.BoxSizer(wx.HORIZONTAL)
        self.lamnda_title = GenStaticText(self, size=(100, -1), label=" Lambda: ", style=wx.ALIGN_RIGHT)
        self.lamnda_title.SetBackgroundColour((210, 210, 210))
        self.show_lambda = wx.TextCtrl(self, self.id)
        self.show_lambda.SetBackgroundColour((210, 210, 210))
        self.id += 1
        self.run = wx.Button(self, self.id, size=(100, -1), label="Run")
        self.id += 1
        lambdasizer.Add(self.lamnda_title, 1)
        lambdasizer.Add(self.show_lambda, 1)
        lambdasizer.Add(self.run, 1)
        degreesizer = wx.BoxSizer(wx.HORIZONTAL)
        self.degree_title = GenStaticText(self, size=(100, -1), label=" Degree: ", style=wx.ALIGN_RIGHT)
        self.degree_title.SetBackgroundColour((210, 210, 210))
        self.show_degree = wx.TextCtrl(self, self.id)
        self.show_degree.SetBackgroundColour((210, 210, 210))
        self.id += 1
        degreesizer.Add(self.degree_title, 1)
        degreesizer.Add(self.show_degree, 1)
        self.subsizer1.Add(subsubsizer1, 0, wx.ALL, 5)
        self.subsizer1.Add(lambdasizer, 0, wx.ALL, 5)
        self.subsizer1.Add(degreesizer, 0, wx.ALL, 5)

        subsubsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        test_title = GenStaticText(self, size=(100, -1), label="Test Values:  ", style=wx.ALIGN_RIGHT)
        test_title.SetBackgroundColour((210, 210, 210))
        self.test_value = wx.TextCtrl(self, style=wx.CB_READONLY)
        self.test_value.SetBackgroundColour((210, 210, 210))
        subsubsizer2.Add(test_title, 1)
        subsubsizer2.Add(self.test_value, 4)
        self.subsizer2 = wx.BoxSizer(wx.VERTICAL)
        self.subsizer2.Add(subsubsizer2, 0, wx.ALL, 5)
        self.gensizer = wx.BoxSizer(wx.HORIZONTAL)
        x_values_title = GenStaticText(self, size=(100, -1), label=" X Values:  ", style=wx.ALIGN_RIGHT)
        x_values_title.SetBackgroundColour((210, 210, 210))
        self.show_x_values = wx.TextCtrl(self, self.id, style=wx.CB_READONLY)
        self.show_x_values.SetBackgroundColour((210, 210, 210))
        self.id += 1
        xvaluessizer = wx.BoxSizer(wx.HORIZONTAL)
        xvaluessizer.Add(x_values_title, 1)
        xvaluessizer.Add(self.show_x_values, 4)
        self.subsizer2.Add(xvaluessizer, 0, wx.ALL, 5)
        self.subsizer2.Add(self.gensizer, 0, wx.ALL, 5)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.subsizer1, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.subsizer2, 2, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetupScrolling()

        self.dataset.Bind(wx.EVT_BUTTON, self.on_load_dataset)
        self.run.Bind(wx.EVT_BUTTON, self.on_run_algo)
        self.algo_choice.Bind(wx.EVT_COMBOBOX, self.on_algo_changed)

    def make_test_items(self, features):
        self.alpha_title = GenStaticText(self, size=(100, -1), label="Choose Alpha:  ", style=wx.ALIGN_RIGHT)
        self.alpha_title.SetBackgroundColour((210, 210, 210))
        self.alpha_choice = wx.ComboBox(self, self.id, choices=[], style=wx.CB_READONLY)
        self.toggle_Coeffs([False, False])
        self.gensizer.Add(self.alpha_title, 1)
        self.gensizer.Add(self.alpha_choice, 1)
        self.id += 1

        self.sample_x_choice = ['X'+str(f+1) for f in features]
        x_title = GenStaticText(self, size=(100, -1), label="Choose X:  ", style=wx.ALIGN_RIGHT)
        x_title.SetBackgroundColour((210, 210, 210))
        self.x_values = np.zeros(len(features))
        self.x_choice = wx.ComboBox(self, self.id, choices=self.sample_x_choice, style=wx.CB_READONLY)
        self.id += 1
        self.x_value = wx.TextCtrl(self, self.id)
        self.x_value.SetBackgroundColour((210, 210, 210))
        self.id += 1
        self.gensizer.Add(x_title, 1)
        self.gensizer.Add(self.x_choice, 0)
        self.gensizer.Add(self.x_value, 1)

        self.alpha_choice.Bind(wx.EVT_COMBOBOX, self.on_alpha_choice_changed)
        self.x_value.Bind(wx.EVT_TEXT, self.on_x_value_changed)
        self.x_choice.Bind(wx.EVT_COMBOBOX, self.on_x_choice_changed)

    def updated_algo_choice(self, samples):
        self.sample_algo_choice = samples
        self.algo_choice.Clear()
        for sample in self.sample_algo_choice:
            self.algo_choice.Append(sample)

    def updated_alpha_choice(self, samples):
        self.sample_alpha_choice = samples
        self.alpha_choice.Clear()
        for sample in self.sample_alpha_choice:
            self.alpha_choice.Append(sample)

    def updated_x_choice(self, samples):
        self.sample_x_choice = ['X'+str(f+1) for f in samples]
        self.x_choice.Clear()
        for sample in self.sample_x_choice:
            self.x_choice.Append(sample)

    def on_load_dataset(self, evt):
        dirname = ""  # set directory name to blank
        dlg = wx.FileDialog(self, "Choose a file to open", dirname, "", "*.*", wx.OPEN)  # open the dialog boxto open file
        if dlg.ShowModal() == wx.ID_OK:  # if positive button selected....
            filename = dlg.GetFilename()  # get the filename of the file
            dirname = dlg.GetDirectory()  # get the directory of where file is located
            self.load_dataset(filename, dirname)
        else:
            pass
        dlg.Destroy()
        if self.parent.panel_plotting_helper:
            self.parent.panel_plotting_helper.fig.clf()
            self.parent.panel_plotting_helper.update_canvas()
        else:
            pass
        self.updated_x_choice(self.parent.mlt.features)
        self.x_values = np.zeros(len(self.parent.mlt.features))
        self.x_idx = -1
        self.kind = -1
        self.delete_attributes()

    def load_dataset(self, fileName, dirName=None):
        if dirName:
            self.parent.mlt.LoadData(os.path.join(dirName, fileName))  # traverse the file directory and find filename in the OS
        else:
            self.parent.mlt.LoadData(os.path.join(os.path.dirname(__file__), fileName))

    def on_algo_changed(self, evt):
        self.algo_idx = evt.GetSelection()
        if self.parent.mlt:
            self.do_stuff(self.algo_idx)
            self.delete_attributes()
            self.result = self.parent.mlt.result
            if self.sample_algo_choice[self.algo_idx] == 'LrByGradientDescent' and len(self.result.keys()) > 1:
                self.updated_alpha_choice(self.result.keys())
                self.toggle_Coeffs([True, False])
                self.kind = 0
            elif self.sample_algo_choice[self.algo_idx] == 'LrByNormalEquation':
                self.toggle_Coeffs([False, False])
                self.kind = 0
                self.theta = self.result['0']['theta']
                self.estimate_y()
            elif self.sample_algo_choice[self.algo_idx] == 'LrByMinimizeCost':
                self.toggle_Coeffs([False, False])
                self.kind = 1
                self.theta = self.result['0']['theta']
                self.instance = self.result['0']['instance']
                self.estimate_y()
            elif self.sample_algo_choice[self.algo_idx] == 'LrByMinimizeCostRegular':
                self.toggle_Coeffs([False, True])
                self.kind = 1
                self.show_lambda.SetValue(str(self.lbda))
                self.show_degree.SetValue(str(self.deg))
                self.theta = self.result['0']['theta']
                self.instance = self.result['0']['instance']
                self.estimate_y()
            else:
                self.toggle_Coeffs([False, False])
                self.kind = -1
        else:
            pass

    def delete_attributes(self):
        self.sample_alpha_choice = []
        self.x_choice.SetSelection(self.x_idx)
        self.x_value.SetValue(str(self.x_values[self.x_idx]))
        self.lbda = 1
        self.deg = 6
        if hasattr(self, 'theta'):
            del self.theta
        else:
            pass
        if hasattr(self, 'mean'):
            del self.mean
        else:
            pass
        if hasattr(self, 'std'):
            del self.std
        else:
            pass
        if hasattr(self, 'instance'):
            del self.instance
        else:
            pass
        self.show_x_values.SetValue('')
        self.test_value.SetValue('')
        self.parent.statusbar.SetStatusText('')

    def toggle_Coeffs(self, isShown):
        if isShown[0]:
            self.alpha_title.Enable()
            self.alpha_choice.Enable()
        else:
            self.alpha_title.Disable()
            self.alpha_choice.Disable()
        if isShown[1]:
            self.lamnda_title.Enable()
            self.show_lambda.Enable()
            self.run.Enable()
            self.degree_title.Enable()
            self.show_degree.Enable()
        else:
            self.lamnda_title.Disable()
            self.show_lambda.Disable()
            self.run.Disable()
            self.degree_title.Disable()
            self.show_degree.Disable()

    def on_alpha_choice_changed(self, evt):
        idx = evt.GetSelection()
        alpha = self.sample_alpha_choice[idx]
        self.theta = self.result[alpha]['theta']
        self.mean = self.result[alpha]['mean']
        self.std = self.result[alpha]['std']
        self.estimate_y()

    def on_x_choice_changed(self, evt):
        self.x_idx = evt.GetSelection()
        self.x_value.SetValue(str(self.x_values[self.x_idx]))

    def on_run_algo(self, evt):
        try:
            self.lbda = float(self.show_lambda.GetValue())
            self.deg = int(self.show_degree.GetValue())
            self.parent.statusbar.SetStatusText('')
        except ValueError:
            print(ValueError)
            self.parent.statusbar.SetStatusText('You must enter a number!!! Please')
        self.do_stuff(self.algo_idx, self.lbda, self.deg)
        self.result = self.parent.mlt.result
        self.theta = self.result['0']['theta']
        self.estimate_y()

    def on_x_value_changed(self, evt):
        if self.x_idx in range(len(self.x_values)) and hasattr(self, 'theta'):
            try:
                self.x_values[self.x_idx] = self.x_value.GetValue()
                self.parent.statusbar.SetStatusText('')
                self.estimate_y()
            except ValueError:
                print(ValueError)
                self.parent.statusbar.SetStatusText('You must enter a number!!! Please')
        else:
            pass
            # self.show_x_values.SetValue('Your test x_array is ' + str(self.x_values))

    def estimate_y(self):
        xx = np.zeros((1, len(self.x_values)+1))
        xx[0, 0] = 1
        for i in range(len(self.x_values)):
            xx[0, i+1] = self.x_values[i]
        if hasattr(self, 'mean') and hasattr(self, 'std'):
            for i in range(len(self.x_values)):
                xx[0, i+1] = (self.x_values[i] - self.mean[i]) / self.std[i]
        else:
            pass
        y = self.compute_y(xx)
        self.test_value.SetValue(str(y))
        xVals = str(xx[0, 0])
        for v in self.x_values:
            xVals += ', ' + str(v)
        self.show_x_values.SetValue('[ %r]' %xVals)

    def compute_y(self, xx):
        if self.kind == 0:
            return np.dot(xx, self.theta)
        elif self.kind == 1:
            return self.instance.estimate(xx, self.theta, self.deg)
        else:
            return ''

    def do_stuff(self, idx, coeff=None, deg=None):
        start = time.time()
        method_call = getattr(self.parent.mlt, self.sample_algo_choice[idx])
        method_call(None, None, coeff, deg)
        end = time.time()
        print("Time consumed of %s: %s sec \n\n" % (self.sample_algo_choice[idx], end-start))


if __name__ == "__main__":
    print 'Panel Controller'
