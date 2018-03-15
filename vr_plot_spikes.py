import itertools
import matplotlib.pylab as plt
import numpy as np
import os
import vr_parameters
import vr_stops


def get_spikes_on_trials(prm, firing_times_unit):
    #spiketimes = stops.get_spike_times(prm)
    location, number_of_trials, all_stops, track_beginnings = vr_stops.get_data_for_spikes_on_trials(prm, firing_times_unit)
    stops_on_trials = vr_stops.get_spikes_on_trials_find_stops(location, number_of_trials, all_stops, track_beginnings)
    return stops_on_trials


def make_plot(prm, stops_on_trials, channelcount):
    #plot_utility.draw_reward_zone()
    #plot_utility.draw_black_boxes()
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




def plot_spikes(prm, firing_times_unit, channelcount):
    plt.gcf().clear()
    stops_on_trials = get_spikes_on_trials(prm, firing_times_unit)
    make_plot(prm, stops_on_trials, channelcount)

    return stops_on_trials




def main():
    prm = parameters.Parameters()
    analysis_path = '/Users/sarahtennant/Work/Analysis/Opto/Spikes/Test_for_Klara/recordings/2017-12-05_14-32-19/Behaviour/Analysis'
    location = np.load('/Users/sarahtennant/Work/Analysis/Opto/Spikes/Test_for_Klara/recordings/2017-12-05_14-32-19/Behaviour/Data/location.npy')
    first_stops = np.load('/Users/sarahtennant/Work/Analysis/Opto/Spikes/Test_for_Klara/recordings/2017-12-05_14-32-19/Behaviour/Data/first_stops.npy')

    prm.set_behaviour_data_path('/Users/sarahtennant/Work/Analysis/Opto/Spikes/Test_for_Klara/recordings/2017-12-05_14-32-19/Behaviour/Behaviour/Data/')
    prm.set_behaviour_analysis_path('/Users/sarahtennant/Work/Analysis/Opto/Spikes/Test_for_Klara/recordings/2017-12-05_14-32-19/Behaviour/Analysis')

    #plot_first_stops(prm, first_stops, location)

    plot_spikes(prm)


if __name__ == '__main__':
    main()
