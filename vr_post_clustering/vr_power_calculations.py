
import vr_file_utility
import vr_open_ephys_IO
import os
import matplotlib.pylab as plt
import numpy as np
import vr_filter
import vr_plot_utility
import vr_optogenetics
import vr_process_movement
import vr_fft
import vr_track_location_plots
import vr_split_data
from scipy import signal
import scipy.fftpack
from scipy import integrate


#loop through stops:
#looping 250 ms of data so will be array[datasize] interval = 7500
#find power - simp - between 70 and 90 hz
#store for all stops





# logarithmic power spectrum
def calculate_power(prm, channel, sampling_rate):
    window = scipy.signal.get_window('hamming', len(channel))
    f, pxx_den = signal.periodogram(channel, sampling_rate, window, return_onesided=True)

    return f, np.sqrt(pxx_den)


#
def find_area_under_curve(prm, f, pxx_den):

    power = integrate.simps(pxx_den, f)

    return power



def find_gamma_power(prm, before_stop, after_stop,  channel):
    stop_number = np.arange(0,len(before_stop), 7500)
    #max_stops = np.amax(stop_number)

    before_store = []
    after_store = []

    for stopcount, stop in enumerate(stop_number):
        data_before = before_stop[before_stop[stop:stop+7500,:]]
        f, pxx_den = vr_fft.calculate_power(prm, data_before, 30000)
        power = find_area_under_curve(prm, f, pxx_den)
        before_store.append(power)

        data_after = before_stop[after_stop[stop:stop+7500,:]]
        f, pxx_den = vr_fft.calculate_power(prm, data_after, 30000)
        power = find_area_under_curve(prm, f, pxx_den)
        after_store.append(power)

    return after_store,before_store



def plot_gamma_power(prm,after_store,before_store, channel):

    print('Plotting and saving power spectra for speed quartiles')

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #ax.set_ylim(0,40)
    plt.plot(after_store, 'o', color = 'k')
    plt.plot(before_store, 'o', color = 'b')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)

    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_pulled_gamma_power.png', dpi=200)
    plt.close()






def calculate_and_plot_pooled_gamma_power(prm,before_stop, after_stop,  channel):

    after_store,before_store = find_gamma_power(prm, before_stop, after_stop,  channel)
    plot_gamma_power(prm,after_store,before_store)
