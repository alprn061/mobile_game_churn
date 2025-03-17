import numpy as np
import pandas as pd
import kagglehub
import os


def load_data(filename):
    """
    Downloads the dataset from Kaggle and loads it as a Pandas DataFrame.
    :param filename: Name of the file to be loaded (e.g., 'dev.csv', 'train.csv')
    :return: Pandas DataFrame
    """
    # Download the dataset from Kaggle
    path = kagglehub.dataset_download("manchvictor/prediction-of-user-loss-in-mobile-games")
    
    # Construct the full file path
    file_path = os.path.join(path, filename)

    # Read the CSV file and return it as a DataFrame
    return pd.read_csv(file_path, delimiter="\t")

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

