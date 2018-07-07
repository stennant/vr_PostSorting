
import vr_file_utility
import vr_open_ephys_IO
import os
import matplotlib.pylab as plt
import numpy as np
import vr_filter
import vr_plot_utility


def load_continuous_data(prm, channel):
    vr_file_utility.create_folder_structure(prm)
    channel_data_all = []

    file_path = prm.get_filepath() + '100_CH' + str(channel) + '.continuous' #todo this should bw in params, it is 100 for me, 105 for Tizzy (I don't have _0)
    channel_data = vr_open_ephys_IO.get_data_continuous(prm, file_path)
    channel_data_all.append(channel_data)
    channel_data_all = np.asarray(channel_data_all)

    return channel_data_all[:,:]


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

    return referenced_data_all[:,:]



def reference_channel(channel_data_all, referenced_data_all):
    referenced = []
    for p, point in enumerate(channel_data_all[0,:]):
        referenced_value = channel_data_all[0,p] - referenced_data_all[0,p]
        referenced = np.append(referenced,referenced_value)
    referenced = np.asarray(referenced)
    return referenced



def rewrite_contiuous_channel(prm, channel,channel_data_all):

    #load continuous data from reference channel

    np.save(prm.get_filepath() + '100_CH' + str(channel) + '.continuous', channel_data_all)


def load_and_rewrite_continuous_data(prm):

    for c, channel in enumerate(np.arange(1,16,1)):

        #load continuous data
        channel_data_all = load_continuous_data(prm, channel)
        #load reference channel
        referenced_data_all = load_reference_channel(prm, channel)
        #reference the channel
        channel_data_all = reference_channel(channel_data_all[:,0:150000], referenced_data_all)
        #filter referenced data
        rewrite_contiuous_channel(prm, channel,channel_data_all)
