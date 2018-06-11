import itertools
import matplotlib.pylab as plt
import numpy as np
import os
import vr_parameters
import vr_stops
import vr_sorted_firing_times


def get_spikes_on_trials(prm, firing_times_unit):
    location, number_of_trials, trials, all_stops, track_beginnings = vr_stops.get_data_for_spikes_on_trials(prm, firing_times_unit)
    time = vr_sorted_firing_times.get_time_in_bin(prm, location, trials)
    stops_on_trials = vr_stops.get_spikes_on_trials_find_stops(location, number_of_trials, time, all_stops, track_beginnings)
    return stops_on_trials


def make_plot(prm, stops_on_trials, channelcount):
    avg_stop_b=[]
    avg_stop_nb=[]
    fig = plt.figure(figsize = (10,12))
    ax = fig.add_subplot(211)

    plt.xlim(0, 200)

    for ith, trial in enumerate(stops_on_trials):
        if trial.size == 0:
            continue

        if ith % 5 == 0 and ith > 0:
            color_of_stop = 'r'
            plt.plot(trial, ith, '|', markersize=3, c=color_of_stop)
            print(trial[:,1:])
            avg_stop_b=np.append(trial[:,1:], avg_stop_b)

        else:
            color_of_stop = 'k'
            plt.plot(trial, ith, '|',markersize=3, c=color_of_stop)
            avg_stop_nb=np.append(trial[:,1:], avg_stop_nb)

    plt.ylim(.5, len(stops_on_trials) + .5)
    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=18)
    plt.ylabel('Spikes\ on\ trials$', fontsize=18)
    ax.axvspan(88, 88+22, facecolor='DarkGreen', alpha=.2, linewidth =0)
    ax.axvspan(0, 30, facecolor='k', linewidth =0, alpha=.2) # black box
    ax.axvspan(200-30, 200, facecolor='k', linewidth =0, alpha=.2)# black box
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 1.5, length = 6,labelsize =18)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6, labelsize =18)
    ax.axvline(0, linewidth = 3, color = 'black') # bold line on the y axis
    ax.axhline(.4, linewidth = 3, color = 'black') # bold line on the x axis
    ax.locator_params(axis = 'x', nbins=3) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=4) # set number of ticks on y axis
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    ax = fig.add_subplot(212)
    plt.xlim(0, 20)
    bin_locations=np.zeros((20))

    for loc_count,loc in enumerate(np.arange(1,200,10)):
        stop_sum = avg_stop_b[np.where(np.logical_and(avg_stop_b < (loc+5),  avg_stop_b > (loc-5)))]
        sum = len(stop_sum)
        bin_locations[loc_count]= sum
        print(bin_locations, 'bin_locations')

    plt.ylim(0,np.max(bin_locations)+.025)
    plt.plot(bin_locations, linewidth = 2)
    plt.xlabel('Location on track (cm)', fontsize=18, labelpad = 20)
    plt.ylabel('Average stops', fontsize=18, labelpad = 20)
    ax.axvspan(8.8, 8.8+2.2, facecolor='DarkGreen', alpha=.2, linewidth =0)
    ax.axvspan(0, 3, facecolor='k', linewidth =0, alpha=.2) # black box
    ax.axvspan(20-3, 20, facecolor='k', linewidth =0, alpha=.2)# black box
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 1.5, length = 6,labelsize =18)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6, labelsize =18)
    ax.axvline(0, linewidth = 3, color = 'black') # bold line on the y axis
    ax.axhline(0, linewidth = 3, color = 'black') # bold line on the x axis
    ax.locator_params(axis = 'x', nbins=3) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=4) # set number of ticks on y axis
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticklabels(['0', '100', '200'])

    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.2, right = 0.92, top = 0.95)
    plt.savefig(prm.get_behaviour_analysis_path() + '/spikes_on_Track/spikes_on_track_hist_Cluster_' + str(channelcount) + '.png')

    plt.close()


def make_plot_hist(prm, stops_on_trials, channelcount):
    ax = plt.subplot(111)

    plt.xlim(0, 200)

    for ith, trial in enumerate(stops_on_trials):
        if trial.size == 0:
            continue

        if ith % 5 == 0 and ith > 0:
            color_of_stop = 'r'
            plt.plot(trial, ith, '|', markersize=3, c=color_of_stop)
        else:
            color_of_stop = 'k'

            plt.plot(trial, ith, '|',markersize=3, c=color_of_stop)
    plt.ylim(.5, len(stops_on_trials) + .5)
    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=18)
    plt.ylabel('Spikes\ on\ trials$', fontsize=18)
    ax.axvspan(88, 88+22, facecolor='DarkGreen', alpha=.2, linewidth =0)
    ax.axvspan(0, 30, facecolor='k', linewidth =0, alpha=.2) # black box
    ax.axvspan(200-30, 200, facecolor='k', linewidth =0, alpha=.2)# black box
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 1.5, length = 6,labelsize =18)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 6, labelsize =18)
    ax.axvline(0, linewidth = 3, color = 'black') # bold line on the y axis
    ax.axhline(.4, linewidth = 3, color = 'black') # bold line on the x axis
    ax.locator_params(axis = 'x', nbins=3) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=4) # set number of ticks on y axis
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.15, right = 0.92, top = 0.95)
    plt.savefig(prm.get_behaviour_analysis_path() + '/spikes_on_Track/spikes_on_track' + str(channelcount) + '.png')

    plt.close()



def plot_spikes(prm, firing_times_unit, channelcount, times):
    plt.gcf().clear()
    stops_on_trials = get_spikes_on_trials(prm, firing_times_unit)
    make_plot(prm, stops_on_trials, channelcount)

    return stops_on_trials

