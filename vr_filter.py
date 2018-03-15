import os
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def butter_bandpass(low_cut, high_cut, fs, order):  # here we define the butter bandpass
                                                    # in order to get coefficient readouts for our output
    nyq = 0.5 * fs  # we define the nquist frequency here for the filter
    low = low_cut / nyq
    high = high_cut / nyq
    # this runs the filter function with our parameters
    butter_b, butter_a = butter(order, [low, high], btype='bandpass', analog=False)
    return butter_b, butter_a


def butter_bandpass_filter(channel, low_cut, high_cut, fs, order):
    # now we run the filtfilt function in order to get the data
    butter_b, butter_a = butter_bandpass(low_cut, high_cut, fs, order)
    butter_y = filtfilt(butter_b, butter_a, channel)
    return butter_y


def theta_filter(channel, sampling_rate):
    order = 2  # this sets the order of the filter
    fs = sampling_rate  # this is the sampling rate
    low_cut = 4  # this is the low end of the theta band pass filter
    high_cut = 10  # this is the high end of the theta band pass filter
    theta = butter_bandpass_filter(channel, low_cut, high_cut, fs, order)
    # plt.plot(theta + position, color)
    return theta


def gamma_filter(channel, sampling_rate):
    order = 2  # this sets the order of the filter
    fs = sampling_rate  # this is the sampling rate
    low_cut = 70  # this is the low end of the gamma band pass filter #70
    high_cut = 130  # this is the high end of the gamma band pass filter #130
    gamma = butter_bandpass_filter(channel, low_cut, high_cut, fs, order)
    # plt.plot(gamma, color)
    return gamma


def custom_filter(channel, lc, hc, sampling_rate, color='k'):
    order = 2  # this sets the order of the filter
    fs = sampling_rate  # this is the sampling rate
    low_cut = lc  # this is the low end of the band pass filter
    high_cut = hc  # this is the high end of the band pass filter
    filtered_channel = butter_bandpass_filter(channel, low_cut, high_cut, fs, order)
    # plt.plot(filtered_channel, color)
    return filtered_channel
