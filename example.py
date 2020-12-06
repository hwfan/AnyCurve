from database import curvedb
from plot import curve
import ipdb
curve_data = curvedb('debug_data')
curve_data.reset()
curve_data.add_value({'x': 0, 'y': 0})
curve_data.add_value({'x': 1, 'y': 0})
curve_data.add_value({'x': 2, 'y': 1})
curve_data.add_value({'x': 3, 'y': -1, 'z': 4})
curve_data.add_value({'x': 4, 'z': 2})
curve_data.save()

curves = curve(figsize=(15, 12))
x_data = curve_data.get_column('x')
y_data = curve_data.get_column('y')
z_data = curve_data.get_column('z')
curves.drawcurves(x_data, y_data, 'x_axis', 'y_axis', 'y_data')
curves.twin()
curves.drawcurves(x_data, z_data, 'x_axis', 'z_axis', 'z_data')
curves.show()
curves.save('test.png')