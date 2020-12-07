from database import curvedb
from plot import curvedrawer

class curve(curvedb, curvedrawer):
    def __init__(self, db_path='', db_name='curvedb', figsize=(15, 12), static=False):
        curvedb.__init__(self, db_path=db_path, db_name=db_name)
        curvedrawer.__init__(self, figsize=figsize, static=static)

    def show(self):
        curvedb.show(self)
        curvedrawer.show(self)

    def log(self, dict_value):
        self.add_value(dict_value)
    
    def draw(self, attr_x, attr_y, label=None):
        self.drawcurves(self.get_column(attr_x), self.get_column(attr_y), attr_x, attr_y, label)

class losscurve(curve):
    def __init__(self, db_path, db_name, load_iter=False, figsize=(15, 12), static=False):
        curve.__init__(self, db_path=db_path, db_name=db_name, figsize=figsize, static=static)
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

    def step(self):
        self.metadata.add_value({'iteration': self.iteration})
        self.iteration += self.stepsize
        if self.states.check_index(0):
            states = self.states.get_value(0)
            states['cur_iter'] = self.iteration
            self.states.modify_value(0, states)
        else:
            self.states.add_value({'cur_iter': self.iteration})
    
    def log(self, dict_value):
        curve.log(self, dict_value)
        self.step()

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
        self.drawcurves(self.metadata.get_column('iteration'), self.get_column(attr), 'iteration', attr, label)

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
    import ipdb
    import numpy as np
    from tqdm import tqdm
    curve_handler = losscurve(db_path='debug', db_name='data', figsize=(20, 12))
    curve_handler.reset(True)
    curve_handler.set_internal()
    for iteration in tqdm(range(5001)):
        curve_handler.log({'loss': 0.11*np.exp(-iteration/500)})
        if iteration % 250 == 0:
            curve_handler.log({'acc': 1 / (1 + np.exp(-iteration/500))})
    curve_handler.synchronize()

    curve_handler.draw('loss', 'loss_curve')
    curve_handler.twin()
    curve_handler.draw('acc', 'acc_curve')
    curve_handler.legend(inside=False)
    curve_handler.render('test.png')