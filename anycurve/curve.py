from .database import curvedb
from .plot import curvedrawer

class curve(curvedb, curvedrawer):
    def __init__(self, db_path='', db_name='curvedb', figsize=(15, 12)):
        curvedb.__init__(self, db_path=db_path, db_name=db_name)
        curvedrawer.__init__(self, figsize=figsize)

    def show(self):
        curvedb.show(self)
        curvedrawer.show(self)
    
    def log(self, dict_value):
        self.add_value(dict_value)
    
    def draw(self, attr_x, attr_y, label=None):
        self.drawcurves(self.get_column(attr_x), self.get_column(attr_y), label)

    def daemon(self, start=False, interval=1):
        if start:
            assert interval >= 1
            self.daemon_counter = 0
            self.daemon_interval = interval
        else:
            if self.daemon_counter == self.daemon_interval:
                self.daemon_counter = 1
                return True
            else:
                self.daemon_counter += 1
        return False
        
class losscurve(curve):
    def __init__(self, db_path, db_name, load_iter=False, figsize=(15, 12)):
        curve.__init__(self, db_path=db_path, db_name=db_name, figsize=figsize)
        self.iteration = 0
        self.stepsize = 1
        self.metadata = curvedb(db_path, 'metadata')
        self.states = curvedb(db_path, 'states')
        if load_iter:
            if self.states.check_index(0):
                if 'cur_iter' in self.states.get_value(0):
                    self.iteration = self.states.get_value(0)['cur_iter']
        self.internal_iter = False

    def set_iter(self, iteration):
        self.iteration = iteration

    def set_step(self, stepsize):
        self.stepsize = stepsize

    def set_internal(self, state=True):
        self.internal_iter = state
        if self.internal_iter:
            self.set_xlabel('iteration')

    def step(self, no_step=False):
        self.metadata.add_value({'iteration': self.iteration})
        if not no_step:
            self.iteration += self.stepsize
            if self.states.check_index(0):
                states = self.states.get_value(0)
                states['cur_iter'] = self.iteration
                self.states.modify_value(0, states)
            else:
                self.states.add_value({'cur_iter': self.iteration})
    
    def log(self, dict_value, no_step=False):
        curve.log(self, dict_value)
        self.step(no_step=no_step)

    def reset(self, force_clean=False):
        curve.reset(self, force_clean=force_clean)
        self.metadata.reset(force_clean=force_clean)
        self.states.reset(force_clean=force_clean)
        self.iteration = 0

    def show(self):
        curvedb.show(self)
        self.metadata.show()
        self.states.show()
        curvedrawer.show(self)
        
    def draw_internal(self, attr=None, label=None):
        self.drawcurves(self.metadata.get_column('iteration'), self.get_column(attr), label)

    def draw_external(self, attr_x=None, attr_y=None, label=None):
        curve.draw(self, attr_x, attr_y, label)
        
    def draw(self, *args, **kwargs):
        if not self.internal_iter:
            self.draw_external(*args, **kwargs)
        else:
            self.draw_internal(*args, **kwargs)

    def synchronize(self):
        curve.save(self)
        self.metadata.save()
        self.states.save()

if __name__ == '__main__':
    import time
    import ipdb
    import numpy as np
    from tqdm import tqdm
    curve_handler = losscurve(db_path='debug', db_name='data', figsize=(20, 12))
    curve_handler.reset(True)
    curve_handler.set_internal()
    curve_handler.set_ylabel('loss', False)
    curve_handler.set_ylabel('acc', True)
    curve_handler.daemon(True, 10)
    for iteration in tqdm(range(501)):
        curve_handler.clean()
        curve_handler.log({'loss_A': 0.11*np.exp(-iteration/500), 'loss_B': 0.11*np.exp(-iteration/1000)}, no_step=iteration % 10 == 0)
        if iteration % 10 == 0:
            curve_handler.log({'acc_A': 1 / (1 + np.exp(-iteration/500)), 'acc_B': 1 / (1 + np.exp(-iteration/1000))})
        
        to_draw = curve_handler.daemon()
        if to_draw:
            curve_handler.draw('loss_A', 'model A')
            curve_handler.draw('loss_B', 'model B')
            curve_handler.twin()
            curve_handler.clean()
            curve_handler.draw('acc_A', 'model A')
            curve_handler.draw('acc_B', 'model B')
            curve_handler.twin()
            curve_handler.reset_choice()
            curve_handler.legend(inside=False)
            curve_handler.synchronize()
            curve_handler.render('test.png')
    