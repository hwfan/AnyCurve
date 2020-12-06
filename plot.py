from matplotlib import pyplot as plt
import numpy as np
import itertools
import ipdb
import os
class curvedrawer(object):
    def __init__(self, figsize):
        self.colorbank = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        self.linestyle = ['solid', 'dotted', 'dashed', 'dashdot']
        self.pointname = ['point', 'triangle_down', 'triangle_up', 'octagon', 'square', 'pentagon', 'star', 'hexagon1', 'hexagon2', 'plus', 'cross', 'diamond', 'circle']
        self.pointstyle = ['.', 'v', '^', '8', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'o']
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

    def drawcurve(self, x, y, color='blue', linestyle='solid', pointstyle='point', x_name=None, y_name=None, y_label=None):
        self.figure = self.ori_figure if not self.twin_state else self.twin_figure
        x_to_draw = np.array(x)
        y_to_draw = np.array(y)
        assert x_to_draw.ndim == 1, 'x should be an 1D array!'
        assert y_to_draw.ndim == 1, 'y should be an 1D array!'
        assert color in self.colorbank, 'color is not in internal color bank!'
        assert linestyle in self.linestyle, 'linestyle is not in internal linestyle bank!'
        assert pointstyle in self.pointname, 'pointstyle is not in internal pointstyle bank!'
        assert len(y_to_draw) == len(x_to_draw), 'the length of x is not equal to the length of y!'
        self.figure.plot(x_to_draw, y_to_draw, color=color, linestyle=linestyle, marker=self.pointdict[pointstyle], label=y_label)
        if x_name is not None:
            self.figure.set_xlabel(x_name)
        if y_name is not None:
            self.figure.set_ylabel(y_name)
        return

    def drawcurves(self, x, y, x_name=None, y_name=None, y_labels=None):
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
            x_name_used = None if y_cursor != 0 or self.twin_state else x_name
            y_label_used = None if y_labels is None else y_labels[y_cursor]
            self.drawcurve(x_to_draw, y_to_draw[:, y_cursor], color=color, linestyle=linestyle, pointstyle=pointstyle, x_name=x_name_used, y_name=y_name, y_label=y_label_used)
            self.choice_cursor += 1
            y_cursor += 1
            if y_cursor == y_to_draw.shape[1]:
                break
        return

    def legend(self, inside=True, left_offset=(-0.1, 1), right_offset=(1.1, 1)):
        if inside:
            self.ori_figure.legend()
            if self.twin_figure is not None:
                self.twin_figure.legend()
        else:
            self.ori_figure.legend(bbox_to_anchor=left_offset, loc=2)
            if self.twin_figure is not None:
                self.twin_figure.legend(bbox_to_anchor=right_offset, loc=1)

    def twin(self):
        if not self.twin_state:
            if self.twin_figure is None:
                self.twin_figure = self.figure.twinx()
            self.twin_state = True
        else:
            self.twin_state = False

    def show(self):
        plt.show()

    def save(self, filename):
        dirname = os.path.dirname(os.path.abspath(filename))
        os.makedirs(dirname, exist_ok=True)
        self.ori_figure.figure.savefig(filename)
        return

if __name__ == '__main__':
    a = curvedrawer((20, 12))
    # a.drawcurve([1, 2], [3, 4], 'red', 'solid', 'point', 'x_axis', 'y_axis', 'good')

    a.drawcurves([1, 2, 3], [[3,5,7], [4,6,8], [5,7,9]], 'x_axis', 'y_axis', ['good', 'bad', 'ugly'])
    a.twin()
    a.drawcurves([1, 2, 3], [[3,1,-1], [2,0,-2], [1,-1,-3]], 'x_axis', 'another_y_axis', ['good', 'bad', 'ugly'])
    a.twin()
    a.drawcurves([1, 2, 3], [[4,6,8], [5,7,9], [6,8,10]], 'x_axis', 'y_axis', ['good', 'bad', 'ugly'])
    a.twin()
    a.drawcurves([1, 2, 3], [[2,0,-2], [1,-1,-3], [0,-2,-4]], 'x_axis', 'another_y_axis', ['good', 'bad', 'ugly'])

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