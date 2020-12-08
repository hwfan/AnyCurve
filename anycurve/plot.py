from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import itertools
import os
import random
import warnings
warnings.filterwarnings('ignore')

class curvedrawer(object):
    def __init__(self, figsize=(15, 12)):
        self.colorbank = ['red', 'blue', 'green', 'purple', 'brown', 'gray', 'orange', 'olive', 'cyan', 'pink']
        self.linestyle = ['solid', 'dotted', 'dashed', 'dashdot']
        self.pointname = ['point', 'triangle_down', 'triangle_up', 'octagon', 'square', 'pentagon', 'star', 'hexagon1', 'hexagon2', 'cross', 'diamond', 'circle', 'plus']
        self.pointstyle = ['.', 'v', '^', '8', 's', 'p', '*', 'h', 'H', 'x', 'D', 'o', '+']
        assert len(self.pointname) == len(self.pointstyle)
        self.pointdict = dict()
        for point_idx, pointname in enumerate(self.pointname):
            self.pointdict[pointname] = self.pointstyle[point_idx]
        self.colorbank_num = len(self.colorbank)
        self.linestyle_num = len(self.linestyle)
        self.pointname_num = len(self.pointname)
        self.choice_num = self.colorbank_num * self.linestyle_num * self.pointname_num
        self.choices = list(itertools.product(self.pointname, self.linestyle, self.colorbank))
        self.choice_cursor = 0
        self.panel = plt.figure(figsize=figsize)
        self.twin_state = False
        self.ori_figure = self.panel.add_subplot(111)
        self.figsize = figsize
        self.twin_figure = None
        self.x_label = None
        self.y_label = None
        self.y_twin_label = None

    def shuffle(self):
        random.shuffle(self.choices)
    
    def reset_choice(self):
        self.choice_cursor = 0

    def set_xlabel(self, x_name=None):
        if x_name is not None:
            self.ori_figure.set_xlabel(x_name)
            self.x_label = x_name

    def set_ylabel(self, y_name=None, twin_state=False):
        if y_name is not None:
            if twin_state:
                if self.twin_figure is None:
                    self.twin_figure = self.ori_figure.twinx()
                self.twin_figure.set_ylabel(y_name)
                self.y_twin_label = y_name
            else:
                self.ori_figure.set_ylabel(y_name)
                self.y_label = y_name

    def drawcurve(self, x, y, color='blue', linestyle='solid', pointstyle='point', y_label=None): 
        x_to_draw = np.array(x)
        y_to_draw = np.array(y)
        assert x_to_draw.ndim == 1, 'x should be an 1D array!'
        assert y_to_draw.ndim == 1, 'y should be an 1D array!'
        assert color in self.colorbank, 'color is not in internal color bank!'
        assert linestyle in self.linestyle, 'linestyle is not in internal linestyle bank!'
        assert pointstyle in self.pointname, 'pointstyle is not in internal pointstyle bank!'
        assert len(y_to_draw) == len(x_to_draw), 'the length of x is not equal to the length of y!'
        valid = np.logical_and(np.logical_not(np.isnan(x_to_draw)), np.logical_not(np.isnan(y_to_draw)))
        x_to_draw = x_to_draw[valid]
        y_to_draw = y_to_draw[valid]
        
        if self.twin_state:
            self.twin_figure.plot(x_to_draw, y_to_draw, color=color, linestyle=linestyle, marker=self.pointdict[pointstyle], label=y_label)
        else:
            self.ori_figure.plot(x_to_draw, y_to_draw, color=color, linestyle=linestyle, marker=self.pointdict[pointstyle], label=y_label)
        return

    def drawcurves(self, x, y, y_labels=None):
        x_to_draw = np.array(x)
        y_to_draw = np.array(y)
        
        if y_to_draw.ndim == 1:
            y_to_draw = np.expand_dims(y_to_draw, axis=1)
        assert x_to_draw.ndim == 1, 'x should be an 1D array!'
        if isinstance(y_labels, str):
            y_labels = [y_labels]
        if y_labels is not None:
            assert len(y_labels) == y_to_draw.shape[1], 'the length of labels should be equal to the number of curves!'
        assert y_to_draw.shape[1] <= self.choice_num, 'anycurve now only supports {:d} types of curve while the number of input curves is {:d}.'.format(self.choice_num, y_to_draw.shape[1])
        y_cursor = 0
        for pointstyle, linestyle, color in self.choices[self.choice_cursor:]:
            y_label_used = None if y_labels is None else y_labels[y_cursor]
            self.drawcurve(x_to_draw, y_to_draw[:, y_cursor], color=color, linestyle=linestyle, pointstyle=pointstyle, y_label=y_label_used)
            self.choice_cursor += 1
            y_cursor += 1
            if y_cursor == y_to_draw.shape[1]:
                break

    def clean(self):
        if self.twin_state:
            self.twin_figure.cla()
        else:
            self.ori_figure.cla() 
        self.set_xlabel(self.x_label)
        self.set_ylabel(self.y_label, False)
        if self.y_twin_label is not None:
            self.set_ylabel(self.y_twin_label, True)
            
    def legend(self, inside=True, left_offset=None, right_offset=None):
        if inside:
            if left_offset is None:
                left_offset = (0, 1)
            if right_offset is None:
                right_offset = (1, 1)

            self.ori_figure.legend(bbox_to_anchor=left_offset, loc=2)
            if self.twin_figure is not None:
                self.twin_figure.legend(bbox_to_anchor=right_offset, loc=1)
        else:
            if left_offset is None:
                left_offset = (-0.12, 1.05)
            if right_offset is None:
                right_offset = (1.12, 1.05)

            self.ori_figure.legend(bbox_to_anchor=left_offset, loc=2)
            if self.twin_figure is not None:
                self.twin_figure.legend(bbox_to_anchor=right_offset, loc=1)

    def show(self):
        plt.show()
    
    def twin(self):
        if not self.twin_state:
            if self.twin_figure is None:
                self.twin_figure = self.ori_figure.twinx()
            self.twin_state = True
        else:
            self.twin_state = False

    def render(self, filename):
        dirname = os.path.dirname(os.path.abspath(filename))
        os.makedirs(dirname, exist_ok=True)
        self.ori_figure.figure.savefig(filename)

if __name__ == '__main__':
    a = curvedrawer((20, 12))
    # a.drawcurve([1, 2], [3, 4], 'red', 'solid', 'point', 'x_axis', 'y_axis', 'good')

    a.drawcurves([1, 2, 3], [[3,5,7], [4,6,8], [5,7,9]], ['good', 'bad', 'ugly'])
    a.twin()
    a.drawcurves([1, 2, 3], [[3,1,-1], [2,0,-2], [1,-1,-3]], ['good', 'bad', 'ugly'])
    a.twin()
    a.drawcurves([1, 2, 3], [[4,6,8], [5,7,9], [6,8,10]], ['good', 'bad', 'ugly'])
    a.twin()
    a.drawcurves([1, 2, 3], [[2,0,-2], [1,-1,-3], [0,-2,-4]], ['good', 'bad', 'ugly'])

    # a.drawcurves([1, 2, 3], [[3,5], [4,6], [5,7]], 'x_axis', 'y_axis', ['good', 'bad'])
    # a.twin()
    # a.drawcurves([1, 2, 3], [[3,1], [2,0], [1,-1]], 'x_axis', 'another_y_axis', ['good_twin', 'bad_twin'])
    # a.twin()
    # a.drawcurves([1, 2, 3], [[4,6], [5,7], [6,8]], 'x_axis', 'y_axis', ['good2', 'bad2'])
    # a.twin()
    # a.drawcurves([1, 2, 3], [[2,0], [1,-1], [0,-2]], 'x_axis', 'another_y_axis', ['good2_twin', 'bad2_twin'])
    # a.twin()

    a.legend(inside=True)
    a.show()
    a.save('test.png')