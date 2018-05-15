
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


def split_locations(prm,no_light,channel_data_all,channel_data_all_spikes,theta,gamma):
    #load data
    trials = np.load(prm.get_filepath() + "Behaviour/Data/trial_numbers.npy")
    location = np.load(prm.get_filepath() + "Behaviour/Data/location.npy")

    #get all your data arrays in the same shape and order so you can stack them together
    channel_all_data = np.transpose(channel_data_all[0,:])
    channel_all_data = vr_process_movement.remove_beginning_and_end(prm,channel_all_data) # remove start of data
    channel_data_all_spikes = np.transpose(channel_data_all_spikes[0,:])
    channel_data_all_spikes = vr_process_movement.remove_beginning_and_end(prm,channel_data_all_spikes)# remove start of data
    theta = np.transpose(theta[0,:])
    theta = vr_process_movement.remove_beginning_and_end(prm,theta)# remove start of data
    gamma = np.transpose(gamma[0,:])
    gamma = vr_process_movement.remove_beginning_and_end(prm,gamma)# remove start of data

    #make an array with the data
    x = np.vstack((trials, location, channel_all_data, channel_data_all_spikes,theta,gamma))
    data = np.transpose(x)

    #split data based on location along the track
    outbound = data[np.where(np.logical_and(data[:,1] > 30, data[:,1] < 90))]
    rewardzone = data[np.where(np.logical_and(data[:,1] > 90, data[:,1] < 110))]
    homebound = data[np.where(np.logical_and(data[:,1] > 110, data[:,1] < 170))]

    print(data.shape, outbound.shape, rewardzone.shape,homebound.shape)
    return outbound,rewardzone, homebound


def plot_track_locations_examples(prm, location, channel, data='data'):


    print('plotting continuous data...')

    #data = data[data[:,1] > 3,:] # remove all data in black box
    trials = np.unique(data[:,0])

    for tcount, trial in enumerate(trials):
        array = data[data[:,0] == trial,:]
        print(array.shape)
        start_time = 0 # in ms
        totaltime = int((array.shape[0])/30)
        try:
            end_times = (np.array((100,500,1000,totaltime))) + start_time # in ms
            print(end_times, 'endtime')
            for t, times in enumerate(end_times):
                end_time = times

                if location ==0:

                    fig = plt.figure(figsize = (12,10))
                    plot_graph(array, start_time,end_time, t, times, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_outbound.png', dpi=200)
                    plt.close()

                if location ==1:

                    fig = plt.figure(figsize = (8,10))
                    plot_graph(array, start_time,end_time, t, times, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_rewardzone.png', dpi=200)
                    plt.close()

                if location ==2:

                    fig = plt.figure(figsize = (12,10))
                    plot_graph(array, start_time,end_time, t, times, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_homebound.png', dpi=200)
                    plt.close()


        except ValueError:
            continue




def plot_graph(array, start_time,end_time, t, times, fig):


    ax = fig.add_subplot(411)

    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),2])

    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),2])
    ax.set_ylim(array_min-10,)

    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    ax = fig.add_subplot(412)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),3])

    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-200,200)

    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    ax = fig.add_subplot(413)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),4])
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),5])

    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-270,270)

    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)


    ax = fig.add_subplot(414)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),1])

    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
    ax.set_ylabel('Location (cm)', fontsize=18, labelpad = 20)

    vr_plot_utility.adjust_spines(ax, ['left','bottom'])
    vr_plot_utility.adjust_spine_thickness(ax)


    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.2, right = 0.92, top = 0.92)












def plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound, channel):
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
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        vr_fft.power_spectrum_log(prm, outbound, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_outbound.png', dpi=200)
        vr_fft.power_spectrum_log2(prm, outbound, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=15, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_outbound2.png', dpi=200)
        plt.close()


        fig, ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        vr_fft.power_spectrum_log(prm, rewardzone, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_rewardzone.png', dpi=200)
        vr_fft.power_spectrum_log2(prm, rewardzone, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=15, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_rewardzone2.png', dpi=200)
        plt.close()

        fig, ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        vr_fft.power_spectrum_log(prm, homebound, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_homebound.png', dpi=200)
        vr_fft.power_spectrum_log2(prm, homebound, 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=15, line_width=15, legend='stationary')
        fig.savefig(prm.get_filepath() + 'Electrophysiology/fft/CH' + str(channel) + '_homebound2.png', dpi=200)
        plt.close()

    else:
        print('Power spectrum for movement and stationary data is already saved.')






def calculate_and_plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound, channel):

    # calculate and plot power spectrum
    #plot_power_spectrum(prm, channel_all_data[0,:], channel)
    plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound,  channel)

