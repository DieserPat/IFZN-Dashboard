# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 12:22:50 2023

@author: gross
"""

import pandas as pd
from numpy.random import normal

def fetchConstData(path):
    file = pd.read_excel(path, sheet_name=None)
    
    data = dict()
    
    for key in file.keys():
        temp = file[key].to_dict()
        tempMod = list(temp["Modul"].values())
        for mod in tempMod:
            data[mod] = dict()
        for k in file[key].keys():
            if k != "Modul":
                for i, mod in enumerate(tempMod):
                    data[mod][k] = list(temp[k].values())[i]
    
    return data

def fetchData(path):
    data = pd.read_csv(path)
    data.index = data["index"]
    returnData = dict()
    for key in data.index:
        returnData[key] = normal(loc=data.loc[key]["mean"], scale=data.loc[key]["derrivate"])
    return returnData 