from database import curvedb
from plot import curvedrawer
class curve(curvedrawer):
    def __init__(self, db_path, db_name):
        self.db_path = db_path
        self.db = curvedb(db_path, db_name)
    