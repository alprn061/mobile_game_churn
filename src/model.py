import pandas as pd


def train_data(data, train):
    data = data.merge(train, on = "user_id", how = "left").dropna()
    return data

def dev_data(data, dev):
    data = data.merge(dev, on = "user_id", how= "left").dropna()
    return data

def test_data(data, test):
    data = data[data["user_id"].isin(test["user_id"])]
    return data


def drop_unused(data, *columns):
    data = data.drop(columns = list(columns), axis = 1)
    return data