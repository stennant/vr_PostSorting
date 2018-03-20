
import vr_file_utility
import vr_open_ephys_IO
import os
import matplotlib.pylab as plt
import numpy as np
import vr_filter
import vr_plot_utility
import vr_process_movement
import vr_plot_continuous_data
import vr_fft
import gc


def load_opto_continuous_data(prm, channel):

    print('loading opto channel...')
    vr_file_utility.create_folder_structure(prm)
    channel_data_all = []

    file_path = prm.get_filepath() + '/' + str(channel) #todo this should bw in params, it is 100 for me, 105 for Tizzy (I don't have _0)
    channel_data = vr_open_ephys_IO.get_data_continuous(prm, file_path)
    channel_data_all.append(channel_data)
    channel_data_all = np.asarray(channel_data_all)

    return channel_data_all[0,:]



def load_and_save_opto_channel(prm):

    if os.path.isfile(prm.get_filepath() + "Behaviour/Data/optogenetics.npy") is False:

        channel = prm.get_opto_ch()

        #load continuous data
        opto_channel = load_opto_continuous_data(prm, channel)
        opto_channel_all = vr_process_movement.remove_beginning_and_end(prm,opto_channel)
        np.save(prm.get_filepath() + "Behaviour/Data/optogenetics", opto_channel_all)
        plt.plot(opto_channel_all)
        plt.show()
    else:
        opto_channel_all = np.load(prm.get_filepath() + "Behaviour/Data/optogenetics.npy")

    return opto_channel_all



def split_light_and_no_light_trials(prm):
    global trial_num

    if os.path.isfile(prm.get_filepath() + "Behaviour/Data/light.npy") is False:

        opto_channel = np.load(prm.get_filepath() + "Behaviour/Data/optogenetics.npy")
        trial_channel = np.load(prm.get_filepath() + "Behaviour/Data/trial_numbers.npy")
        trial_type_channel = np.load(prm.get_filepath() + "Behaviour/Data/con_trial_type.npy")
        location = np.load(prm.get_filepath() + "Behaviour/Data/location.npy")
        speed = np.load(prm.get_filepath() + "Behaviour/Data/speed.npy")

        x = np.vstack((opto_channel,trial_channel,trial_type_channel,location, speed))
        x = np.transpose(x)
        # [0 = opto channel, 1 = trial numbers, 2 = trial types, 3 = location, 4 = speed]

        light = np.zeros((0,5))
        no_light = np.zeros((0,5))

        print('splitting stimulation and non-stimulation trials...')

        for t, trial in enumerate(np.unique(trial_channel)):
            trial_data = x[x[:,1] == trial,:]
            trial_sorted = 0
            for p,point in enumerate(trial_data[:,0]):
                if point > 0.5:
                    light = np.vstack((light,trial_data))
                    trial_sorted = 1
                    break
            if trial_sorted ==0:
                no_light = np.vstack((no_light,trial_data))


        print('trials split')
        np.save(prm.get_filepath() + "Behaviour/Data/light", light)
        np.save(prm.get_filepath() + "Behaviour/Data/nolight", no_light)
        np.save(prm.get_filepath() + "Behaviour/Data/trials_light", light[:,1])
        np.save(prm.get_filepath() + "Behaviour/Data/trials_nolight", no_light[:,1])

    else:
        light = np.load(prm.get_filepath() + "Behaviour/Data/light.npy")
        no_light = np.load(prm.get_filepath() + "Behaviour/Data/nolight.npy")

    return light, no_light



def split_light_and_no_light_channel(prm, channel_all_data, channel):

    if os.path.isfile(prm.get_filepath() + "Behaviour/Data/CH" + str(channel) + "_light.npy") is False:

        trials = np.load(prm.get_filepath() + "Behaviour/Data/trial_numbers.npy")
        light = np.load(prm.get_filepath() + "Behaviour/Data/light.npy")
        no_light = np.load(prm.get_filepath() + "Behaviour/Data/nolight.npy")
        light_trials = np.unique(light[:,1])
        no_light_trials = np.unique(no_light[:,1])

        channel_all_data = vr_process_movement.remove_beginning_and_end(prm,channel_all_data[:,0])

        x = np.vstack((channel_all_data, trials))
        x = np.transpose(x)

        light = np.zeros((0,2))
        no_light = np.zeros((0,2))

        print('splitting stimulation and non-stimulation trials...')

        for t, trial in enumerate(light_trials):
            trial_data = x[x[:,1] == trial,:]
            light = np.vstack((light,trial_data))
        np.save(prm.get_filepath() + "Behaviour/Data/CH" + str(channel) + "_light", light)

        for t, trial in enumerate(no_light_trials):
            trial_data = x[x[:,1] == trial,:]
            no_light = np.vstack((no_light,trial_data))
        np.save(prm.get_filepath() + "Behaviour/Data/CH" + str(channel) + "_nolight", no_light)

    else:
        light = np.load(prm.get_filepath() + "Behaviour/Data/CH" + str(channel) + "_light.npy")
        no_light = np.load(prm.get_filepath() + "Behaviour/Data/CH" + str(channel) + "_nolight.npy")

    print('stimulation and non-stimulation trials are split')

    return light, no_light




def plot_continuous_opto_data(prm, data, channel, param):

    print('plotting continuous data...')

    data = data[data[:,3] > 3,:] # remove all data in black box
    trials = np.unique(data[:,1])

    for tcount, trial in enumerate(trials):
        array = data[data[:,1] == trial,:]
        start_time = 1000 # in ms
        end_time = (np.array((25,50,100,500,1000,5000))) + start_time # in ms
        try:
            for t, times in enumerate(end_time):
                end_time = times
                #plot continuous data
                fig = plt.figure(figsize = (14,8))
                ax = fig.add_subplot(111)
                ax.plot(np.arange(start_time,end_time,(1/30)),array[(start_time*30):(end_time*30),5])

                ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
                ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
                ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
                ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis
                ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
                ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)

                vr_plot_utility.adjust_spines(ax, ['left','bottom'])
                vr_plot_utility.adjust_spine_thickness(ax)
                plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.15, right = 0.92, top = 0.92)

                if param == 1:
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/opto_stimulation/continuous/raw/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_light.png', dpi=200)
                    plt.close()
                if param == 2:
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/opto_stimulation/continuous/raw/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_nolight.png', dpi=200)
                    plt.close()
        except ValueError:
                continue




def plot_continuous_filtered_opto_data(prm, data, channel, param):

    print('plotting continuous data...')

    data = data[data[:,3] > 3,:] # remove all data in black box
    trials = np.unique(data[:,1])

    for tcount, trial in enumerate(trials):
        array = data[data[:,1] == trial,:]
        start_time = 1000 # in ms
        end_time = (np.array((25,50,100,500,1000,5000))) + start_time # in ms
        try:
            for t, times in enumerate(end_time):
                end_time = times
                #plot continuous data
                fig = plt.figure(figsize = (14,8))
                ax = fig.add_subplot(111)
                ax.plot(np.arange(start_time,end_time,(1/30)),array[(start_time*30):(end_time*30),5])

                ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
                ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
                ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
                ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis
                ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
                ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)

                vr_plot_utility.adjust_spines(ax, ['left','bottom'])
                vr_plot_utility.adjust_spine_thickness(ax)
                plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.15, right = 0.92, top = 0.92)

                if param == 1:
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/opto_stimulation/continuous/filtered/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_light.png', dpi=200)
                    plt.close()
                if param == 2:
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/opto_stimulation/continuous/filtered/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_nolight.png', dpi=200)
                    plt.close()
        except ValueError:
                continue




def plot_opto_power_spectrum(prm, channel_all_data, channel, param):

    print('Plotting and saving power spectra')

    fig, ax = plt.subplots()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    vr_fft.power_spectrum_log(prm, channel_all_data[:,5], 30000, 'k', prm.get_filename(), title="$Power spectrum$", x_lim=150, line_width=15, legend='stationary')

    if param == 1:
        fig.savefig(prm.get_filepath() + 'Electrophysiology/opto_stimulation/fft/CH' + str(channel)  +  '_light.png', dpi=200)
        plt.close()
    if param == 2:
        fig.savefig(prm.get_filepath() + 'Electrophysiology/opto_stimulation/fft/CH' + str(channel)  + '_nolight.png', dpi=200)
        plt.close()


def load_reference_channel(prm, channel):
    #load .txt that tells us which channel is used as reference for the current channel
    array = np.loadtxt(prm.get_filepath() + 'ref.txt')
    channel_reference = int(array[channel])

    #load continuous data from reference channel
    referenced_data_all = []
    reference = prm.get_filepath() + '100_CH' + str(channel_reference) + '.continuous' #todo this should bw in params, it is 100 for me, 105 for Tizzy (I don't have _0)
    referenced_data = vr_open_ephys_IO.get_data_continuous(prm, reference)
    referenced_data_all.append(referenced_data)
    referenced_data_all = np.asarray(referenced_data_all)
    referenced_data_all=np.transpose(referenced_data_all)

    return referenced_data_all # just first 3 seconds


def reference_channel(channel_data_all, referenced_data_all):
    referenced = np.zeros((referenced_data_all.shape))
    print(referenced.shape, channel_data_all.shape)
    print('referencing channel...')
    for p, point in enumerate(channel_data_all):
        referenced_value = channel_data_all[p,0] - referenced_data_all[p]
        referenced[p] = referenced_value
    referenced = np.asarray(referenced)
    referenced = np.hstack((referenced,channel_data_all))
    print('channel referenced')

    return referenced



def plot_continuous_theta_opto_data(prm, theta, gamma,channel, param):

    print('plotting continuous data...')

    theta = theta[theta[:,3] > 3,:] # remove all data in black box
    trials = np.unique(theta[:,1])

    for tcount, trial in enumerate(trials):
        theta = theta[theta[:,1] == trial,:]
        gamma = gamma[gamma[:,1] == trial,:]
        start_time = 1000 # in ms
        end_time = (np.array((25,50,100,500,1000,5000))) + start_time # in ms
        try:
            for t, times in enumerate(end_time):
                end_time = times
                #plot continuous data
                fig = plt.figure(figsize = (14,8))
                ax = fig.add_subplot(111)
                ax.plot(np.arange(start_time,end_time,(1/30)),theta[(start_time*30):(end_time*30),5])

                ax.plot(np.arange(start_time,end_time,(1/30)),gamma[(start_time*30):(end_time*30),5])

                ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
                ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
                ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
                ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis
                ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
                ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)

                vr_plot_utility.adjust_spines(ax, ['left','bottom'])
                vr_plot_utility.adjust_spine_thickness(ax)
                plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.15, right = 0.92, top = 0.92)

                if param == 1:
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/opto_stimulation/theta/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_light.png', dpi=200)
                    plt.close()
                if param == 2:
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/opto_stimulation/theta/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_nolight.png', dpi=200)
                    plt.close()
        except ValueError:
                continue


def load_and_process_opto_channel(prm):

    opto_data = load_and_save_opto_channel(prm)
    print('opto channel loaded')

    #split data according to light and no light stimulation
    light, no_light = split_light_and_no_light_trials(prm)
    print('data split by light/nolight')

    for c, channel in enumerate(np.arange(1,16,1)):

        #load continuous data
        channel_all_data = vr_plot_continuous_data.load_continuous_data(prm, channel)
        #load reference channel
        referenced_data_all = load_reference_channel(prm, channel)
        #reference the channel
        channel_all_data = reference_channel(np.transpose(channel_all_data), referenced_data_all)
        print('channel referenced')

        # split ephys according to light and no light stimulation
        #light_ch,no_light_ch = split_light_and_no_light_channel(prm, channel_all_data, channel)
        print('channel split by light/nolight')

        #plot continuous data for each light/nolight trial
        #plot_continuous_opto_data(prm, np.hstack((light,light_ch)), channel, 1)
        #plot_continuous_opto_data(prm, np.hstack((no_light,no_light_ch)), channel, 2)
        print('continuous referenced data plotted')

        #plot power spectrum for all light/nolight trials
        #plot_opto_power_spectrum(prm, np.hstack((light,light_ch)), channel,1)
        #plot_opto_power_spectrum(prm, np.hstack((no_light,no_light_ch)), channel,2)
        print('power spectra data plotted')

        #light_theta = vr_filter.theta_filter(light_ch[:,0], 30000)
        #nolight_theta = vr_filter.theta_filter(no_light_ch[:,0], 30000)
        print('channel filtered for theta')
        #light_gamma = vr_filter.gamma_filter(light_ch[:,0], 30000)
        #nolight_gamma = vr_filter.gamma_filter(no_light_ch[:,0], 30000)
        print('channel filtered for gamma')

        #ight_theta = np.column_stack((light,light_theta))
        #nolight_theta = np.column_stack((no_light,nolight_theta))
        #light_gamma = np.column_stack((light, light_gamma))
        #nolight_gamma = np.column_stack((no_light, nolight_gamma))

        #plot_continuous_theta_opto_data(prm, light_theta, light_gamma,channel, 1)
        #plot_continuous_theta_opto_data(prm, nolight_theta, nolight_gamma,channel, 2)

        #filter data
        #light_ch = vr_filter.custom_filter(light_ch[:,0], 600, 6000, 30000, color='k')
        #no_light_ch = vr_filter.custom_filter(no_light_ch[:,0], 600, 6000, 30000, color='k')

        #light_ch=np.vstack((light_ch, light_ch));light_ch=np.transpose(light_ch)
        #no_light_ch=np.vstack((no_light_ch, no_light_ch));no_light_ch=np.transpose(no_light_ch)

        #plot filtered data
        #plot_continuous_filtered_opto_data(prm, np.hstack((light,light_ch)), 6, 1)
        #plot_continuous_filtered_opto_data(prm, np.hstack((no_light,no_light_ch)), 6, 2)
        #filter for theta





