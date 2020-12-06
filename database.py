import pandas as pd
import os
import numpy as np
class curvedb(object):
    '''
    database class for storing curve data.
    '''
    def __init__(self, db_path, db_name='curvedb'):
        self.db_name = db_name
        self.initialize(db_path)
    
    def initialize(self, db_path):
        assert len(db_path) > 0
        if os.path.exists(db_path):
            self.load(db_path)
        else:
            self.reset()
            self.save(db_path, True)

    def reset(self):
        self.db = pd.DataFrame()

    def get_db(self):
        return self.db

    @property
    def cursor(self):
        return self.db.shape[0]

    @property
    def keys(self):
        return list(self.db.keys())
    
    def get_column(self, key):
        return self.db[key].to_numpy()

    def add_key(self, key):
        if isinstance(key, list):
            for each_key in key:
                self.db[each_key] = np.nan
        else:
            self.db[key] = np.nan

    def delete_key(self, key):
        if isinstance(key, list):
            self.db.drop(columns=key, inplace=True)
        else:
            self.db.drop(columns=[key], inplace=True)
            
    def search_value(self, key, target_value):
        return self.db[key] == target_value

    def add_value(self, dict_value):
        assert isinstance(dict_value, dict), 'The input of add_value should be a dict variable!'

        for key in dict_value:
            if key not in self.keys:
                self.add_key(key)

        for key in self.keys:
            if key not in dict_value:
                dict_value[key] = np.nan

        self.db.loc[self.cursor] = dict_value

    def modify_value(self, index, dict_value):
        self.db.loc[index] = dict_value

    def del_value(self, index):
        if isinstance(key, list):
            self.db.drop(index=index)
        else:
            self.db.drop(index=[index])
    
    def show(self):
        print(self.db)

    def save(self, path='', change_path=False):
        if len(path) == 0:
            self.db.to_hdf(self.default_path, self.db_name)
        elif change_path:
            self.db.to_hdf(path, self.db_name)
            self.default_path = path
        else:
            self.db.to_hdf(path, self.db_name)

    def load(self, path, change_path=True):
        self.db = pd.read_hdf(path, self.db_name)
        if change_path:
            self.default_path = path