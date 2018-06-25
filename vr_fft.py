'''
power spectrum plots the power spectrum for the given channel
power_spectum_log plots the logarithmic power spectrum

'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
import matplotlib.pylab as plt
import os
import numpy as np
import pylab as pl
from scipy.fftpack import fft, rfft, fftfreq
import pylab as plt
import vr_plot_utility

# plot power spectrum for channel
# this function is copied from StackExchange
def power_spectrum(prm, channel, color, sampling_rate):
    ps = np.abs(np.fft.fft(channel))**2
    time_step = 1 / 30000
    freqs = np.fft.fftfreq(channel.size, time_step)
    idx = np.argsort(freqs)
    plt.plot(freqs[idx], ps[idx])
    plt.xlabel('$Frequency (Hz)$', fontsize = 18)
    plt.ylabel('$PSD (V^2/Hz)$', fontsize = 18)
    plt.xlim(0, 100)
    #plt.ylim(0, 1)




# plot logarithmic power spectrum for channel
def power_spectrum_log(prm, ax, channel, sampling_rate, color, filename, title="$Power  spectrum$", x_lim=130, line_width=15,
                       legend='set legend'):
    window = scipy.signal.get_window('hamming', len(channel))
    f, pxx_den = signal.periodogram(channel, sampling_rate, window)

    ax.plot(f, np.sqrt(pxx_den), color, line_width)
    ax.set_title(title)

    ax.set_xlim([0, x_lim])
    #ax.set_xlim([5, 130])
    ax.set_xlabel('$Frequency (Hz)$', fontsize = 16)
    ax.set_ylabel('$PSD (V^2/Hz)$', fontsize = 16)
    #plt.savefig(filename + ".png")




# plot logarithmic power spectrum for channel
def power_spectrum_log2(prm, channel, sampling_rate, color, filename, title="$Power  spectrum$", x_lim=15, line_width=15,
                       legend='set legend'):
    window = scipy.signal.get_window('hamming', channel.size)
    f, pxx_den = signal.periodogram(channel, sampling_rate, window)

    plt.plot(f, np.sqrt(pxx_den), color, line_width)
    plt.title(title)

    plt.xlim([0, x_lim])
    plt.ylim([5, 300])
    plt.xlabel('$Frequency (Hz)$', fontsize = 18)
    plt.ylabel('$PSD (V^2/Hz)$', fontsize = 18)
    #plt.savefig(filename + ".png")



# plot logarithmic power spectrum for channel
def power_spectrum_log_inset(prm, channel, sampling_rate, color, filename, title="$Power  spectrum$", x_lim=15, line_width=15,
                       legend='set legend'):
    window = scipy.signal.get_window('hann', channel.size)
    f, pxx_den = signal.periodogram(channel, sampling_rate, window)

    plt.plot(f, np.sqrt(pxx_den), color, line_width)
    plt.title(title)

    plt.xlim([0, 15])
    #plt.ylim([5, 200])
    plt.xlabel('$Frequency (Hz)$')
    plt.ylabel('$PSD (V^2/Hz)$')
    plt.savefig(filename + ".png")



def plot_power_spectrum(prm, channel_all_data, channel):
    ephys_path = prm.get_filepath() + 'Electrophysiology'
    data_path = ephys_path + '/Data'
    analysis_path = ephys_path + '/Analysis'
    spike_path = ephys_path + '/Spike_sorting'

    if os.path.exists(ephys_path) is False:
        print('Behavioural data will be saved in {}.'.format(ephys_path))
        os.makedirs(ephys_path)
        os.makedirs(data_path)
        os.makedirs(analysis_path)
        os.makedirs(spike_path)

    if os.path.isfile(analysis_path + 'ps_stationary_movement.png') is False:
        print('Plotting and saving power spectra')

        fig, ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

        #power_spectrum_log(prm, channel_all_data, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
        power_spectrum(channel_all_data, 'k', 30000)
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '.png', dpi=200)
        plt.close()

    else:
        print('Power spectrum for movement and stationary data is already saved.')








def plot_power_spectrum_moves_light(prm, light_movement, nolight_movement, light_stationary, nolight_stationary, channel):
    ephys_path = prm.get_filepath() + 'Electrophysiology'
    data_path = ephys_path + '/Data'
    analysis_path = ephys_path + '/Analysis'
    spike_path = ephys_path + '/Spike_sorting'

    print(light_movement.shape, nolight_movement.shape)
    if os.path.exists(ephys_path) is False:
        print('Behavioural data will be saved in {}.'.format(ephys_path))
        os.makedirs(ephys_path)
        os.makedirs(data_path)
        os.makedirs(analysis_path)
        os.makedirs(spike_path)

    if os.path.isfile(analysis_path + 'ps_stationary_movement.png') is False:
        print('Plotting and saving power spectra')

        fig, ax = plt.subplots()

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        power_spectrum_log(prm, light_movement, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_light_movement.png', dpi=200)
        power_spectrum_log2(prm, light_movement, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=15, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_light_movement2.png', dpi=200)
        plt.close()


        fig, ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        power_spectrum_log(prm, light_stationary, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_light_stationary.png', dpi=200)
        power_spectrum_log2(prm, light_stationary, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=15, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_light_stationary2.png', dpi=200)
        plt.close()

        fig, ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        power_spectrum_log(prm, nolight_movement, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_ nolight_movement.png', dpi=200)
        power_spectrum_log2(prm, nolight_movement, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=15, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_ nolight_movement2.png', dpi=200)
        plt.close()


        fig, ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        power_spectrum_log(prm, nolight_stationary, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_nolight_stationary.png', dpi=200)
        power_spectrum_log2(prm, nolight_stationary, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=15, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_nolight_stationary2.png', dpi=200)
        plt.close()


    else:
        print('Power spectrum for movement and stationary data is already saved.')






def calculate_and_plot_power_spectrum_split(prm, light_movement, nolight_movement, light_stationary, nolight_stationary, channel):

    # calculate and plot power spectrum
    #plot_power_spectrum(prm, channel_all_data[0,:], channel)
    plot_power_spectrum_moves_light(prm, light_movement, nolight_movement, light_stationary, nolight_stationary,  channel)





def plot_power_spectrum_moves(prm, moves, stationary, channel):

    print('Plotting and saving power spectra')

    fig, ax = plt.subplots()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    power_spectrum_log(prm, moves, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
    fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_moves.png', dpi=200)
    plt.close()


    fig, ax = plt.subplots()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    power_spectrum_log(prm, stationary, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
    fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_stationary.png', dpi=200)
    plt.close()





def calculate_and_plot_power_spectrum(prm, moves, stationary, channel):

    # calculate and plot power spectrum
    #plot_power_spectrum(prm, channel_all_data[0,:], channel)
    plot_power_spectrum_moves(prm, moves, stationary,  channel)



def generate_theta(prm):

    Fs = 30000 # time of sample
    f = 7.5 # frequency of signal generated
    sample = 3000000 # sampling rate
    x = np.arange(sample)
    y = np.sin(2 * np.pi * f * x / Fs) # find sine angle of signal
    plt.plot(x, y)
    plt.xlabel('sample(n)')
    plt.ylabel('voltage(V)')
    plt.show()

    return y


def generate_gamma(prm):

    Fs = 30000 # time of sample
    f = 65 # frequency of signal generated
    sample = 3000000 # sampling rate
    x = np.arange(sample)
    y = np.sin(2 * np.pi * f * x / Fs) # find sine angle of signal
    plt.plot(x, y)
    plt.xlabel('sample(n)')
    plt.ylabel('voltage(V)')
    plt.show()

    return y


def test_fft(prm):

    # calculate and plot power spectrum
    signal_t = generate_theta(prm)
    signal_g = generate_gamma(prm)
    signal = signal_t+signal_g
    plot_test_power_spectrum(prm,signal)


def plot_test_power_spectrum(prm, data):

    print('Plotting and saving power spectra')

    fig, ax = plt.subplots()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)

    power_spectrum(prm, data, 30000, 'k')
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + '_test.png', dpi=200)
    power_spectrum_log(prm, data, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=10, line_width=15, legend='stationary')
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + '_test2.png', dpi=200)
    plt.close()





