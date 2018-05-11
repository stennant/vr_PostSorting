
import vr_file_utility
import vr_open_ephys_IO
import os
import matplotlib.pylab as plt
import numpy as np
import vr_filter
import vr_plot_utility
import vr_optogenetics
import vr_process_movement



def split_locations(prm,no_light,channel_all_data,channel_data_all_spikes,theta,gamma):
    trials = np.load(prm.get_filepath() + "Behaviour/Data/trial_numbers.npy")
    trials = np.unique(trials[:,1])
    channel_all_data = np.transpose(channel_all_data[0,:])
    channel_all_data = vr_process_movement.remove_beginning_and_end(prm,channel_all_data)
    channel_data_all_spikes = np.transpose(channel_data_all_spikes[0,:])
    channel_data_all_spikes = vr_process_movement.remove_beginning_and_end(prm,channel_data_all_spikes)
    theta = np.transpose(theta[0,:])
    theta = vr_process_movement.remove_beginning_and_end(prm,theta)
    gamma = np.transpose(gamma[0,:])
    gamma = vr_process_movement.remove_beginning_and_end(prm,gamma)

    x = np.vstack((channel_all_data, trials, channel_data_all_spikes,theta,gamma))
    x = np.transpose(x)

    return x



def plot_track_locations_examples(prm, location, channel, data='data'):


    print('plotting continuous data...')

    data = data[data[:,3] > 3,:] # remove all data in black box
    trials = np.unique(data[:,1])

    for tcount, trial in enumerate(trials[:20]):
        array = data[data[:,1] == trial,:]
        trial_type = array[1,2]
        start_time = 0 # in ms
        try:
            end_time = (np.array((100,500,1000,(np.shape(array[0]))/30))) + start_time # in ms
            for t, times in enumerate(end_time):
                end_time = times

                if location ==0:

                    fig = plt.figure(figsize = (10,12))
                    plot_graph(array, start_time,end_time, t, times, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_outbound.png', dpi=200)

                if location ==1:

                    fig = plt.figure(figsize = (6,12))
                    plot_graph(array, start_time,end_time, t, times, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_rewardzone.png', dpi=200)

                if location ==2:

                    fig = plt.figure(figsize = (10,12))
                    plot_graph(array, start_time,end_time, t, times, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_homebound.png', dpi=200)


        except ValueError:
            continue




def plot_graph(array, start_time,end_time, t, times, fig):

    ax = fig.add_subplot(511)

    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),5])
    opto_ch = (array[(start_time*30):(end_time*30),0])+(array_min-5)
    ax.set_ylim(array_min-10,array_min+10)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),opto_ch, 'k')

    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    ax = fig.add_subplot(512)

    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),5])

    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),5])
    #opto_ch = (array[(start_time*30):(end_time*30),0])+(array_min-5)
    ax.set_ylim(array_min-10,)

    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    ax = fig.add_subplot(513)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),7])

    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),6])
    ax.set_ylim(-200,200)

    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    ax = fig.add_subplot(514)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),9])
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),8])

    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),8])
    opto_ch = (array[(start_time*30):(end_time*30),0])+(array_min-5)
    ax.set_ylim(-270,270)

    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)


    ax = fig.add_subplot(515)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),3])

    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
    ax.set_ylabel('Location (cm)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),4])
    array_max = np.min(array[(start_time*30):(end_time*30),4])
    #ax.set_ylim(0,20)

    vr_plot_utility.adjust_spines(ax, ['left','bottom'])
    vr_plot_utility.adjust_spine_thickness(ax)


    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.2, right = 0.92, top = 0.92)
