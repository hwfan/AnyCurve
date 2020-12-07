from anycurve import losscurve
import time
import ipdb
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
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
    




# from database import curvedb
# from plot import curve
# import ipdb
# curve_data = curvedb('debug_data')
# curve_data.add_value({'x': 0, 'y': 0})
# curve_data.add_value({'x': 1, 'y': 0})
# curve_data.add_value({'x': 2, 'y': 1})
# curve_data.add_value({'x': 3, 'y': -1, 'z': 4})
# curve_data.add_value({'x': 4, 'z': 2})
# curve_data.save()

# curves = curve(figsize=(15, 12))
# x_data = curve_data.get_column('x')
# y_data = curve_data.get_column('y')
# z_data = curve_data.get_column('z')
# curves.drawcurves(x_data, y_data, 'x_axis', 'y_axis', 'y_data')
# curves.twin()
# curves.drawcurves(x_data, z_data, 'x_axis', 'z_axis', 'z_data')
# curves.show()
# curves.save('test.png')