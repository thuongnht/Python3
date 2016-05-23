# plot 2d matplotlib
# plot 3d miyavi
import numpy as np
import random

import matplotlib
matplotlib.interactive( True )
matplotlib.use( 'WXAgg' )
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg, Toolbar
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from matplotlib.text import Text
from matplotlib.lines import Line2D
from matplotlib.legend import Legend

import wx

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
	    wx.Panel.__init__(self, parent=parent, size=(w, 0.7*h))
	    self.parent = parent
	    self.legends = []
	    self.legendpos = [0.5, 1]
		
	    self.fig = Figure(figsize=(12,6), dpi=90) # create a figure size 8x6 inches, 80 dots per inches
	    self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
	    self.toolbar = Toolbar(self.canvas) #matplotlib toolbar
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
	    annotate = self.splts[index].annotate(comment, xy=(len(J)-1, J[len(J)-1]), xytext=(len(J)/2, (J[0]+J[len(J)-1])/2), \
                                                arrowprops=dict(facecolor='black', shrink=0.05), fontsize=FONT_SIZE, picker=True)
	    annotate.draggable(True)											
		
    def plot_data_gradient_descent(self, X, y, format):
	    print("Plotting data ... \n")
	    for i in range(int(round(len(self.splts)/2))):
		    self.plot_data(self.splts[i], X, y, format)
	    self.update_canvas()
		
    def plot_data_normal_equation(self, X, y, format):
	    print("Plotting data ... \n")
	    for i in range(int(round((len(self.splts)+1)/2))):
		    self.plot_data(self.splts[i], X, y, format)
	    self.update_canvas()
		
    def plot_data(self, splt, X, y, format):   
	    line, = splt.plot(X, y, 'ro', color=format['color'], label=format['label'], picker=True)
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
	    print("Plotting Linear-Regression (Gradient Descent) and J-Convergence ... \n")
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
	    print("Plotting Linear-Regression (Normal Equation) ... \n")
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
	        self.splts[count].text(0.05, 0.95, comment, transform=self.splts[count].transAxes, fontsize=FONT_SIZE, verticalalignment='top', \
			                                                bbox=props, picker=True)
	        count += 1
	    self.show_legend()
	    self.update_canvas()
	
    def show_legend(self):
	    self.legends = []
	    for i in range(len(self.splts)):
	        splt = self.splts[i]
		    # Shrink current axis by 20%
	        box = splt.get_position()
	        splt.set_position([box.x0, box.y0, box.width * self.box_width_fraction, box.height * self.box_height_fraction])
	        # Now add the legend with some customizations.
	        legend = splt.legend(loc='upper center', ncol=1, fancybox=True, shadow=True)
	        legend.set_bbox_to_anchor((self.legendpos[0], self.legendpos[1] + legend.get_window_extent().height/self.figh + 0.25))
	        legend.figure.canvas.mpl_connect('pick_event', self.on_pick)
	        legend.draggable(True)			
	        #lined = dict()
	        #for legline, origline in zip(legend.get_lines(), self.lines):
	        #    legline.set_picker(5)  # 5 pts tolerance
	        #    self.lined[legline] = origline			
	        self.legends.append(legend)
	        if (legend):     
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
	    min = np.min(data)
	    max = np.max(data)
	    return np.arange(min, max, int((max-min)/3))
		
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
		    #box_points = evt.artist.get_position()
		    global TEXT_DRAGGABLE 
		    TEXT_DRAGGABLE = not TEXT_DRAGGABLE
		    evt.artist.draggable(TEXT_DRAGGABLE)	
        elif isinstance(evt.artist, Line2D):
		    #box_points = evt.artist.get_clip_box()
            pass			
        elif isinstance(evt.artist, Legend):
		    #box_points = evt.artist.get_clip_box()
		    global LEGEND_DRAGGABLE 
		    LEGEND_DRAGGABLE = not LEGEND_DRAGGABLE
		    evt.artist.draggable(LEGEND_DRAGGABLE)
        else:
		    print(evt.artist)
		    pass		
	
        #print("You've clicked on a bar with coords:\n %r, %r" % (box_points , evt.artist))
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
		
	    if (type == 'gd'):
	        gs = GridSpec(2, 3)
	        gs.update(hspace=0.7, wspace=0.8)
	        self.splts = [self.fig.add_subplot(gs[int(i/3),int(i%3)]) for i in range(2*3) ] # grid nxn
	    elif (type == 'ne'):
		    gs = GridSpec(1,1)
		    gs.update(hspace=0.7, wspace=0.8)
		    self.splts = [self.fig.add_subplot(gs[int(i/3),int(i%3)]) for i in range(1*1) ] # grid nxn
	    else:
		    pass
		
    def random_color(self):
        rgbl=[0, random.random(), random.random()]
        return tuple(rgbl)
		
    def update_canvas(self):
	    self.fig.canvas.draw()
	    self.canvas.Refresh()
	    self.toolbar.update()				

		
	
class Panel_Controller(wx.Panel):
    
    def __init__(self, parent):
	    w, h = parent.GetSize()
	    wx.Panel.__init__(self, parent=parent, size=(w, 0.3*h))
	    self.parent = parent
		
	    self.title = wx.StaticText(self, label="Panel Controllers")
	    
	    sizer = wx.BoxSizer()
	    sizer.Add(self.title, -1, wx.EXPAND | wx.ALL)
	    self.SetSizer(sizer)
			

if __name__ == '__main__':
    ph = Panel_Plotting_Helper(parent=None, id=-1)
    print(ph)
    