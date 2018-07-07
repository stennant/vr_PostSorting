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
    referenced = np.zeros((referenced_data_all.shape))
    print('referencing channel...')
    for p, point in enumerate(channel_data_all):
        referenced_value = channel_data_all[p,0] - referenced_data_all[p]
        referenced[p] = referenced_value
    referenced = np.asarray(referenced)
    #referenced = np.hstack((referenced,channel_data_all))
    print('channel referenced')

    return referenced
