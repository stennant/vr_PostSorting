import itertools
import matplotlib.pylab as plt
import numpy as np
import os
import vr_parameters
import plot_utility
import vr_stops


def get_stops_on_trials(prm):
    stoptimes = vr_stops.get_stop_times(prm)
    location, number_of_trials, all_stops, track_beginnings = vr_stops.get_data_for_stops_on_trials(prm)
    stops_on_trials = vr_stops.get_stops_on_trials_find_stops(location, number_of_trials, all_stops, track_beginnings)
    return stops_on_trials


def make_plot(prm, stops_on_trials):
    avg_stop_b=[]
    avg_stop_nb=[]
    fig = plt.figure(figsize = (8,12))
    ax = fig.add_subplot(211)
    plt.xlim(0, 200)

    for ith, trial in enumerate(stops_on_trials):
        if trial.size == 0:
            continue

        if ith % 5 == 0 and ith > 0:
            color_of_stop = 'r'
            plt.plot(trial, ith, 'ko', markersize=3, c=color_of_stop, markeredgewidth=0.0)
            avg_stop_b=np.append(trial, avg_stop_b)
        else:
            color_of_stop = 'k'
            plt.plot(trial, ith, 'ko', markersize=3, c=color_of_stop, markeredgewidth=0.0)
            avg_stop_nb=np.append(trial, avg_stop_nb)

    plt.ylim(.5, len(stops_on_trials) + .5)
    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=18)
    plt.ylabel('$Stops\ on\ trials$', fontsize=18)
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
        sum = len(stop_sum) / len(stops_on_trials)
        bin_locations[loc_count]= sum

    plt.ylim(0,np.max(bin_locations)+.05)
    plt.plot(bin_locations)
    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=18)
    plt.ylabel('$Average\ stops\ on\ trials$', fontsize=18)
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

    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.15, right = 0.92, top = 0.95)
    fig.savefig(prm.get_behaviour_analysis_path() + '/stops_on_Track/stops_on_track.png')

    plt.close()



def plot_stops(prm):
    plt.gcf().clear()
    stops_on_trials = get_stops_on_trials(prm)
    make_plot(prm, stops_on_trials)

    return stops_on_trials


def plot_first_stops(prm, first_stops, location):
    analysis_path = prm.get_behaviour_analysis_path()
    plt.gcf().clear()
    plot_utility.draw_reward_zone()
    plot_utility.draw_black_boxes()
    first_stops = np.asanyarray(first_stops, dtype=int)
    first_stop_locations = np.take(location, first_stops)
    weights = np.ones_like(first_stop_locations)/float(len(first_stop_locations))
    first_stop_hist = plt.subplot(111)
    first_stop_hist.hist(first_stop_locations, 20, color='r', range=[0, 200], weights=weights)
    first_stop_hist.spines['right'].set_visible(False)
    first_stop_hist.spines['top'].set_visible(False)
    first_stop_hist.yaxis.set_ticks_position('left')
    first_stop_hist.xaxis.set_ticks_position('bottom')

    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=20)
    plt.ylabel('$Frequency\ of\ first\ stops\ (histogram)$', fontsize=20)

    if os.path.exists(analysis_path) is False:
        os.makedirs(analysis_path)

    plt.savefig(analysis_path + '/first_stops.png')
    plt.close()


def plot_first_stops_location(prm, first_stop_locations):
    analysis_path = prm.get_behaviour_analysis_path()
    plt.gcf().clear()
    plot_utility.draw_reward_zone()
    plot_utility.draw_black_boxes()
    weights = np.ones_like(first_stop_locations)/float(len(first_stop_locations))
    first_stop_hist = plt.subplot(111)
    first_stop_hist.hist(first_stop_locations, 20, color='r', range=[0, 200], weights=weights)
    first_stop_hist.spines['right'].set_visible(False)
    first_stop_hist.spines['top'].set_visible(False)
    first_stop_hist.yaxis.set_ticks_position('left')
    first_stop_hist.xaxis.set_ticks_position('bottom')

    plt.xlabel('$Location\ on\ track\ (cm)$', fontsize=20)
    plt.ylabel('$Frequency\ of\ first\ stops\ (histogram)$', fontsize=20)

    if os.path.exists(analysis_path) is False:
        os.makedirs(analysis_path)

    plt.savefig(analysis_path + '/first_stops.png')
    plt.close()


def main():
    prm = vr_parameters.Parameters()
    analysis_path = '/Users/sarahtennant/Work/Analysis/Opto/Spikes/Test_for_Klara/recordings/2017-12-05_14-32-19/Behaviour/Analysis'
    location = np.load('/Users/sarahtennant/Work/Analysis/Opto/Spikes/Test_for_Klara/recordings/2017-12-05_14-32-19/Behaviour/Data/location.npy')
    first_stops = np.load('/Users/sarahtennant/Work/Analysis/Opto/Spikes/Test_for_Klara/recordings/2017-12-05_14-32-19/Behaviour/Data/first_stops.npy')

    #plot_first_stops(prm, first_stops, location)

    plot_stops(prm)


if __name__ == '__main__':
    main()
