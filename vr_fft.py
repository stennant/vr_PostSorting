'''
power spectrum plots the power spectrum for the given channel
power_spectum_log plots the logarithmic power spectrum

'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from scipy import signal
import matplotlib.pylab as plt
import numpy as np
import os
import vr_plot_continuous_data


# plot power spectrum for channel
def power_spectrum(channel, color, sampling_rate):
    # channel = data['data'][:,10][-50947920:]
    # #channel 11, 5th of the data is removed from the beginning because of noise
    ps = np.abs(np.fft.fft(channel))**2
    time_step = 1 / int(sampling_rate)
    freqs = np.fft.fftfreq(channel.size, time_step)
    idx = np.argsort(freqs)
    plt.plot(freqs[idx], ps[idx], color, linewidth=10)
    plt.xlim(0, 200)


# plot logarithmic power spectrum for channel
def power_spectrum_log(prm, channel, sampling_rate, color, filename, title="$Power  spectrum$", x_lim=1000, line_width=15,
                       legend='set legend'):
    window = scipy.signal.get_window('hamming', len(channel))
    f, pxx_den = signal.periodogram(channel, sampling_rate, window)

    plt.semilogy(f, np.sqrt(pxx_den), color, line_width)
    plt.title(title)
#    plt.legend(loc='upper right')
#    plt.legend(frameon=False)

    plt.xlim([0, x_lim])
    plt.ylim([5, 1000])
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

        #raw_data = np.asanyarray(fr.get_raw_data())

        #stationary_signal = signal_for_indices.signal_for_indices_multi_ch(prm.get_good_channels(), raw_data.T,
                                                                           #stationary)
        #moves_signal = signal_for_indices.signal_for_indices_multi_ch(prm.get_good_channels(), raw_data.T, moves)

        #filename = analysis_path + '/ps_stationary_movement'
        fig, ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

        #plt.xticks([0, 50, 100, 150])
        #plt.yticks([10, 100, 1000])


        power_spectrum_log(prm, channel_all_data, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=1000, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '.png', dpi=200)
        plt.close()
        #Ffrpower_spectrum_log(prm, moves_signal, 30000, 'b', filename, title="$Power spectrum$", x_lim=150, line_width=15, legend='movement')
        #plt.show()
        #plt.close(fig)
    else:
        print('Power spectrum for movement and stationary data is already saved.')




def calculate_and_plot_power_spectrum(prm):

    for c, channel in enumerate(np.arange(1,16,1)):

        #load continuous data
        channel_all_data = vr_plot_continuous_data.load_continuous_data(prm, channel)

        # calculate and plot power spectrum
        plot_power_spectrum(prm, channel_all_data[0,:], channel)
