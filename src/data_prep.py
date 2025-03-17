import numpy as np
import pandas as pd


def load_data(path):
    ### Load CSV files ###
    return pd.read_csv(path, delimiter="\t")

def total(data):
    data["total"] = data.sum(axis=1)
    return data

def level_selection(data, level_start: int, level_end:int, seq=1):
    return data[data["level_id"].isin(np.arange(level_start, level_end, seq))]

def level_selection_index(data, level_start: int, level_end: int, seq = 1):
    ### As level is index of the data, choose level to an interval"""
    return data.loc[level_start:level_end:seq]

def total_ratio(data):
    data["total"] = data.sum(axis = 1)
    data["fail_ratio"] = data[0] / data["total"]
    data["success_ratio"] = data[1] / data["total"]
    return data

