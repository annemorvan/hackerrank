#!/bin/python3

import math
import os
import random
import re
import sys

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def read_training_data():
    """
    The first number denotes the amount of time the laptop was charged.
    The second number denotes the amount of time the battery lasted.
    :return:
    """
    file_name = '../data/trainingdata.txt'
    training_data = pd.read_csv(file_name, header=None, names=["time_charged", "time_lasted"])
    return training_data

def analysis_data():

    # EDA
    training_data = read_training_data()
    print(training_data)
    training_data.plot(x="time_charged", y="time_lasted", kind='scatter')
    plt.show()

    # We observe a clear linear part slightly after 4.11 hours and then the battery life is around 8h.
    print(training_data[training_data["time_lasted"] == 8.0].time_charged.min())

def linear_fit_data():
    training_data = read_training_data()
    x = training_data[training_data["time_lasted"] < 8.0].time_charged
    y = training_data[training_data["time_lasted"] < 8.0].time_lasted
    slope, intercept, r, p, std_err = stats.linregress(x, y)
    return slope, intercept, r, p, std_err

def predict_how_long_battery_will_last(time_charged, slope, intercept):
    breaking_point = 4.0
    if time_charged <= breaking_point:
        return slope * time_charged + intercept
    else:
        return 8.0

if __name__ == '__main__':

    #analysis_data()
    slope, intercept, r, p, std_err = linear_fit_data()
    time_charged = float(input().strip())
    prediction = predict_how_long_battery_will_last(time_charged, slope, intercept)
    print(round(prediction, 2))



