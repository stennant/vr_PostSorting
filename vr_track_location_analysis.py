
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



def plot_continuous_trials(prm, data, channel):

    print('plotting continuous data per trial...')

    trials = np.unique(data[:,0]) # find unique trial numbers

    for tcount, trial in enumerate(trials[:10]):
        array = data[data[:,0] == trial,:]
        start_time = 0 # in ms
        totaltime = int((array.shape[0])/30)
        end_time = totaltime + start_time # in ms

        try:

            fig = plt.figure(figsize = (14,8))

            # spikes
            ax = fig.add_subplot(411)
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),2])
            ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
            array_min = np.min(array[(start_time*30):(end_time*30),2])
            ax.set_ylim(array_min-10,)
            vr_plot_utility.adjust_spines(ax, ['left'])
            vr_plot_utility.plot_basics(prm,ax)
            vr_plot_utility.adjust_spine_thickness(ax)

            # LFP
            ax = fig.add_subplot(412)
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),3])
            ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
            ax.set_ylim(-200,200)
            vr_plot_utility.adjust_spines(ax, ['left'])
            vr_plot_utility.plot_basics(prm,ax)
            vr_plot_utility.adjust_spine_thickness(ax)

            # theta & gamma
            ax = fig.add_subplot(413)
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),4])
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),5])
            ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
            ax.set_ylim(-270,270)
            vr_plot_utility.adjust_spines(ax, ['left'])
            vr_plot_utility.plot_basics(prm,ax)
            vr_plot_utility.adjust_spine_thickness(ax)

            # location
            ax = fig.add_subplot(414)
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),1])
            ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
            ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
            ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
            ax.set_ylabel('Location (cm)', fontsize=18, labelpad = 20)
            vr_plot_utility.adjust_spines(ax, ['left','bottom'])
            vr_plot_utility.plot_basics(prm,ax)
            vr_plot_utility.adjust_spine_thickness(ax)

            plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.1, right = 0.92, top = 0.92)

            fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_Trial' + str(tcount+1) + '.png', dpi=200)
            plt.close()

        except ValueError:
                continue

        tcount+=1


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

def find_before_and_after_stops(prm,data):

    moving = False
    before_stop = np.zeros((0,7))
    after_stop = np.zeros((0,7))
    for rowcount,row in enumerate(data):
        if(data[rowcount, 6]<=0.7 and moving): # if speed is below threshold
            moving = False
            after_stop = np.vstack((after_stop, data[rowcount:rowcount+7500,:])) # location, (beaconed/non-beaconed/probe), trialid, reward(YES/NO)

        if(data[rowcount, 6]>4 and not moving):
            moving = True
            before_stop = np.vstack((before_stop, data[rowcount:rowcount+7500,:])) # location, (beaconed/non-beaconed/probe), trialid, reward(YES/NO)

    print('Extracted 250 ms before and after stops')

    return before_stop, after_stop


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


def split_locations(prm,data):

    #split data based on location along the track
    outbound = data[np.where(np.logical_and(data[:,1] > 70, data[:,1] < 90))]
    rewardzone = data[np.where(np.logical_and(data[:,1] > 90, data[:,1] < 110))]
    homebound = data[np.where(np.logical_and(data[:,1] > 110, data[:,1] < 130))]

    print('location split')

    return outbound,rewardzone, homebound


def split_speed(prm,data):
    speed = data[:,6]
    speed_median = np.percentile(speed, 50)
    speed_75 = np.percentile(speed, 75)
    speed_25 = np.percentile(speed, 25)

    #split data based on location along the track
    middle_upper = data[np.where(np.logical_and(data[:,6] > speed_median, data[:,6] < speed_75))]
    upper = data[np.where(data[:,6] > speed_75)]
    middle_lower = data[np.where(np.logical_and(data[:,6] < speed_median, data[:,6] > speed_25))]
    lower = data[np.where(data[:,6] < speed_25)]

    print('speed split')

    return middle_upper,upper, middle_lower, lower



def split_locations_speed(prm,middle_upper,upper, middle_lower, lower):

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



def plot_power_spectrum_before_after_stop(prm, before_stop, after_stop, channel):
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

    print('Plotting and saving power spectra')

    # beforestop
    fig = plt.figure(figsize = (10,6)) # figsize = (width, height)
    ax = fig.add_subplot(121)
    ax.set_title('Before stop (moving)', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,50)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    # afterstop
    ax = fig.add_subplot(122)
    ax.set_title('After stop (stationary)', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,50)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop[:7500], 30000)
    plt.subplots_adjust(hspace = .35, wspace = .5,  bottom = 0.2, left = 0.2, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_before_after_stop.png', dpi=200)
    plt.close()





def stop_start_power_spectra(prm,before_stop, after_stop, channel):

    before_stop = add_theta_and_gamma_signal(prm, before_stop, before_stop)
    after_stop = add_theta_and_gamma_signal(prm, after_stop, after_stop)

    plot_power_spectrum_before_after_stop(prm, before_stop, after_stop,  channel)





def plot_power_spectrum_track_locations(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel):


    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (12,12)) # figsize = (width, height)

    ax = fig.add_subplot(321)
    ax.set_title('After stop (stationary) \n 70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_outbound[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(323)
    ax.set_title('Reward zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_rewardzone[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    # reward zone
    ax = fig.add_subplot(325)
    ax.set_title('110-130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_homebound[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)


    ax = fig.add_subplot(322)
    ax.set_title('Before stop (moving) \n 70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_outbound[:7500], 30000)

    # homebound
    ax = fig.add_subplot(324)
    ax.set_title('Reward zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_rewardzone[:7500], 30000)

    ax = fig.add_subplot(326)
    ax.set_title('110-130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_homebound[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.1, left = 0.1, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_locations.png', dpi=200)
    plt.close()





def plot_power_spectrum_track_locations_gamma(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel):


    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (12,12)) # figsize = (width, height)

    ax = fig.add_subplot(321)
    ax.set_title('After stop (stationary) \n 70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_outbound[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(323)
    ax.set_title('Reward zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_rewardzone[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    # reward zone
    ax = fig.add_subplot(325)
    ax.set_title('110-130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_homebound[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)


    ax = fig.add_subplot(322)
    ax.set_title('Before stop (moving) \n 70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_outbound[:7500], 30000)

    # homebound
    ax = fig.add_subplot(324)
    ax.set_title('Reward zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_rewardzone[:7500], 30000)

    ax = fig.add_subplot(326)
    ax.set_title('110-130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_homebound[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.1, left = 0.1, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_locations_gamma.png', dpi=200)
    plt.close()


def stop_start_power_spectra_locations(prm,before_stop, after_stop, channel):

    #split data by track location
    before_stop_outbound, before_stop_rewardzone, before_stop_homebound = split_locations(prm, before_stop)
    after_stop_outbound, after_stop_rewardzone, after_stop_homebound = split_locations(prm, after_stop)

    # power spectra for just gamma activity
    plot_power_spectrum_track_locations_gamma(prm, after_stop_outbound[:,5], after_stop_rewardzone[:,5], after_stop_homebound[:,5], before_stop_outbound[:,5], before_stop_rewardzone[:,5],  before_stop_homebound[:,5], channel)

    # add theta and gamma signal
    before_stop_outbound = add_theta_and_gamma_signal(prm, before_stop_outbound, before_stop_outbound)
    before_stop_rewardzone = add_theta_and_gamma_signal(prm, before_stop_rewardzone, before_stop_rewardzone)
    before_stop_homebound = add_theta_and_gamma_signal(prm, before_stop_homebound, before_stop_homebound)
    after_stop_outbound = add_theta_and_gamma_signal(prm, after_stop_outbound, after_stop_outbound)
    after_stop_rewardzone = add_theta_and_gamma_signal(prm, after_stop_rewardzone, after_stop_rewardzone)
    after_stop_homebound = add_theta_and_gamma_signal(prm, after_stop_homebound, after_stop_homebound)

    #power spectra for theta and gamma
    plot_power_spectrum_track_locations(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel)




def power_spectra_speed(prm,data, channel):
    # split data based on speed
    middle_upper,upper, middle_lower, lower = split_speed(prm, data)

    #power spectra for just gamma signal
    plot_power_spectrum_speed_gamma(prm, middle_upper[:,5],upper[:,5], middle_lower[:,5], lower[:,5], channel)

    # add theta and gamma signal
    m_upper = add_theta_and_gamma_signal(prm, middle_upper, middle_upper)
    u = add_theta_and_gamma_signal(prm, upper, upper)
    m_lower = add_theta_and_gamma_signal(prm, middle_lower, middle_lower)
    l = add_theta_and_gamma_signal(prm, lower, lower)

    # power spectra for theta and gamma signal
    plot_power_spectrum_speed(prm, m_upper,u, m_lower, l, channel)

    return middle_upper,upper, middle_lower, lower


def plot_power_spectrum_speed(prm, middle_upper,upper, middle_lower, lower, channel):


    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (12,12)) # figsize = (width, height)

    ax = fig.add_subplot(221)
    ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, middle_upper[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(222)
    ax.set_title('upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, upper[:7500], 30000)


    # reward zone
    ax = fig.add_subplot(223)
    ax.set_title('middle_lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, middle_lower[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(224)
    ax.set_title('lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, lower[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.1, left = 0.1, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_speed.png', dpi=200)
    plt.close()



def plot_power_spectrum_speed_gamma(prm, middle_upper,upper, middle_lower, lower, channel):


    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (12,12)) # figsize = (width, height)

    ax = fig.add_subplot(221)
    ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, middle_upper[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(222)
    ax.set_title('upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, upper[:7500], 30000)


    # reward zone
    ax = fig.add_subplot(223)
    ax.set_title('middle_lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, middle_lower[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(224)
    ax.set_title('lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, lower[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.1, left = 0.1, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_speed_gamma.png', dpi=200)
    plt.close()



def plot_power_spectrum_speed_locations_gamma(prm, outbound_m_upper,outbound_upper,outbound_m_lower,outbound_lower,rz_m_upper,rz_upper,rz_m_lower,rz_lower,hb_m_upper,hb_upper,hb_m_lower,hb_lower, channel):


    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (12,12)) # figsize = (width, height)

    ax = fig.add_subplot(434)
    ax.set_title('Middle upper quartile \n 70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, outbound_m_upper[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(431)
    ax.set_title('Upper quartile \n 70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, outbound_upper[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    # reward zone
    ax = fig.add_subplot(437)
    ax.set_title('outbound_m_lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, outbound_m_lower[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(4,3,10)
    ax.set_title('outbound_lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, outbound_lower[:7500], 30000)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18)
    ax.set_xlabel('Frequency (Hz)', fontsize = 1, labelpad = 108)

    ax = fig.add_subplot(435)
    ax.set_title('rz_m_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, rz_m_upper[:7500], 30000)

    ax = fig.add_subplot(432)
    ax.set_title('rz_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, rz_upper[:7500], 30000)

    # reward zone
    ax = fig.add_subplot(438)
    ax.set_title('rz_m_lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, rz_m_lower[:7500], 30000)

    ax = fig.add_subplot(4,3,11)
    ax.set_title('rz_lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, rz_lower[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 1, labelpad = 108)

    ax = fig.add_subplot(436)
    ax.set_title('hb_m_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hb_m_upper[:7500], 30000)

    ax = fig.add_subplot(4,3,3)
    ax.set_title('hb_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hb_upper[:7500], 30000)

    # reward zone
    ax = fig.add_subplot(4,3,9)
    ax.set_title('hb_m_lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hb_m_lower[:7500], 30000)

    ax = fig.add_subplot(4,3,12)
    ax.set_title('hb_lower', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hb_lower[:7500], 30000)
    ax.set_xlabel('Frequency (Hz)', fontsize = 1, labelpad = 108)
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.1, left = 0.1, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_speed_gamma_locations.png', dpi=200)
    plt.close()


def power_spectra_speed_locations(prm,middle_upper,upper, middle_lower, lower, channel):
    # split data based on speed
    outbound_m_upper,outbound_upper,outbound_m_lower,outbound_lower,rz_m_upper,rz_upper,rz_m_lower,rz_lower,hb_m_upper,hb_upper,hb_m_lower,hb_lower = split_locations_speed(prm, middle_upper,upper, middle_lower, lower)

    #power spectra for just gamma signal
    plot_power_spectrum_speed_locations_gamma(prm, outbound_m_upper[:,5],outbound_upper[:,5],outbound_m_lower[:,5],outbound_lower[:,5],rz_m_upper[:,5],rz_upper[:,5],rz_m_lower[:,5],rz_lower[:,5],hb_m_upper[:,5],hb_upper[:,5],hb_m_lower[:,5],hb_lower[:,5], channel)

    # add theta and gamma signal
    #middle_upper = add_theta_and_gamma_signal(prm, middle_upper, middle_upper)
    #upper = add_theta_and_gamma_signal(prm, upper, upper)
    #middle_lower = add_theta_and_gamma_signal(prm, middle_lower, middle_lower)
    #lower = add_theta_and_gamma_signal(prm, lower, lower)

    # power spectra for theta and gamma signal
    #plot_power_spectrum_speed(prm, middle_upper,upper, middle_lower, lower, channel)


def make_stop_start_continuous_plot(prm, channel, before_stop, after_stop):

    print('plotting continuous data...')

    start_time = 0 # in ms
    end_time = 250 # 250 ms

    fig = plt.figure(figsize = (12,10)) # figsize = (width, height)
    plot_graph(before_stop, start_time,end_time, fig)
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + 'ms_beforestop.png', dpi=200)
    plt.close()

    fig = plt.figure(figsize = (12,10)) # figsize = (width, height)
    plot_graph(after_stop, start_time,end_time, fig)
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + 'ms_afterstop.png', dpi=200)
    plt.close()


def plot_graph(array, start_time,end_time, fig):

    # spikes
    ax = fig.add_subplot(411)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),2])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),2])
    ax.set_ylim(array_min-10,)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # LFP
    ax = fig.add_subplot(412)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),3])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-200,200)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # theta & gamma
    ax = fig.add_subplot(413)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),4])
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),5])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-270,270)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # location
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

    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.1, right = 0.92, top = 0.92)


def stop_start_continuous_plot(prm,before_stop, after_stop, channel):
        make_stop_start_continuous_plot(prm, channel, before_stop, after_stop)

"""""
def plot_graph(array, start_time,end_time, fig):

    # spikes
    ax = fig.add_subplot(411)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),2])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),2])
    ax.set_ylim(array_min-10,)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # LFP
    ax = fig.add_subplot(412)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),3])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-200,200)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # theta & gamma
    ax = fig.add_subplot(413)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),4])
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),5])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-270,270)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # location
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

    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.1, right = 0.92, top = 0.92)




def plot_track_locations_examples(prm, location, channel, data='data'):

    print('plotting continuous data...')

    #data = data[data[:,1] > 3,:] # remove all data in black box
    trials = np.unique(data[:,0])

    for tcount, trial in enumerate(trials[10:20]): # only plot first 10 trials
        array = data[data[:,0] == trial,:]
        start_time = 0 # in ms
        totaltime = int((array.shape[0])/30)
        try:
            end_times = (np.array((1000,totaltime))) + start_time # in ms
            for t, times in enumerate(end_times):
                end_time = times

                if location ==0:

                    fig = plt.figure(figsize = (12,10)) # figsize = (width, height)
                    plot_graph(array, start_time,end_time, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_outbound.png', dpi=200)
                    plt.close()

                if location ==1:

                    fig = plt.figure(figsize = (8,10)) # figsize = (width, height)
                    plot_graph(array, start_time,end_time, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_rewardzone.png', dpi=200)
                    plt.close()

                if location ==2:

                    fig = plt.figure(figsize = (12,10)) # figsize = (width, height)
                    plot_graph(array, start_time,end_time, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_homebound.png', dpi=200)
                    plt.close()


        except ValueError:
            continue






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

    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, outbound, 30000)
    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.2, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_outbound.png', dpi=200)
    plt.close()

    # reward zone
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, rewardzone, 30000)
    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.2, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_rewardzone.png', dpi=200)
    plt.close()


    # homebound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, homebound, 30000)
    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.2, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_homebound.png', dpi=200)
    plt.close()



def add_theta_and_gamma_signal(prm,outbound, rewardzone, homebound):
    outbound = outbound[:,4] + outbound[:,5]
    homebound = homebound[:,4] + homebound[:,5]
    rewardzone = rewardzone[:,4] + rewardzone[:,5]

    return outbound, rewardzone, homebound



def calculate_and_plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound, channel):

    # calculate and plot power spectrum
    outbound, rewardzone, homebound = add_theta_and_gamma_signal(prm,outbound, rewardzone, homebound)
    plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound,  channel)

"""""
