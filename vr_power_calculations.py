
import vr_file_utility
import vr_open_ephys_IO
import os
import matplotlib.pylab as plt
import numpy as np
from scipy import stats
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
import vr_power_calculations_plots
import vr_track_location_analysis

#loop through stops:
#looping 250 ms of data so will be array[datasize] interval = 7500
#find power - simp - between 70 and 90 hz
#store for all stops


# main functions
def calculate_power(prm, channel, sampling_rate):
    window = scipy.signal.get_window('hamming', len(channel))
    f, pxx_den = signal.periodogram(channel, sampling_rate, window, return_onesided=True)

    print(f,'f')
    return f, np.sqrt(pxx_den)


def find_area_under_curve(prm, f, pxx_den):

    power = integrate.simps(pxx_den, f)

    return power


def find_gamma_power(prm, before_stop, after_stop,  channel):
    stop_number = np.arange(1,len(before_stop), 7500)
    #max_stops = np.amax(stop_number)

    before_store = []
    after_store = []

    for stopcount, stop in enumerate(stop_number):
        data_before = before_stop[stop:stop+7500]
        f, pxx_den = vr_fft.calculate_power(prm, data_before, 30000)
        power = find_area_under_curve(prm, f, pxx_den)
        before_store.append(power)

        data_after = after_stop[stop:stop+7500]
        f, pxx_den = vr_fft.calculate_power(prm, data_after, 30000)
        power = find_area_under_curve(prm, f, pxx_den)
        after_store.append(power)

    return np.array(after_store),np.array(before_store)


def find_gamma_power_difference(after_store,before_store):
    store=np.zeros((after_store.shape))
    for xcount,x in enumerate(store):
        store[xcount] = after_store[xcount]-before_store[xcount]

    return store


def get_average_speed(prm,speed_data):
    time_windows = np.arange(1,len(speed_data), 7500)
    speed_windows = np.zeros((len(time_windows)))

    for timebin, time in enumerate(time_windows):
        average_speed = np.nanmean(speed_data[time:time+7500])

        speed_windows[timebin] = average_speed

    return speed_windows


def get_gamma_per_window(prm,gamma_data):
    time_windows = np.arange(1,len(gamma_data), 7500)
    gamma_windows = np.zeros((len(time_windows)))

    for timebin, time in enumerate(time_windows):
        gamma = gamma_data[time:time+7500]
        f, pxx_den = vr_fft.calculate_power(prm, gamma, 30000)
        power = find_area_under_curve(prm, f, pxx_den)

        gamma_windows[timebin] = power

    return gamma_windows


def bin_speed_data(prm,data):
    min_speed = 0
    max_speed = 13
    interval = (max_speed - min_speed)/200
    bins = np.arange(min_speed,max_speed,interval)
    speed_bins = np.zeros((len(bins)))

    for bcount,b in enumerate(bins):

        speed_b = data[np.where(np.logical_and(data[:,0] >= b, data[:,0] < b+interval))]
        speed_b_avg = np.nanmean(speed_b[:,1])

        speed_bins[bcount] = speed_b_avg

    return bins, speed_bins


def linear_regression(bins,values):
    slope,intercept,r_value, p_value, std_err = stats.linregress(bins,values)
    ablinevalues = []
    for icount, i in enumerate(bins):
        ablinevalues.append(slope*i+intercept)

    return ablinevalues, slope,intercept,r_value, p_value




# called functions

def find_average_stop_start_speed(prm, before_stop, after_stop,  channel):
    stop_number = np.arange(1,len(before_stop), 7500)

    before_store = []
    after_store = []

    for stopcount, stop in enumerate(stop_number):
        data_before = before_stop[stop:stop+7500]
        avg=np.nanmean(data_before)
        before_store.append(avg)

        data_after = after_stop[stop:stop+7500]
        avg=np.nanmean(data_after)
        after_store.append(avg)

    return np.array(after_store),np.array(before_store)


def calculate_power_versus_speed(prm,data, channel):
    speed = get_average_speed(prm,data[:,6])
    gamma_power = get_gamma_per_window(prm,data[:,5])
    theta_power = get_gamma_per_window(prm,data[:,4])

    data = np.vstack((speed,gamma_power)); data = np.transpose(data)
    bins,speed_bins = bin_speed_data(prm,data)
    vr_power_calculations_plots.plot_gamma_power_speed(prm, bins,speed_bins, channel)

    #data = np.vstack((speed,theta_power)); data = np.transpose(data)
    #bins,speed_bins = bin_speed_data(prm,data)
    #vr_power_calculations_plots.plot_theta_power_speed(prm, bins,speed_bins, channel)


def calculate_and_plot_pooled_gamma_power_stop_start(prm,before_stop, after_stop,  channel):

    after_store,before_store = find_gamma_power(prm, before_stop[:,5], after_stop[:,5],  channel)
    vr_power_calculations_plots.plot_gamma_power_stop_start(prm,after_store,before_store, channel)
    #difference = find_gamma_power_difference(after_store,before_store)
    #vr_power_calculations_plots.plot_gamma_power_difference_stop_start(prm,difference, channel)


def calculate_and_plot_pooled_gamma_power_stop_start_locations(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel):

    after_store_ob = get_gamma_per_window(prm,after_stop_outbound[:,5]);before_store_ob = get_gamma_per_window(prm,before_stop_outbound[:,5])
    after_store_rz = get_gamma_per_window(prm,after_stop_rewardzone[:,5]);before_store_rz = get_gamma_per_window(prm,before_stop_rewardzone[:,5])
    after_store_hb = get_gamma_per_window(prm,after_stop_homebound[:,5]);before_store_hb = get_gamma_per_window(prm,before_stop_homebound[:,5])

    vr_power_calculations_plots.plot_gamma_power_stop_start_location(prm,after_store_ob,before_store_ob,after_store_rz,before_store_rz,after_store_hb,before_store_hb, channel)

    #difference_ob = find_gamma_power_difference(after_store_ob,before_store_ob)
    #difference_rz = find_gamma_power_difference(after_store_rz,before_store_rz)
    #difference_hb = find_gamma_power_difference(after_store_hb,before_store_hb)

    #vr_power_calculations_plots.plot_gamma_power_difference_stop_start_location(prm,difference_ob,difference_rz, difference_hb,channel)


def calculate_and_plot_pooled_gamma_power_stop_start_locations_hit_miss(prm,  bs_outbound_hit, bs_outbound_miss, as_outbound_hit,as_outbound_miss, bs_rz_hit, bs_rz_miss, as_rz_hit, as_rz_miss, bs_homebound_hit, bs_homebound_miss, as_homebound_hit, as_homebound_miss, channel):

    after_store_ob_hit = get_gamma_per_window(prm,as_outbound_hit[:,5]);before_store_ob_hit = get_gamma_per_window(prm,bs_outbound_hit[:,5])
    after_store_rz_hit = get_gamma_per_window(prm,as_rz_hit[:,5]);before_store_rz_hit = get_gamma_per_window(prm,bs_rz_hit[:,5])
    after_store_hb_hit = get_gamma_per_window(prm,as_homebound_hit[:,5]);before_store_hb_hit = get_gamma_per_window(prm,bs_homebound_hit[:,5])

    after_store_ob_miss = get_gamma_per_window(prm,as_outbound_miss[:,5]);before_store_ob_miss = get_gamma_per_window(prm,bs_outbound_miss[:,5])
    after_store_rz_miss = get_gamma_per_window(prm,as_rz_miss[:,5]);before_store_rz_miss = get_gamma_per_window(prm,bs_rz_miss[:,5])
    after_store_hb_miss = get_gamma_per_window(prm,as_homebound_miss[:,5]);before_store_hb_miss = get_gamma_per_window(prm,bs_homebound_miss[:,5])

    vr_power_calculations_plots.plot_gamma_power_stop_start_location_hit_miss(prm,after_store_ob_hit,after_store_rz_hit,after_store_hb_hit,before_store_ob_hit,before_store_rz_hit,before_store_hb_hit, after_store_ob_miss,after_store_rz_miss,after_store_hb_miss,before_store_ob_miss,before_store_rz_miss,before_store_hb_miss, channel)

    #difference_ob = find_gamma_power_difference(after_store_ob,before_store_ob)
    #difference_rz = find_gamma_power_difference(after_store_rz,before_store_rz)
    #difference_hb = find_gamma_power_difference(after_store_hb,before_store_hb)

    #vr_power_calculations_plots.plot_gamma_power_difference_stop_start_location(prm,difference_ob,difference_rz, difference_hb,channel)




def calculate_and_plot_average_stop_start_speed(prm,before_stop, after_stop,  channel):

    after_store,before_store = find_average_stop_start_speed(prm, before_stop[:,6], after_stop[:,6],  channel)
    vr_track_location_plots.plot_average_stop_start_speed(prm,after_store,before_store)


def calculate_power_hit_miss(prm,data, channel):
    hit_data, miss_data = vr_split_data.split_all_data_hit_miss(prm,data)
    #plot power spectra
    hit_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, hit_data, hit_data)
    miss_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, miss_data, miss_data)

    vr_track_location_plots.plot_power_spectrum_all_hitmiss(prm, hit_data_theta,miss_data_theta, channel)
    vr_track_location_plots.plot_power_spectrum_all_hitmiss_gamma(prm, hit_data[:,5],miss_data[:,5], channel)
    #average area under curve etc for all stops
    hit_power = get_gamma_per_window(prm,hit_data[:,5])
    miss_power = get_gamma_per_window(prm,miss_data[:,5])
    vr_power_calculations_plots.plot_gamma_power_hit_miss(prm, hit_power,miss_power, channel)
    #hit_power = get_gamma_per_window(prm,hit_data[:,4])
    #miss_power = get_gamma_per_window(prm,miss_data[:,4])
    #vr_power_calculations_plots.plot_theta_power_hit_miss(prm, hit_power,miss_power, channel)


def calculate_power_hit_miss_success(prm,data, channel):
    hit_data, miss_data,success_data = vr_split_data.split_all_data_hit_miss_success(prm,data)
    #plot power spectra
    hit_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, hit_data, hit_data)
    miss_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, miss_data, miss_data)
    sucess_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, success_data, success_data)

    vr_track_location_plots.plot_power_spectrum_all_hitmiss_success(prm, hit_data_theta,miss_data_theta, sucess_data_theta,channel)
    vr_track_location_plots.plot_power_spectrum_all_hitmiss_success_gamma(prm, hit_data[:,5],miss_data[:,5], success_data[:,5],channel)
    #average area under curve etc for all stops
    hit_power = get_gamma_per_window(prm,hit_data[:,5])
    miss_power = get_gamma_per_window(prm,miss_data[:,5])
    success_power = get_gamma_per_window(prm,success_data[:,5])
    vr_power_calculations_plots.plot_gamma_power_hit_miss_success(prm, hit_power,miss_power, success_power,channel)
    #hit_power = get_gamma_per_window(prm,hit_data[:,4])
    #miss_power = get_gamma_per_window(prm,miss_data[:,4])
    #success_power = get_gamma_per_window(prm,success_data[:,4])
    #vr_power_calculations_plots.plot_theta_power_hit_miss_success(prm, hit_power,miss_power, success_power,channel)


def calculate_power_hit_miss_locations(prm,data, channel):
    hit_data, miss_data = vr_split_data.split_all_data_hit_miss(prm,data)

    hit_data_ob, hit_data_rz,hit_data_hb = vr_track_location_analysis.split_locations(prm,hit_data)
    miss_data_ob, miss_data_rz,miss_data_hb = vr_track_location_analysis.split_locations(prm,miss_data)

    #plot power spectra
    #hit_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, hit_data, hit_data)
    #miss_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, miss_data, miss_data)

    #vr_track_location_plots.plot_power_spectrum_all_hitmiss(prm, hit_data_theta,miss_data_theta, channel)
    #vr_track_location_plots.plot_power_spectrum_all_hitmiss_gamma(prm, hit_data[:,5],miss_data[:,5], channel)
    #average area under curve etc for all stops
    hit_power_ob = get_gamma_per_window(prm,hit_data_ob[:,5]);hit_power_rz = get_gamma_per_window(prm,hit_data_rz[:,5]);hit_power_hb = get_gamma_per_window(prm,hit_data_hb[:,5])
    miss_power_ob = get_gamma_per_window(prm,miss_data_ob[:,5]);miss_power_rz = get_gamma_per_window(prm,miss_data_rz[:,5]);miss_power_hb = get_gamma_per_window(prm,miss_data_hb[:,5])
    vr_power_calculations_plots.plot_gamma_power_hit_miss_locations(prm, hit_power_ob,miss_power_ob, hit_power_rz,miss_power_rz,hit_power_hb,miss_power_hb,channel)

    #it_power_ob = get_gamma_per_window(prm,hit_data_ob[:,4]);hit_power_rz = get_gamma_per_window(prm,hit_data_rz[:,4]);hit_power_hb = get_gamma_per_window(prm,hit_data_hb[:,4])
    #miss_power_ob = get_gamma_per_window(prm,miss_data_ob[:,4]);miss_power_rz = get_gamma_per_window(prm,miss_data_rz[:,4]);miss_power_hb = get_gamma_per_window(prm,miss_data_hb[:,4])
    #vr_power_calculations_plots.plot_theta_power_hit_miss_locations(prm, hit_power_ob,miss_power_ob, hit_power_rz,miss_power_rz,hit_power_hb,miss_power_hb,channel)


def calculate_power_hit_miss_success_locations(prm,data, channel):
    hit_data, miss_data,success_data = vr_split_data.split_all_data_hit_miss_success(prm,data)

    hit_data_ob, hit_data_rz,hit_data_hb = vr_track_location_analysis.split_locations(prm,hit_data)
    miss_data_ob, miss_data_rz,miss_data_hb = vr_track_location_analysis.split_locations(prm,miss_data)
    success_data_ob, success_data_rz,success_data_hb = vr_track_location_analysis.split_locations(prm,success_data)

    #plot power spectra
    #hit_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, hit_data, hit_data)
    #miss_data_theta = vr_track_location_analysis.add_theta_and_gamma_signal(prm, miss_data, miss_data)

    #vr_track_location_plots.plot_power_spectrum_all_hitmiss(prm, hit_data_theta,miss_data_theta, channel)
    #vr_track_location_plots.plot_power_spectrum_all_hitmiss_gamma(prm, hit_data[:,5],miss_data[:,5], channel)
    #average area under curve etc for all stops
    hit_power_ob = get_gamma_per_window(prm,hit_data_ob[:,5]);hit_power_rz = get_gamma_per_window(prm,hit_data_rz[:,5]);hit_power_hb = get_gamma_per_window(prm,hit_data_hb[:,5])
    miss_power_ob = get_gamma_per_window(prm,miss_data_ob[:,5]);miss_power_rz = get_gamma_per_window(prm,miss_data_rz[:,5]);miss_power_hb = get_gamma_per_window(prm,miss_data_hb[:,5])
    success_power_ob = get_gamma_per_window(prm,success_data_ob[:,5]);success_power_rz = get_gamma_per_window(prm,success_data_rz[:,5]);success_power_hb = get_gamma_per_window(prm,success_data_hb[:,5])
    vr_power_calculations_plots.plot_gamma_power_hit_miss_success_locations(prm, hit_power_ob,miss_power_ob, success_power_ob,hit_power_rz,miss_power_rz,success_power_rz,hit_power_hb,miss_power_hb,success_power_hb,channel)

    #hit_power_ob = get_gamma_per_window(prm,hit_data_ob[:,5]);hit_power_rz = get_gamma_per_window(prm,hit_data_rz[:,5]);hit_power_hb = get_gamma_per_window(prm,hit_data_hb[:,5])
    #miss_power_ob = get_gamma_per_window(prm,miss_data_ob[:,5]);miss_power_rz = get_gamma_per_window(prm,miss_data_rz[:,5]);miss_power_hb = get_gamma_per_window(prm,miss_data_hb[:,5])
    #success_power_ob = get_gamma_per_window(prm,success_data_ob[:,5]);success_power_rz = get_gamma_per_window(prm,success_data_rz[:,5]);success_power_hb = get_gamma_per_window(prm,success_data_hb[:,5])
    #vr_power_calculations_plots.plot_theta_power_hit_miss_success_locations(prm, hit_power_ob,miss_power_ob, success_power_ob,hit_power_rz,miss_power_rz,success_power_rz,hit_power_hb,miss_power_hb,success_power_hb,channel)


def calculate_power_speed_hit_miss(prm,data, channel):
    hit_data, miss_data = vr_split_data.split_all_data_hit_miss(prm,data)

    speed_hit = get_average_speed(prm,hit_data[:,6])
    speed_miss = get_average_speed(prm,miss_data[:,6])
    gamma_power_hit = get_gamma_per_window(prm,hit_data[:,5])
    gamma_power_miss = get_gamma_per_window(prm,miss_data[:,5])
    theta_power_hit = get_gamma_per_window(prm,hit_data[:,4])
    theta_power_miss = get_gamma_per_window(prm,miss_data[:,4])

    #plot for gamma
    hit_data = np.vstack((speed_hit,gamma_power_hit)); hit_data = np.transpose(hit_data)
    miss_data = np.vstack((speed_miss,gamma_power_miss)); miss_data = np.transpose(miss_data)
    bins_hit,speed_bins_hit = bin_speed_data(prm,hit_data)
    bins_miss,speed_bins_miss = bin_speed_data(prm,miss_data)
    vr_power_calculations_plots.plot_gamma_power_speed_hit_miss(prm, bins_hit,speed_bins_hit,bins_miss,speed_bins_miss, channel)

    #plot for theta
    #hit_data = np.vstack((speed_hit,theta_power_hit)); hit_data = np.transpose(hit_data)
    #miss_data = np.vstack((speed_miss,theta_power_miss)); miss_data = np.transpose(miss_data)
    #bins_hit,speed_bins_hit = bin_speed_data(prm,hit_data)
    #bins_miss,speed_bins_miss = bin_speed_data(prm,miss_data)
    #vr_power_calculations_plots.plot_theta_power_speed_hit_miss(prm, bins_hit,speed_bins_hit,bins_miss,speed_bins_miss, channel)


def calculate_power_speed_hit_miss_success(prm,data, channel):
    hit_data, miss_data,success_data = vr_split_data.split_all_data_hit_miss_success(prm,data)

    speed_hit = get_average_speed(prm,hit_data[:,6])
    speed_miss = get_average_speed(prm,miss_data[:,6])
    speed_success = get_average_speed(prm,success_data[:,6])
    gamma_power_hit = get_gamma_per_window(prm,hit_data[:,5])
    gamma_power_miss = get_gamma_per_window(prm,miss_data[:,5])
    gamma_power_success = get_gamma_per_window(prm,success_data[:,5])
    theta_power_hit = get_gamma_per_window(prm,hit_data[:,4])
    theta_power_miss = get_gamma_per_window(prm,miss_data[:,4])
    theta_power_success = get_gamma_per_window(prm,success_data[:,4])

    #plot for gamma
    hit_data = np.vstack((speed_hit,gamma_power_hit)); hit_data = np.transpose(hit_data)
    miss_data = np.vstack((speed_miss,gamma_power_miss)); miss_data = np.transpose(miss_data)
    success_data = np.vstack((speed_success,gamma_power_success)); success_data = np.transpose(success_data)
    bins_hit,speed_bins_hit = bin_speed_data(prm,hit_data)
    bins_miss,speed_bins_miss = bin_speed_data(prm,miss_data)
    bins_success,speed_bins_success = bin_speed_data(prm,success_data)
    vr_power_calculations_plots.plot_gamma_power_speed_hit_miss_success(prm, bins_hit,speed_bins_hit,bins_miss,speed_bins_miss,bins_success,speed_bins_success, channel)

    #plot for theta
    #hit_data = np.vstack((speed_hit,theta_power_hit)); hit_data = np.transpose(hit_data)
    #miss_data = np.vstack((speed_miss,theta_power_miss)); miss_data = np.transpose(miss_data)
    #success_data = np.vstack((speed_success,theta_power_success)); success_data = np.transpose(success_data)
    #bins_hit,speed_bins_hit = bin_speed_data(prm,hit_data)
    #bins_miss,speed_bins_miss = bin_speed_data(prm,miss_data)
    #bins_success,speed_bins_success = bin_speed_data(prm,success_data)
    #vr_power_calculations_plots.plot_theta_power_speed_hit_miss_success(prm, bins_hit,speed_bins_hit,bins_miss,speed_bins_miss,bins_success,speed_bins_success, channel)


def calculate_power_speed_hit_miss_locations(prm,data, channel):
    hit_data, miss_data = vr_split_data.split_all_data_hit_miss(prm,data)

    hit_data_ob, hit_data_rz,hit_data_hb = vr_track_location_analysis.split_locations(prm,hit_data)
    miss_data_ob, miss_data_rz,miss_data_hb = vr_track_location_analysis.split_locations(prm,miss_data)

    speed_hit_ob = get_average_speed(prm,hit_data_ob[:,6]);speed_hit_rz = get_average_speed(prm,hit_data_rz[:,6]);speed_hit_hb = get_average_speed(prm,hit_data_hb[:,6])
    speed_miss_ob = get_average_speed(prm,miss_data_ob[:,6]);speed_miss_rz = get_average_speed(prm,miss_data_rz[:,6]);speed_miss_hb = get_average_speed(prm,miss_data_hb[:,6])
    gamma_power_hit_ob = get_gamma_per_window(prm,hit_data_ob[:,5]);gamma_power_hit_rz = get_gamma_per_window(prm,hit_data_rz[:,5]);gamma_power_hit_hb = get_gamma_per_window(prm,hit_data_hb[:,5])
    gamma_power_miss_ob = get_gamma_per_window(prm,miss_data_ob[:,5]);gamma_power_miss_rz = get_gamma_per_window(prm,miss_data_rz[:,5]);gamma_power_miss_hb = get_gamma_per_window(prm,miss_data_hb[:,5])
    theta_power_hit_ob = get_gamma_per_window(prm,hit_data_ob[:,4]);theta_power_hit_rz = get_gamma_per_window(prm,hit_data_rz[:,4]);theta_power_hit_hb = get_gamma_per_window(prm,hit_data_hb[:,4])
    theta_power_miss_ob = get_gamma_per_window(prm,miss_data_ob[:,4]);theta_power_miss_rz = get_gamma_per_window(prm,miss_data_rz[:,4]);theta_power_miss_hb = get_gamma_per_window(prm,miss_data_hb[:,4])

    #plot gamma
    hit_data_ob = np.vstack((speed_hit_ob,gamma_power_hit_ob)); hit_data_ob = np.transpose(hit_data_ob)
    miss_data_ob = np.vstack((speed_miss_ob,gamma_power_miss_ob)); miss_data_ob = np.transpose(miss_data_ob)
    hit_data_rz = np.vstack((speed_hit_rz,gamma_power_hit_rz)); hit_data_rz = np.transpose(hit_data_rz)
    miss_data_rz = np.vstack((speed_miss_rz,gamma_power_miss_rz)); miss_data_rz = np.transpose(miss_data_rz)
    hit_data_hb = np.vstack((speed_hit_hb,gamma_power_hit_hb)); hit_data_hb = np.transpose(hit_data_hb)
    miss_data_hb = np.vstack((speed_miss_hb,gamma_power_miss_hb)); miss_data_hb = np.transpose(miss_data_hb)
    bins_hit_ob,speed_bins_hit_ob = bin_speed_data(prm,hit_data_ob);bins_hit_rz,speed_bins_hit_rz = bin_speed_data(prm,hit_data_rz);bins_hit_hb,speed_bins_hit_hb = bin_speed_data(prm,hit_data_hb)
    bins_miss_ob,speed_bins_miss_ob = bin_speed_data(prm,miss_data_ob);bins_miss_rz,speed_bins_miss_rz = bin_speed_data(prm,miss_data_rz);bins_miss_hb,speed_bins_miss_hb = bin_speed_data(prm,miss_data_hb)
    vr_power_calculations_plots.plot_gamma_power_speed_hit_miss_locations(prm, bins_hit_ob,speed_bins_hit_ob,bins_miss_ob,speed_bins_miss_ob,bins_hit_rz,speed_bins_hit_rz,bins_miss_rz,speed_bins_miss_rz, bins_hit_hb,speed_bins_hit_hb,bins_miss_hb,speed_bins_miss_hb, channel)

    #plot theta
    #hit_data_ob = np.vstack((speed_hit_ob,theta_power_hit_ob)); hit_data_ob = np.transpose(hit_data_ob)
    #miss_data_ob = np.vstack((speed_miss_ob,theta_power_miss_ob)); miss_data_ob = np.transpose(miss_data_ob)
    #hit_data_rz = np.vstack((speed_hit_rz,theta_power_hit_rz)); hit_data_rz = np.transpose(hit_data_rz)
    #miss_data_rz = np.vstack((speed_miss_rz,theta_power_miss_rz)); miss_data_rz = np.transpose(miss_data_rz)
    #hit_data_hb = np.vstack((speed_hit_hb,theta_power_hit_hb)); hit_data_hb = np.transpose(hit_data_hb)
    #miss_data_hb = np.vstack((speed_miss_hb,theta_power_miss_hb)); miss_data_hb = np.transpose(miss_data_hb)
    #bins_hit_ob,speed_bins_hit_ob = bin_speed_data(prm,hit_data_ob);bins_hit_rz,speed_bins_hit_rz = bin_speed_data(prm,hit_data_rz);bins_hit_hb,speed_bins_hit_hb = bin_speed_data(prm,hit_data_hb)
    #bins_miss_ob,speed_bins_miss_ob = bin_speed_data(prm,miss_data_ob);bins_miss_rz,speed_bins_miss_rz = bin_speed_data(prm,miss_data_rz);bins_miss_hb,speed_bins_miss_hb = bin_speed_data(prm,miss_data_hb)
    #vr_power_calculations_plots.plot_theta_power_speed_hit_miss_locations(prm, bins_hit_ob,speed_bins_hit_ob,bins_miss_ob,speed_bins_miss_ob,bins_hit_rz,speed_bins_hit_rz,bins_miss_rz,speed_bins_miss_rz, bins_hit_hb,speed_bins_hit_hb,bins_miss_hb,speed_bins_miss_hb, channel)
