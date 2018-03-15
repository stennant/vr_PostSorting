
import vr_file_utility
import vr_open_ephys_IO
import os
import matplotlib.pylab as plt
import numpy as np
import vr_plot_continuous_data
import vr_filter


def convert_bits_to_ms(prm, bits):
    # sampling rate = 30000 / 30 kHz
    ms = bits / 30
    return ms

def convert_bits_to_sec(prm, bits):
    # sampling rate = 30000 / 30 kHz
    sec = int(bits / 30000)
    return sec

def convert_ms_to_bits(prm, ms):
    bits = ms*30
    return bits


def plot_theta(prm, filtered_theta, channel):

    #plot data
    fig = plt.figure(figsize = (15,6))
    ax = fig.add_subplot(111)
    ax.plot(np.arange(27000000,27120000,1), filtered_theta[0,27000000:27120000])

    ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis

    fig.savefig(prm.get_filepath() + 'Electrophysiology/theta_and_gamma/CH' + str(channel) + '_theta.png', dpi=200)
    plt.close()


def plot_gamma(prm, filtered_gamma, channel):

    #plot data
    fig = plt.figure(figsize = (15,6))
    ax = fig.add_subplot(111)
    ax.plot(np.arange(27000000,27120000,1), filtered_gamma[0,27000000:27120000])

    ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis

    fig.savefig(prm.get_filepath() + 'Electrophysiology/theta_and_gamma/CH' + str(channel) + '_gamma.png', dpi=200)
    plt.close()


def plot_theta_and_gamma(prm, filtered_theta, filtered_gamma, channel):

    #plot data
    fig = plt.figure(figsize = (15,6))
    ax = fig.add_subplot(111)
    ax.plot(np.arange(27000000,27120000,1), filtered_gamma[0,27000000:27120000], alpha = 0.5, color = 'k')
    ax.plot(np.arange(27000000,27120000,1), filtered_theta[0,27000000:27120000], color = 'DodgerBlue')

    ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis

    fig.savefig(prm.get_filepath() + 'Electrophysiology/theta_and_gamma/CH' + str(channel) + '_overlay.png', dpi=200)
    plt.close()



def load_and_plot_theta_and_gamma(prm):

    for c, channel in enumerate(np.arange(1,16,1)):

        #load continuous data
        channel_data_all = vr_plot_continuous_data.load_continuous_data(prm, channel)
        print('channel data loaded')

        #filter for theta
        filtered_theta = vr_filter.theta_filter(channel_data_all, 30000)
        print('channel filtered for theta')

        #filter for gamma
        filtered_gamma = vr_filter.gamma_filter(channel_data_all, 30000)
        print('channel filtered for gamma')

        #plot filtered data
        #plot_theta(prm, filtered_theta, channel)
        #plot_gamma(prm, filtered_gamma, channel)
        print('theta and gamma plotted')

        plot_theta_and_gamma(prm, filtered_theta,filtered_gamma, channel)
        print('theta and gamma overlay plotted')



