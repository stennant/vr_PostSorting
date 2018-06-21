import itertools
import matplotlib.pylab as plt
import numpy as np
import math
from scipy import stats
import os
import vr_parameters
import vr_stops
import vr_sorted_firing_times
import vr_plot_utility
from scipy.stats import uniform


def get_stops_on_trials(prm):
    location, number_of_trials, all_stops, track_beginnings = vr_stops.get_data_for_stops_on_trials(prm)
    stops_on_trials = vr_stops.get_stops_on_trials_find_stops(location, number_of_trials, all_stops, track_beginnings)
    return stops_on_trials


def get_spikes_on_trials(prm, firing_times_unit):
    location, number_of_trials, trials, all_stops, track_beginnings = vr_stops.get_data_for_spikes_on_trials(prm, firing_times_unit)
    time = vr_sorted_firing_times.get_time_in_bin(prm, location, trials)
    stops_on_trials = vr_stops.get_spikes_on_trials_find_stops(location, number_of_trials, time, all_stops, track_beginnings)
    return stops_on_trials, all_stops


def wrap_spike_interval(spike_list):
    interval_list=[]
    for rowcount, row in enumerate(spike_list[:-1]):
        interval = spike_list[rowcount+1] - spike_list[rowcount]
        if interval < 0:
            interval = (200-(spike_list[rowcount])) + spike_list[rowcount+1]
        interval_list = np.append(interval,interval_list)
    return interval_list


def get_spike_interval(prm, firing_times_unit):
    spike_list=[]
    for rowcount, row in enumerate(firing_times_unit):
        spike_list = np.append(spike_list, row)

    interval_list = wrap_spike_interval(spike_list)
    return interval_list


def distribution_of_intervals(interval_list):
    inverval_locations=np.zeros((200))

    for loc_count,loc in enumerate(np.arange(1,200,1)):
        intervals = interval_list[np.where(np.logical_and(interval_list <= (loc+1),  interval_list > (loc)))]
        prop = len(intervals)*(1/len(interval_list))
        inverval_locations[loc_count] = prop
    return inverval_locations


def spike_histogram(spikes_on_trials):
    print('Calculating spike histogram')
    bin_locations=np.zeros((200, len(spikes_on_trials))); bin_locations[:,:] = np.nan
    bin_locations_nb=np.zeros((200, len(spikes_on_trials))); bin_locations_nb[:,:] = np.nan

    for ith, trial in enumerate(spikes_on_trials):
        if trial.size == 0:
            continue

        if ith % 5 == 0 and ith > 0:
            for loc_count,loc in enumerate(np.arange(1,200,1)):
                stop_sum = trial[np.where(np.logical_and(trial <= (loc+1),  trial > (loc)))]
                sum = (len(stop_sum))/len(spikes_on_trials)
                bin_locations_nb[loc_count, ith] = sum

        else:
            for loc_count,loc in enumerate(np.arange(1,200,1)):
                stop_sum = trial[np.where(np.logical_and(trial <= (loc+1),  trial > (loc)))]
                sum = (len(stop_sum))/len(spikes_on_trials)
                bin_locations[loc_count, ith] = sum

    return bin_locations, bin_locations_nb



def time_normalised_spike_histogram(bin_locations, times):
    print('Calculating time normalized spike histogram')
    time_bin_locations=np.zeros((200, bin_locations.shape[1])); time_bin_locations[:,:] = np.nan

    for ith, trial in enumerate(bin_locations[1]):

        for loc_count,loc in enumerate(bin_locations,0):
            bin_time = times[loc_count, ith]
            bin_spike_number = bin_locations[loc_count, ith]
            normalised_time = (bin_spike_number/bin_time) *10
            time_bin_locations[loc_count,ith] = normalised_time
    return time_bin_locations


# SHUFFLE STOPS
def shuffle_stops(shuffled_spikes_on_trials):
    print('Shuffling spikes')
    for ith, trial in enumerate(shuffled_spikes_on_trials):
        if trial.size == 0:
            continue
        # create an array that contains the amount by which every stop will be shuffled
        rand_rotation = uniform.rvs(loc=0, scale=20, size=trial.shape[1])
        # add random value
        #print(spikes_on_trials[ith], 'rand_rotation', rand_rotation)
        shuffled_spikes_on_trials[ith] = rand_rotation

    return shuffled_spikes_on_trials


def shuffled_vs_real_histogram(prm, spikes, shuffled_spikes, times, bin_locations):
    shuff = np.zeros((200, bin_locations.shape[1]))
    real = np.zeros((200, bin_locations.shape[1]))
    for ith, trial in enumerate(spikes):
        if trial.size == 0:
            continue
        for loc_count,loc in enumerate(np.arange(1,200,1)):
            sp = trial[np.where(np.logical_and(trial <= (loc+1),  trial > (loc)))]
            bin_time = times[loc_count, ith]
            real[loc_count, ith] = (len(sp)/bin_time)*10

    for ith, trial in enumerate(shuffled_spikes):
        if trial.size == 0:
            continue
        for loc_count,loc in enumerate(np.arange(1,200,1)):
            sp = trial[np.where(np.logical_and(trial <= (loc+1),  trial > (loc)))]
            bin_time = times[loc_count, ith]
            shuff[loc_count, ith] = (len(sp)/bin_time)*10
    return shuff,real


def calculate_p_value(shuff,re):
    print('Calculating p values')
    p_values=np.zeros((200)); p_values[:] = np.nan

    for loc_count,loc in enumerate(np.arange(1,200,1)):
        shuffled = shuff[loc_count,:]
        real = re[loc_count,:]
        print(real, 'real', shuffled, 'shuffled')
        tstat, p_value = stats.ttest_ind(shuffled,real, equal_var = True)
        print(p_value, tstat)
        p_values[loc_count] = p_value
    return p_values


def make_plot(prm, spikes_on_trials, channelcount, stops_on_trials, time_normalised_bin_locations, time_normalised_bin_locations_nb, inverval_locations, p_values):
    fig = plt.figure(figsize = (12,10))
    ax = fig.add_subplot(221)
    plt.xlim(0, 200)

    # plot stops
    for ith, trial in enumerate(stops_on_trials):
        if trial.size == 0:
            continue
        try:
            if ith % 5 == 0 and ith > 0:
                ax.plot(trial[:,1:], ith, 'o', markersize=5, c='g', markeredgewidth=0.0, alpha=0.5)
            else:
                ax.plot(trial[:,1:], ith, 'o', markersize=5, c='g', markeredgewidth=0.0, alpha=0.5)
        except ZeroDivisionError:
            print('empty trial found...deleting...')
    ax.plot(0, 0, 'o', markersize=5, c='g', markeredgewidth=0.0, alpha=0.5, label = 'Stops')

    # plot spikes
    for ith, trial in enumerate(spikes_on_trials):
        if trial.size == 0:
            continue
        try:
            if ith % 5 == 0 and ith > 0:
                ax.plot(trial, ith, '|', markersize=4, c='b')
            else:
                ax.plot(trial, ith, '|',markersize=4, c='k')
        except ZeroDivisionError:
            print('empty trial found...deleting...')
    ax.plot(0, 0, '|', markersize=6, c='k', label = 'Spike (B)')
    ax.plot(0, 0, '|', markersize=6, c='b', label = 'Spike (NB)')


    # make plot aesthetically pleasing
    plt.ylim(.5, len(stops_on_trials) + .5)
    plt.ylabel('Spikes on trials', fontsize=20, labelpad = 20)
    plt.xlabel('Location (cm)', fontsize=20, labelpad = 20)
    ax.axvspan(88, 88+22, facecolor='DarkGreen', alpha=.25, linewidth =0)
    ax.axvspan(0, 30, facecolor='k', linewidth =0, alpha=.25) # black box
    ax.axvspan(200-30, 200, facecolor='k', linewidth =0, alpha=.25)# black box
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6,labelsize =20)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6, labelsize =20)
    ax.axvline(0, linewidth = 3, color = 'black') # bold line on the y axis
    ax.axhline(.4, linewidth = 3, color = 'black') # bold line on the x axis
    ax.locator_params(axis = 'x', nbins=3) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=4) # set number of ticks on y axis
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticklabels(['', '', ''])
    vr_plot_utility.makelegend(fig,ax, 0.9)

    ax = fig.add_subplot(222)
    bins=np.arange(0.5,200.5,1)

    # plot average spikes for beaconed and non beaconed - normalised by time
    sd_time_normalised_bin_locations = np.nanstd(time_normalised_bin_locations,axis=1)/math.sqrt(len(spikes_on_trials))
    sd_time_normalised_bin_locations_nb = np.nanstd(time_normalised_bin_locations_nb,axis=1)/math.sqrt(len(spikes_on_trials))
    time_normalised_bin_locations = np.nanmean(time_normalised_bin_locations,axis=1)
    time_normalised_bin_locations_nb = np.nanmean(time_normalised_bin_locations_nb,axis=1)

    ax.plot(bins,time_normalised_bin_locations, c='k', linewidth = 2)
    ax.fill_between(bins,time_normalised_bin_locations-sd_time_normalised_bin_locations,time_normalised_bin_locations+sd_time_normalised_bin_locations, facecolor = 'k', alpha = 0.3)
    ax.plot(bins,time_normalised_bin_locations_nb, c='b', linewidth = 2)
    ax.fill_between(bins,time_normalised_bin_locations_nb-sd_time_normalised_bin_locations_nb,time_normalised_bin_locations_nb+sd_time_normalised_bin_locations_nb, facecolor = 'b', alpha = 0.3)

    plt.xlim(0, 200)
    #plt.ylim(0,np.max(time_normalised_bin_locations)+.01)
    plt.ylim(0)
    plt.xlabel('Location (cm)', fontsize=20, labelpad = 20)
    plt.ylabel('Average spikes / time (ms)', fontsize=20, labelpad = 20)
    ax.axvspan(88, 88+22, facecolor='DarkGreen', alpha=.2, linewidth =0)
    ax.axvspan(0, 30, facecolor='k', linewidth =0, alpha=.2) # black box
    ax.axvspan(200-30, 200, facecolor='k', linewidth =0, alpha=.2)# black box
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6,labelsize =20)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6, labelsize =20)
    ax.axvline(0, linewidth = 3, color = 'black') # bold line on the y axis
    ax.axhline(0, linewidth = 3, color = 'black') # bold line on the x axis
    ax.locator_params(axis = 'x', nbins=3) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=4) # set number of ticks on y axis
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticklabels(['0', '100', '200'])


    ax = fig.add_subplot(223)
    ax.plot(inverval_locations, c='k', linewidth = 2)
    #ax.fill_between(bins,time_normalised_bin_locations-sd_time_normalised_bin_locations,time_normalised_bin_locations+sd_time_normalised_bin_locations, facecolor = 'k', alpha = 0.3)

    plt.xlim(0, 20)
    #plt.ylim(0,np.max(time_normalised_bin_locations)+.01)
    plt.ylim(0)
    plt.xlabel('Interval (cm)', fontsize=20, labelpad = 20)
    plt.ylabel('Proportion', fontsize=20, labelpad = 20)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6,labelsize =20)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6, labelsize =20)
    ax.axvline(0, linewidth = 3, color = 'black') # bold line on the y axis
    ax.axhline(0, linewidth = 3, color = 'black') # bold line on the x axis
    ax.locator_params(axis = 'x', nbins=3) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=4) # set number of ticks on y axis
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticklabels(['0', '100', '200'])

    ax = fig.add_subplot(224)
    ax.plot(p_values, c='k', linewidth = 2)
    #ax.fill_between(bins,time_normalised_bin_locations-sd_time_normalised_bin_locations,time_normalised_bin_locations+sd_time_normalised_bin_locations, facecolor = 'k', alpha = 0.3)

    plt.xlim(0, 20)
    #plt.ylim(0,np.max(time_normalised_bin_locations)+.01)
    plt.ylim(0)
    plt.xlabel('Location (cm)', fontsize=20, labelpad = 20)
    plt.ylabel('p value', fontsize=20, labelpad = 20)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6,labelsize =20)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6, labelsize =20)
    ax.axvline(0, linewidth = 3, color = 'black') # bold line on the y axis
    ax.axhline(0, linewidth = 3, color = 'black') # bold line on the x axis
    ax.locator_params(axis = 'x', nbins=3) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=4) # set number of ticks on y axis
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticklabels(['0', '100', '200'])

    plt.subplots_adjust(hspace = .45, wspace = .5,  bottom = 0.1, left = 0.12, right = 0.95, top = 0.87)
    plt.savefig(prm.get_behaviour_analysis_path() + '/spikes_on_Track/VR_SpikePlots_Cluster_' + str(channelcount) + '.png')

    plt.close()




def plot_spikes(prm, firing_times_unit, channelcount, times):
    plt.gcf().clear()

    #get spikes on trials
    spikes_on_trials, all_spikes = get_spikes_on_trials(prm, firing_times_unit)
    stops_on_trials = get_stops_on_trials(prm)

    # make histograms of average spike vs location
    bin_locations, bin_locations_nb = spike_histogram(spikes_on_trials)
    time_bin_locations = time_normalised_spike_histogram(bin_locations, times)
    time_bin_locations_nb = time_normalised_spike_histogram(bin_locations_nb, times)

    # analyse spike interval
    interval_list = get_spike_interval(prm, spikes_on_trials)
    inverval_locations = distribution_of_intervals(interval_list)

    #shuffled data
    shuffle_spikes = shuffle_stops(spikes_on_trials)
    shuffled,real = shuffled_vs_real_histogram(prm, spikes_on_trials, shuffle_spikes, times, bin_locations)
    p_values = calculate_p_value(shuffled,real)

    spikes_on_trials, all_spikes = get_spikes_on_trials(prm, firing_times_unit)

    make_plot(prm, spikes_on_trials, channelcount,stops_on_trials, time_bin_locations, time_bin_locations_nb, inverval_locations, p_values)

    return stops_on_trials

