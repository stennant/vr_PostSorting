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
import vr_power_calculations


def stack_datasets(prm,channel_data_all,channel_data_all_spikes,theta,gamma):

    #load data
    trials = np.load(prm.get_filepath() + "Behaviour/Data/trial_numbers.npy")
    location = np.load(prm.get_filepath() + "Behaviour/Data/location.npy")
    speed = np.load(prm.get_filepath() + "Behaviour/Data/speed.npy")

    #get all your data arrays in the same shape and order so you can stack them together
    channel_all_data = np.transpose(channel_data_all[0,:])
    channel_all_data = vr_process_movement.remove_beginning_and_end(prm,channel_all_data) # remove start of data (1ms)
    channel_data_all_spikes = np.transpose(channel_data_all_spikes[0,:])
    channel_data_all_spikes = vr_process_movement.remove_beginning_and_end(prm,channel_data_all_spikes)# remove start of data (1ms)
    theta = np.transpose(theta[0,:])
    theta = vr_process_movement.remove_beginning_and_end(prm,theta)# remove start of data(1ms)
    gamma = np.transpose(gamma[0,:])
    gamma = vr_process_movement.remove_beginning_and_end(prm,gamma)# remove start of data(1ms)

    #make an array with the data
    x = np.vstack((trials, location, channel_all_data, channel_data_all_spikes,theta,gamma, speed))
    data = np.transpose(x)

    print('datasets stacked')

    return data


def find_before_and_after_stops(prm,data):

    moving = False
    before_stop = np.zeros((0,7))
    after_stop = np.zeros((0,7))
    for rowcount,row in enumerate(data):
        if(data[rowcount, 6]<=0.7 and moving): # if speed is below threshold
            moving = False
            after_stop = np.vstack((after_stop, data[rowcount:rowcount+7500,:])) # location, (beaconed/non-beaconed/probe), trialid, reward(YES/NO)
            before_stop = np.vstack((before_stop, data[rowcount-7500:rowcount,:])) # location, (beaconed/non-beaconed/probe), trialid, reward(YES/NO)

        if(data[rowcount, 6]>4 and not moving):
            moving = True
            #before_stop = np.vstack((before_stop, data[rowcount:rowcount+7500,:])) # location, (beaconed/non-beaconed/probe), trialid, reward(YES/NO)

    print('Extracted 250 ms before and after stops')

    return before_stop, after_stop


def split_locations(prm,data):

    #split data based on location along the track
    outbound = data[np.where(np.logical_and(data[:,1] > 30, data[:,1] < 80))]
    rewardzone = data[np.where(np.logical_and(data[:,1] > 90, data[:,1] < 110))]
    homebound = data[np.where(np.logical_and(data[:,1] > 110, data[:,1] < 170))]

    print('location split')

    return outbound,rewardzone, homebound


def split_speed(prm,data):
    speed = data[:,6]
    speed = np.delete(speed, np.where(speed[:] <0),0)
    speed = np.delete(speed, np.where(speed[:] >15),0)
    speed_median = np.percentile(speed, 50)
    speed_75 = np.percentile(speed, 75)
    speed_25 = np.percentile(speed, 25)

    #split data based on location along the track
    middle_upper = data[np.where(np.logical_and(data[:,6] > speed_median, data[:,6] < speed_75))]
    upper = data[np.where(data[:,6] > speed_75)]
    middle_lower = data[np.where(np.logical_and(data[:,6] < speed_median, data[:,6] > speed_25))]
    lower = data[np.where(data[:,6] < speed_25)]

    print('speed split')

    return upper, middle_upper, middle_lower, lower


def split_locations_speed(prm,upper, middle_upper, middle_lower, lower):

    #split data based on location along the track
    outbound_m_upper = middle_upper[np.where(np.logical_and(middle_upper[:,1] > 30, middle_upper[:,1] < 80))]
    outbound_upper = upper[np.where(np.logical_and(upper[:,1] > 30, upper[:,1] < 80))]
    outbound_m_lower = middle_lower[np.where(np.logical_and(middle_lower[:,1] > 30, middle_lower[:,1] < 80))]
    outbound_lower = lower[np.where(np.logical_and(lower[:,1] > 30, lower[:,1] < 80))]

    rz_m_upper = middle_upper[np.where(np.logical_and(middle_upper[:,1] > 80, middle_upper[:,1] < 110))]
    rz_upper = upper[np.where(np.logical_and(upper[:,1] > 80, upper[:,1] < 110))]
    rz_m_lower = middle_lower[np.where(np.logical_and(middle_lower[:,1] > 80, middle_lower[:,1] < 110))]
    rz_lower = lower[np.where(np.logical_and(lower[:,1] > 80, lower[:,1] < 110))]

    hb_m_upper = middle_upper[np.where(np.logical_and(middle_upper[:,1] > 110, middle_upper[:,1] < 170))]
    hb_upper = upper[np.where(np.logical_and(upper[:,1] > 110, upper[:,1] < 170))]
    hb_m_lower = middle_lower[np.where(np.logical_and(middle_lower[:,1] > 110, middle_lower[:,1] < 170))]
    hb_lower = lower[np.where(np.logical_and(lower[:,1] > 110, lower[:,1] < 170))]

    print('speed split according to location')

    return outbound_m_upper,outbound_upper,outbound_m_lower,outbound_lower,rz_m_upper,rz_upper,rz_m_lower,rz_lower,hb_m_upper,hb_upper,hb_m_lower,hb_lower


def add_theta_and_gamma_signal(prm,theta, gamma):
    signal = theta[:,4] + gamma[:,5]

    return signal






def stop_start_power_spectra(prm,before_stop, after_stop, channel):

    before_stop = add_theta_and_gamma_signal(prm, before_stop, before_stop)
    after_stop = add_theta_and_gamma_signal(prm, after_stop, after_stop)

    vr_track_location_plots.plot_power_spectrum_before_after_stop(prm, before_stop, after_stop,  channel)


def stop_start_power_spectra_locations(prm,before_stop_outbound, before_stop_rewardzone, before_stop_homebound,after_stop_outbound, after_stop_rewardzone, after_stop_homebound, channel):

    #example data
    # power spectra for just gamma activity
    #vr_track_location_plots.plot_power_spectrum_track_locations_gamma(prm, after_stop_outbound[:,5], after_stop_rewardzone[:,5], after_stop_homebound[:,5], before_stop_outbound[:,5], before_stop_rewardzone[:,5],  before_stop_homebound[:,5], channel)
    #vr_track_location_plots.plot_power_spectrum_track_locations_gamma2(prm, after_stop_outbound[:,5], after_stop_rewardzone[:,5], after_stop_homebound[:,5], before_stop_outbound[:,5], before_stop_rewardzone[:,5],  before_stop_homebound[:,5], channel)
    vr_track_location_plots.plot_power_spectrum_track_locations_gamma3(prm, after_stop_outbound[:,5], after_stop_rewardzone[:,5], after_stop_homebound[:,5], before_stop_outbound[:,5], before_stop_rewardzone[:,5],  before_stop_homebound[:,5], channel)

    # add theta and gamma signal
    before_stop_outbound = add_theta_and_gamma_signal(prm, before_stop_outbound, before_stop_outbound)
    before_stop_rewardzone = add_theta_and_gamma_signal(prm, before_stop_rewardzone, before_stop_rewardzone)
    before_stop_homebound = add_theta_and_gamma_signal(prm, before_stop_homebound, before_stop_homebound)
    after_stop_outbound = add_theta_and_gamma_signal(prm, after_stop_outbound, after_stop_outbound)
    after_stop_rewardzone = add_theta_and_gamma_signal(prm, after_stop_rewardzone, after_stop_rewardzone)
    after_stop_homebound = add_theta_and_gamma_signal(prm, after_stop_homebound, after_stop_homebound)

    #power spectra for theta and gamma
    vr_track_location_plots.plot_power_spectrum_track_locations(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel)


def power_spectra_speed(prm,data, channel):
    # split data based on speed
    upper, middle_upper, middle_lower, lower = split_speed(prm, data)

    #power spectra for just gamma signal
    vr_track_location_plots.plot_power_spectrum_speed_gamma(prm, upper[:,5],middle_upper[:,5], middle_lower[:,5], lower[:,5], channel)

    # add theta and gamma signal
    u = add_theta_and_gamma_signal(prm, upper, upper)
    m_upper = add_theta_and_gamma_signal(prm, middle_upper, middle_upper)
    m_lower = add_theta_and_gamma_signal(prm, middle_lower, middle_lower)
    l = add_theta_and_gamma_signal(prm, lower, lower)

    # power spectra for theta and gamma signal
    vr_track_location_plots.plot_power_spectrum_speed(prm, u,m_upper, m_lower, l, channel)

    return upper,middle_upper, middle_lower, lower


def power_spectra_speed_locations(prm,upper,middle_upper, middle_lower, lower, channel):
    # split data based on speed
    outbound_m_upper,outbound_upper,outbound_m_lower,outbound_lower,rz_m_upper,rz_upper,rz_m_lower,rz_lower,hb_m_upper,hb_upper,hb_m_lower,hb_lower = split_locations_speed(prm, middle_upper,upper, middle_lower, lower)

    #power spectra for just gamma signal
    vr_track_location_plots.plot_power_spectrum_speed_locations_gamma(prm, outbound_m_upper[:,5],outbound_upper[:,5],outbound_m_lower[:,5],outbound_lower[:,5],rz_m_upper[:,5],rz_upper[:,5],rz_m_lower[:,5],rz_lower[:,5],hb_m_upper[:,5],hb_upper[:,5],hb_m_lower[:,5],hb_lower[:,5], channel)

    # add theta and gamma signal
    #middle_upper = add_theta_and_gamma_signal(prm, middle_upper, middle_upper)
    #upper = add_theta_and_gamma_signal(prm, upper, upper)
    #middle_lower = add_theta_and_gamma_signal(prm, middle_lower, middle_lower)
    #lower = add_theta_and_gamma_signal(prm, lower, lower)

    # power spectra for theta and gamma signal
    #vr_track_location_plots.plot_power_spectrum_speed(prm, middle_upper,upper, middle_lower, lower, channel)


def hit_miss_power_spectra_speed(prm,before_stop, after_stop, middle_upper,upper, middle_lower, lower,channel):
    hit_trials = np.load(prm.get_filepath() + "Behaviour/Data/hit_trials.npy")
    miss_trials = np.load(prm.get_filepath() + "Behaviour/Data/miss_trials.npy")

    #just for stationary and movement
    hit_before_stop,miss_before_stop,hit_after_stop,miss_after_stop = vr_split_data.hit_miss_trials(prm, hit_trials, miss_trials, before_stop, after_stop)
    vr_track_location_plots.plot_power_spectrum_hitmiss_gamma(prm, hit_before_stop[:,5],miss_before_stop[:,5], hit_after_stop[:,5], miss_after_stop[:,5], channel)

    #for speed
    hit_middle_upper,hit_upper, hit_middle_lower, hit_lower, miss_middle_upper,miss_upper, miss_middle_lower, miss_lower = vr_split_data.hit_miss_speed(prm, hit_trials, miss_trials, middle_upper,upper, middle_lower, lower)
    vr_track_location_plots.plot_power_spectrum_hitmiss_speed_gamma(prm, hit_middle_upper[:,5],hit_upper[:,5], hit_middle_lower[:,5], hit_lower[:,5],miss_middle_upper[:,5],miss_upper[:,5], miss_middle_lower[:,5], miss_lower[:,5], channel)


def stop_start_continuous_plot(prm,before_stop, after_stop, channel):
        vr_track_location_plots.make_stop_start_continuous_plot(prm, channel, before_stop, after_stop)



"""""
    #old code - requires looping and took too long
    
    before_stop = np.zeros((0,7))
    after_stop = np.zeros((0,7))

    for p, point in enumerate(data):
        if data[p,6] < 0.7:
            before_stop = np.vstack((before_stop,data[p:7500,:]))
            after_stop = np.vstack((after_stop,data[7500:p,:]))


def extractstops(stops):
    moving = False
    data = []
    for row in stops:
        if(row[2]<=STOP_THRESHOLD and moving): # if speed is below threshold
            moving = False
            data.append([float(row[1])+0.2, float(row[0]), int(row[9]), int(row[4])]) # location, (beaconed/non-beaconed/probe), trialid, reward(YES/NO)

        if(row[2]>STOP_THRESHOLD and not moving):
            moving = True
    return np.array(data)
"""""

"""""
def find_before_and_after_stops(prm,data):

    before_stop_indices, after_stop_indices = find_stop_indices(prm,data)
    print(data.shape, 'data.shape')
    print(before_stop_indices.shape, 'before_stop_indices.shape')
    before_stop = np.repeat(before_stop_indices[0,:], 7, axis=1)
    after_stop = np.repeat(after_stop_indices[0,:], 7, axis=1)

    after_stop = np.take(data, after_stop_indices, mode='raise')
    before_stop = np.take(data, before_stop_indices, mode='raise')

    print('found times around stops', before_stop.shape, after_stop.shape)

    return before_stop, after_stop
"""""
