import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def hist(data_cal, duration_start=1, duration_end=data_cal.index[-1]):
    """
    This function plots histogram
    :param data_cal: DataFrame output from calculate_basic.py or others
    :param duration_start: start point you want to analyze
    :param duration_end: end point you want to analyze
    :return: plotting
    """
    sns.set()
    x = duration_start:data_cal.index[-1]
    y = data_cal[duration_start:data_cal.index[-1]]
    plt.plot(x,y)