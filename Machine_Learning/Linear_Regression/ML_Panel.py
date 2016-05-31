# plot 2d matplotlib
# plot 3d miyavi
import numpy as np
import random
import os
import time

import matplotlib
matplotlib.interactive( True )
matplotlib.use( 'WXAgg' )
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg, Toolbar
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.lines import Line2D
from matplotlib.legend import Legend

import wx
from wx.lib.stattext import GenStaticText

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.gridspec import GridSpec

FONT_SIZE = 10
PICKER = True
TEXT_DRAGGABLE = True
LEGEND_DRAGGABLE = True


class Panel_Plotting_Helper(wx.Panel):

    def __init__(self, parent):
        w, h = parent.GetSize()
        wx.Panel.__init__(self, parent=parent, size=(w, 0.7*h), style=wx.SUNKEN_BORDER)
        self.parent = parent
        self.legends = []
        self.legendpos = [0.5, 1]

        self.fig = Figure(figsize=(12, 6), dpi=90)  # create a figure size 8x6 inches, 80 dots per inches
        self.splts = []
        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        self.toolbar = Toolbar(self.canvas)  # matplotlib toolbar
        # additional toolbar
        status_txt = wx.StaticText(self.toolbar, label='    Status on hover: ', pos=(230, 7), \
                                   size=(100, 17))
        self.status = wx.TextCtrl(self.toolbar, pos=(330,4), size=(300, 22), \
                                  style=wx.TE_READONLY)
        self.toolbar.Realize()

        self.figw, self.figh = self.fig.get_window_extent().width, self.fig.get_window_extent().height

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.toolbar, 0, wx.GROW)
        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(sizer)
        self.box_width_fraction = 1.0
        self.box_height_fraction = 0.9
        self.lines = []
        self.lined = dict()
        self.draggableList = ['Text', 'Legend']
        # print(self.toolbar.GetBackgroundColour())

        self.fig.canvas.mpl_connect('resize_event', self.squeeze_legend)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('figure_leave_event', self.on_leave)

    def plot_J(self, J, theta, format, r, count):
        index = count%3 + 3
        self.splts[index].plot(np.arange(len(J)), J, color=format['color'], linewidth=format['linewidth'], linestyle=format['linestyle'], label=format['label'], picker=True)
        self.splts[index].set_xlabel("Number of Iteration", fontsize=FONT_SIZE)
        self.splts[index].set_ylabel("Cost value", fontsize = FONT_SIZE)
        self.set_ticks(self.splts[index], np.arange(len(J)), J)
        comment = r + ': [\n'
        for t in theta:
            comment += '    ' + str(t) + '\n'
            comment += ']'
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        annotate = self.splts[index].annotate(comment, xy=(len(J)-1, J[len(J)-1]), xytext=(len(J)/2, (J[0]+J[len(J)-1])/2), \
                                                  arrowprops=dict(facecolor='black', shrink=0.05), bbox=props, fontsize=FONT_SIZE, picker=True)
        annotate.draggable(True)

    def plot_data_gradient_descent(self, X, y, format):
        print("Plotting data ...")
        for i in range(int(round(len(self.splts)/2))):
            self.plot_data(self.splts[i], X, y, format)
        self.update_canvas()

    def plot_data_normal_equation(self, X, y, format):
        print("Plotting data ...")
        for i in range(int(round((len(self.splts)+1)/2))):
            self.plot_data(self.splts[i], X, y, format)
        self.update_canvas()

    def plot_data(self, splt, X, y, format):
        line, = splt.plot(X, y, 'ro', color=format['color'], label=format['label'], picker=True)
        self.set_ticks(splt, X, y)
        self.lines.append(line)
        splt.set_xlabel("X1", fontsize=FONT_SIZE)
        splt.set_ylabel("Y", fontsize=FONT_SIZE)

    def set_ticks(self, splt, X, y):
        xticks = self.make_ticks(X)
        yticks = self.make_ticks(y)
        splt.set_xticks(xticks)
        splt.set_yticks(yticks)
        for tick in splt.get_xticklabels():
            tick.set_rotation(45)
            tick.set_fontsize(FONT_SIZE)
        for tick in splt.get_yticklabels():
            tick.set_rotation(45)
            tick.set_fontsize(FONT_SIZE)

    def plot_all_gradient_descent(self, object):
        print("Plotting Linear-Regression (Gradient Descent) and J-Convergence ...")
        count = 0
        for r in object:
            c = self.random_color()
            self.splts[count].plot(object[r]['data']['x'], object[r]['data']['y'], color=c, linestyle="-", label="Linear Regression (alpha="+r+")", picker=True)
            self.set_ticks(self.splts[count], object[r]['data']['x'], object[r]['data']['y'])
            self.plot_J(object[r]['J_history'], object[r]['theta'], {"color": c, "linewidth": 5, "linestyle": "-", "label": "Convergence of J"}, r, count)
            count += 1
        self.show_legend()
        self.update_canvas()

    def plot_all_normal_equation(self, object):
        print("Plotting Linear-Regression (Normal Equation) ...")
        count = 0
        for r in object:
            c = self.random_color()
            line, = self.splts[count].plot(object[r]['data']['x'], object[r]['data']['y'], color=c, linestyle="-", label="Linear Regression (Normal Equation)", picker=True)
            self.lines.append(line)
            self.set_ticks(self.splts[count], object[r]['data']['x'], object[r]['data']['y'])
            comment = 'Theta: [\n'
            for t in object[r]['theta']:
                comment += '    ' + str(t[0]) + '\n'
            comment += ']'
            # place a text box in upper left in axes coords
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            annotate = self.splts[count].annotate(comment, xy=(min(object[r]['data']['x']), max(object[r]['data']['y'])), \
                                                      xytext=(min(object[r]['data']['x']), max(object[r]['data']['y'])), bbox=props, fontsize=FONT_SIZE, picker=True)
            annotate.draggable(True)
            count += 1
        self.show_legend()
        self.update_canvas()

    def show_legend(self):
        self.legends = []
        for i in range(len(self.splts)):
            splt = self.splts[i]
            # Shrink current axis by 20%
            box = splt.get_position()
            splt.set_position([box.x0, box.y0, box.width * self.box_width_fraction, \
                               box.height * self.box_height_fraction])
            # Now add the legend with some customizations.
            legend = splt.legend(loc='upper center', ncol=1, fancybox=True, shadow=True)
            legend.set_bbox_to_anchor((self.legendpos[0], \
                                       self.legendpos[1] + legend.get_window_extent().height/self.figh + 0.25))
            legend.figure.canvas.mpl_connect('pick_event', self.on_pick)
            legend.draggable(True)
            # lined = dict()
            # for legline, origline in zip(legend.get_lines(), self.lines):
            #    legline.set_picker(5)  # 5 pts tolerance
            #    self.lined[legline] = origline
            self.legends.append(legend)
            if legend:
                # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
                frame = legend.get_frame()
                frame.set_facecolor('0.90')
                # Set the fontsize
                for label in legend.get_texts():
                    label.set_fontsize(FONT_SIZE)
                for label in legend.get_lines():
                    label.set_linewidth(0.75)  # the legend line width
            else:
                pass

    def make_ticks(self, data):
        minn = np.min(data)
        maxx = np.max(data)
        return np.arange(minn, maxx, int((maxx-minn)/3))

    def squeeze_legend(self, evt):
        new_height = self.fig.get_window_extent().height
        self.box_height_fraction = new_height / self.figh
        self.figh = new_height
        new_width = self.fig.get_window_extent().width
        self.box_width_fraction = new_width / self.figw
        self.figw = new_width
        self.show_legend()
        self.update_canvas()

    def on_pick(self, evt):
        if isinstance(evt.artist, Text):
            # box_points = evt.artist.get_position()
            global TEXT_DRAGGABLE
            TEXT_DRAGGABLE = not TEXT_DRAGGABLE
            evt.artist.draggable(TEXT_DRAGGABLE)
        elif isinstance(evt.artist, Line2D):
            # box_points = evt.artist.get_clip_box()
            pass
        elif isinstance(evt.artist, Legend):
            # box_points = evt.artist.get_clip_box()
            global LEGEND_DRAGGABLE
            LEGEND_DRAGGABLE = not LEGEND_DRAGGABLE
            evt.artist.draggable(LEGEND_DRAGGABLE)
        else:
            print(evt.artist)
            pass

        # print("You've clicked on a bar with coords:\n %r, %r" % (box_points , evt.artist))
        self.update_canvas()

    def on_motion(self, mouseevt):
        w, h = self.canvas.GetSize()
        if mouseevt.x in range(0, int(w+1)) and mouseevt.y in range(0, int(h+1)):
            self.status.SetValue('Click on %r for dragging On/Off' % self.draggableList)
        else:
            pass

    def on_leave(self, mouseevt):
        self.status.SetValue('')

    def make_figure(self, type):
        self.fig.clf()
        if type == 'gd':
            gs = GridSpec(2, 3)
            gs.update(hspace=0.7, wspace=0.8)
            self.splts = [self.fig.add_subplot(gs[int(i/3), int(i%3)]) for i in range(2*3)]  # grid nxn
        elif type == 'ne':
            gs = GridSpec(1,1)
            gs.update(hspace=0.7, wspace=0.8)
            self.splts = [self.fig.add_subplot(gs[int(i/3), int(i%3)]) for i in range(1*1)]  # grid nxn
        else:
            pass

    def random_color(self):
        rgbl = [0, random.random(), random.random()]
        return tuple(rgbl)

    def update_canvas(self):
        self.fig.canvas.draw()
        self.canvas.Refresh()
        self.toolbar.update()


class Panel_Controller(wx.Panel):

    def __init__(self, parent):
        w, h = parent.GetSize()
        wx.Panel.__init__(self, parent=parent, size=(w, 0.2*h), style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour((210, 210, 210))
        self.parent = parent
        self.sample_algo_choice = []
        self.id = 0
        self.x_idx = -1

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
        subsubsizer1.Add(algo_title, 1, wx.EXPAND | wx.ALL)
        subsubsizer1.Add(self.algo_choice, 1, wx.EXPAND | wx.ALL)
        self.subsizer1.Add(subsubsizer1, 0, wx.EXPAND | wx.ALL, 5)

        subsubsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        test_title = GenStaticText(self, size=(100, -1), label="Test Values:  ", style=wx.ALIGN_RIGHT)
        test_title.SetBackgroundColour((210, 210, 210))
        self.test_value = wx.TextCtrl(self, style=wx.CB_READONLY)
        self.test_value.SetBackgroundColour((210, 210, 210))
        subsubsizer2.Add(test_title, 1, wx.EXPAND | wx.ALL)
        subsubsizer2.Add(self.test_value, 4, wx.EXPAND | wx.ALL)
        self.subsizer2 = wx.BoxSizer(wx.VERTICAL)
        self.subsizer2.Add(subsubsizer2, 0, wx.EXPAND | wx.ALL, 5)
        self.gensizer = wx.BoxSizer(wx.HORIZONTAL)
        x_values_title = GenStaticText(self, size=(100, -1), label=" X Values:  ", style=wx.ALIGN_RIGHT)
        x_values_title.SetBackgroundColour((210, 210, 210))
        self.show_x_values = wx.TextCtrl(self, self.id, style=wx.CB_READONLY)
        self.show_x_values.SetBackgroundColour((210, 210, 210))
        self.id += 1
        xvaluessizer = wx.BoxSizer(wx.HORIZONTAL)
        xvaluessizer.Add(x_values_title, 1, wx.EXPAND | wx.ALL)
        xvaluessizer.Add(self.show_x_values, 4, wx.EXPAND | wx.ALL)
        self.subsizer2.Add(xvaluessizer, 0, wx.EXPAND | wx.ALL, 5)
        self.subsizer2.Add(self.gensizer, 0, wx.EXPAND | wx.ALL, 5)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.subsizer1, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.subsizer2, 3, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(sizer)

        self.dataset.Bind(wx.EVT_BUTTON, self.on_load_dataset)
        self.algo_choice.Bind(wx.EVT_COMBOBOX, self.on_algo_changed)

    def make_test_items(self, features):
        self.alpha_title = GenStaticText(self, size=(100, -1), label="Choose Alpha:  ", style=wx.ALIGN_RIGHT)
        self.alpha_title.SetBackgroundColour((210, 210, 210))
        self.alpha_choice = wx.ComboBox(self, self.id, choices=[], style=wx.CB_READONLY)
        self.toggle_Alpha(False)
        self.gensizer.Add(self.alpha_title, 1, wx.EXPAND | wx.ALL)
        self.gensizer.Add(self.alpha_choice, 1, wx.EXPAND | wx.ALL)
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
        self.gensizer.Add(x_title, 1, wx.EXPAND | wx.ALL)
        self.gensizer.Add(self.x_choice, 1, wx.EXPAND | wx.ALL)
        self.gensizer.Add(self.x_value, 1, wx.EXPAND | wx.ALL)

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
        self.dirname = ""  # set directory name to blank
        dlg = wx.FileDialog(self, "Choose a file to open", self.dirname, "", "*.*", wx.OPEN)  # open the dialog boxto open file
        if dlg.ShowModal() == wx.ID_OK:  # if positive button selected....
            self.filename = dlg.GetFilename()  # get the filename of the file
            self.dirname = dlg.GetDirectory()  # get the directory of where file is located
            self.parent.mlt.loadData(os.path.join(self.dirname, self.filename))  # traverse the file directory and find filename in the OS
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
        self.delete_attributes()

    def on_algo_changed(self, evt):
        idx = evt.GetSelection()
        if self.parent.mlt:
            self.do_stuff(idx)
            self.delete_attributes()
            self.result = self.parent.mlt.result
            if len(self.result.keys()) > 1:
                # self.alphas = self.result.keys()
                self.updated_alpha_choice(self.result.keys())
            else:
                self.theta = self.result['0']['theta']
                self.estimate_y()
            if self.sample_algo_choice[idx] == 'lrByGradientDescent' and len(self.sample_alpha_choice) > 0:
                self.toggle_Alpha(True)
            else:
                self.toggle_Alpha(False)
        else:
            pass

    def delete_attributes(self):
        self.sample_alpha_choice = []
        self.x_choice.SetSelection(self.x_idx)
        self.x_value.SetValue(str(self.x_values[self.x_idx]))
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
        self.show_x_values.SetValue('')
        self.test_value.SetValue('')

    def toggle_Alpha(self, isShown):
        if isShown:
            self.alpha_title.Enable()
            self.alpha_choice.Enable()
        else:
            self.alpha_title.Disable()
            self.alpha_choice.Disable()

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

    def on_x_value_changed(self, evt):
        if self.x_idx in range(len(self.x_values)) and hasattr(self, 'theta'):
            try:
                self.x_values[self.x_idx] = self.x_value.GetValue()
                self.estimate_y()
            except ValueError:
                print(ValueError)
                self.show_x_values.SetValue('You must enter a number!!! Please')
        else:
            pass
            # self.show_x_values.SetValue('Your test x_array is ' + str(self.x_values))

    def estimate_y(self):
        xx = np.zeros((1, len(self.x_values)+1))
        xx[0][0] = 1
        for i in range(len(self.x_values)):
            xx[0][i+1] = self.x_values[i]
        if hasattr(self, 'mean') and hasattr(self, 'std'):
            for i in range(len(self.x_values)):
                xx[0][i+1] = (self.x_values[i] - self.mean[i]) / self.std[i]
        else:
            pass
        y = np.dot(xx, self.theta)
        self.test_value.SetValue(str(y))
        xVals = str(xx[0][0])
        for v in self.x_values:
            xVals += ', ' + str(v)
        self.show_x_values.SetValue('[ %r]' %xVals)

    def do_stuff(self, idx):
        start = time.time()
        method_call = getattr(self.parent.mlt, self.sample_algo_choice[idx])
        method_call()
        end = time.time()
        print("Time consumed of %s: %s sec \n\n" % (self.sample_algo_choice[idx], end-start))


if __name__ == '__main__':
    ph = Panel_Plotting_Helper()
    print(ph)
