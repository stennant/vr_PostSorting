
import vr_file_utility
import vr_open_ephys_IO
import os
import matplotlib.pylab as plt
import numpy as np
import vr_filter
import vr_plot_utility
import vr_optogenetics

def load_continuous_data(prm, channel):
    vr_file_utility.create_folder_structure(prm)
    channel_data_all = []

    file_path = prm.get_filepath() + '100_CH' + str(channel) + '.continuous' #todo this should bw in params, it is 100 for me, 105 for Tizzy (I don't have _0)
    channel_data = vr_open_ephys_IO.get_data_continuous(prm, file_path)
    channel_data_all.append(channel_data)
    channel_data_all = np.asarray(channel_data_all)

    return channel_data_all[:,:]



def plot_continuous_data(prm, channel_data_all, channel):
    start_time = 0 # in ms
    end_time = (np.array((100,500,1000,5000)))+ start_time # in ms
    for t, times in enumerate(end_time):
        end_time = times
        #plot continuous data
        fig = plt.figure(figsize = (14,8))
        ax = fig.add_subplot(111)
        ax.plot(np.arange(start_time,end_time,(1/30)),channel_data_all[0,(start_time*30):(end_time*30)])

        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
        ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis
        ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
        ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)

        vr_plot_utility.adjust_spines(ax, ['left','bottom'])
        vr_plot_utility.adjust_spine_thickness(ax)
        plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.15, right = 0.92, top = 0.92)

        fig.savefig(prm.get_filepath() + 'Electrophysiology/continuous/raw/CH' + str(channel) + '_' + str(end_time) + 'ms.png', dpi=200)
        plt.close()


def plot_continuous_filtered_data(prm, channel_data_all, channel):
    start_time = 0 # in ms
    end_time = (np.array((25,50,100,500,1000,5000)))+ start_time # in ms
    for t, times in enumerate(end_time):
        end_time = times
        #plot continuous data
        fig = plt.figure(figsize = (14,8))
        ax = fig.add_subplot(111)
        ax.plot(np.arange(start_time,end_time,(1/30)),channel_data_all[0,(start_time*30):(end_time*30)])

        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
        ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis
        ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
        ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)

        vr_plot_utility.adjust_spines(ax, ['left','bottom'])
        vr_plot_utility.adjust_spine_thickness(ax)
        plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.15, right = 0.92, top = 0.92)

        fig.savefig(prm.get_filepath() + 'Electrophysiology/continuous/raw/CH' + str(channel) + '_' + str(end_time) + 'ms_filtered.png', dpi=200)
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

    return referenced_data_all # just first 3 seconds



def reference_channel(channel_data_all, referenced_data_all):
    referenced = []
    for p, point in enumerate(channel_data_all[0,:]):
        referenced_value = channel_data_all[0,p] - referenced_data_all[0,p]
        referenced = np.append(referenced,referenced_value)
    referenced = np.asarray(referenced)
    return referenced



def plot_referenced_data(prm, channel_data_all, channel):
    start_time = 0 # in ms
    end_time = (np.array((25,50,100,500,1000)))+ start_time # in ms
    for t, times in enumerate(end_time):
        end_time = times
        #plot continuous data
        fig = plt.figure(figsize = (14,8))
        ax = fig.add_subplot(111)
        ax.plot(np.arange(start_time,end_time,(1/30)),channel_data_all[(start_time*30):(end_time*30)])

        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
        ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis
        ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
        ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)

        vr_plot_utility.adjust_spines(ax, ['left','bottom'])
        vr_plot_utility.adjust_spine_thickness(ax)
        plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.15, right = 0.92, top = 0.92)

        fig.savefig(prm.get_filepath() + 'Electrophysiology/continuous/referenced/CH' + str(channel) + '_' + str(end_time) + 'ms.png', dpi=200)
        plt.close()




def plot_referenced_filtered_data(prm, channel_data_all, channel):
    start_time = 0 # in ms
    end_time = (np.array((25,50,100,500,1000)))+ start_time # in ms
    for t, times in enumerate(end_time):
        end_time = times
        #plot continuous data
        fig = plt.figure(figsize = (14,8))
        ax = fig.add_subplot(111)
        ax.plot(np.arange(start_time,end_time,(1/30)),channel_data_all[(start_time*30):(end_time*30)])

        ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
        ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
        ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
        ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis
        ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
        ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)

        vr_plot_utility.adjust_spines(ax, ['left','bottom'])
        vr_plot_utility.adjust_spine_thickness(ax)
        plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.15, right = 0.92, top = 0.92)

        fig.savefig(prm.get_filepath() + 'Electrophysiology/continuous/referenced/CH' + str(channel) + '_' + str(end_time) + 'ms_filtered.png', dpi=200)
        plt.close()




def load_and_plot_continuous_raw(prm):

    for c, channel in enumerate(np.arange(1,16,1)):

        #load continuous data
        channel_data_all = load_continuous_data(prm, channel)
        #plot
        plot_continuous_data(prm, channel_data_all, channel)
        #filter
        filtered_data_all = vr_filter.custom_filter(channel_data_all, 300, 6000, 30000, color='k')
        #plot filtered data
        plot_continuous_filtered_data(prm, filtered_data_all, channel)
        #print('continuous raw data analysed and plotted')


def load_and_plot_continuous_referenced(prm):

    for c, channel in enumerate(np.arange(1,16,1)):

        #load continuous data
        channel_data_all = load_continuous_data(prm, channel)
        #load reference channel
        referenced_data_all = load_reference_channel(prm, channel)
        #reference the channel
        channel_data_all = reference_channel(channel_data_all[:,0:150000], referenced_data_all)
        #plot referenced data
        plot_referenced_data(prm, channel_data_all, channel)
        #filter referenced data
        filtered_data_all = vr_filter.custom_filter(channel_data_all, 600, 6000, 30000, color='k')
        #plot filtered referenced data
        plot_referenced_filtered_data(prm, filtered_data_all, channel)
        #print('continuous referenced data analysed and plotted')





def plot_continuous_opto(prm, channel_data_all,channel, light,nolight,theta, gamma,channel_data_all_spikes):

    light_ch,no_light_ch = vr_optogenetics.split_light_and_no_light_channel(prm, channel_data_all, channel, light,nolight,theta, gamma,channel_data_all_spikes)

    light = np.hstack((light,light_ch))
    #light = np.take((light, np.where(light[:,4] > 0.7)))
    nolight = np.hstack((nolight,no_light_ch))
    #nolight = np.take((nolight, np.where(nolight[:,4] > 0.7)))

    #plot

    vr_optogenetics.plot_continuous_opto_data(prm, light, channel, 1,)
    vr_optogenetics.plot_continuous_opto_data(prm, nolight, channel, 2)
    #plot filtered data
    #plot_continuous_filtered_data(prm, channel_data_all, channel)
    #print('continuous raw data analysed and plotted')

