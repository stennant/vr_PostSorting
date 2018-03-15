'''
Functions for converting open ephys data to mountainsort's mda format

'''

import vr_file_utility
import matplotlib.pylab as plt
import mdaio
import numpy as np
import vr_open_ephys_IO
import os


def pad_event(waveforms, channel, samples_per_spike, event):
    padded_event = np.hstack((waveforms[event, :, channel], np.zeros(samples_per_spike)))
    return padded_event


def get_padded_array(waveforms, samples_per_spike):
    number_of_events = waveforms.shape[0]
    all_padded = np.zeros((4, samples_per_spike*2*number_of_events))

    for channel in range(4):
        padded_events_ch = np.zeros((number_of_events, samples_per_spike*2))
        for event in range(number_of_events):
            padded_event = pad_event(waveforms, channel, samples_per_spike, event)
            padded_events_ch[event, :] = padded_event
        padded_events_ch = padded_events_ch.flatten('C')
        all_padded[channel, :] = padded_events_ch

    too_big_indices = np.where(all_padded > 30000)
    too_small_indices = np.where(all_padded < -30000)

    all_padded[too_big_indices] = 30000
    all_padded[too_small_indices] = -30000

    all_padded = all_padded * (-1)*10000000

    all_padded = np.asarray(all_padded, dtype='int16')

    return all_padded


def get_peak_indices(waveforms, samples_per_spike):
    number_of_events = waveforms.shape[0]
    waveforms2d = np.zeros((number_of_events, 4*samples_per_spike))

    for event in range(number_of_events):
        waveforms2d[event, :] = waveforms[event, :, :].flatten()

    peak_indices_all_ch = np.argmax(waveforms2d, 1)
    peak_indices_in_wave = np.floor(peak_indices_all_ch/4)
    peak_indices_in_wave = np.asarray(peak_indices_in_wave, dtype='int16')
    peak_indices_all_events = peak_indices_in_wave + np.arange(0, number_of_events)*40
    peak_indices = np.array(peak_indices_all_events, dtype='int32')
    return peak_indices # add event number to this, it needs the absolute index not 0-40


def convert_spk_to_mda(prm):
    vr_file_utility.create_folder_structure(prm)
    folder_path = prm.get_filepath()
    spike_data_path = prm.get_spike_path() + '\\'
    number_of_tetrodes = prm.get_num_tetrodes()
    samples_per_spike = prm.get_waveform_size()

    if os.path.isfile(spike_data_path + 't1_' + prm.get_date() + '\\raw.nt1.mda') is False:
        vr_file_utility.create_ephys_folder_structure(prm)

        for tetrode in range(number_of_tetrodes):
            file_path = folder_path + 'TT' + str(tetrode) + '.spikes'
            waveforms, timestamps = vr_open_ephys_IO.get_data_spike(folder_path, file_path, 'TT' + str(tetrode + 1))
            np.save(spike_data_path + 't' + str(tetrode + 1) + '_' + prm.get_date() + '\\TT' + str(tetrode + 1) + '_timestamps', timestamps)  # todo: this is shifted by 10 seconds relative to light and location!

            padded_array = get_padded_array(waveforms, samples_per_spike)

            mdaio.writemda16i(padded_array, spike_data_path + 't' + str(tetrode + 1) + '_' + prm.get_date() + '\\raw.nt' + str(tetrode + 1) + '.mda')
            peak_indices = get_peak_indices(waveforms, samples_per_spike)
            mdaio.writemda32i(peak_indices, spike_data_path + 't' + str(tetrode + 1) + '_' + prm.get_date() + '\\event_times.nt' + str(tetrode + 1) + '.mda')

            mdaio.writemda32(timestamps, spike_data_path + 't' + str(tetrode + 1) + '_' + prm.get_date() + '\\timestamps.nt' + str(tetrode + 1) + '.mda')


def convert_continuous_to_mda(prm):
    vr_file_utility.create_folder_structure(prm)
    number_of_tetrodes = prm.get_num_tetrodes()
    folder_path = prm.get_filepath()
    spike_data_path = prm.get_spike_path() + '\\'
    channel_data_all = []

    if os.path.isfile(spike_data_path + 't1_' + prm.get_date() + '\\raw.nt1.mda') is False:
        vr_file_utility.create_ephys_folder_structure(prm)

    for tetrode in range(number_of_tetrodes):
        for channel in range(4):
            file_path = folder_path + '100_CH' + str(tetrode*4 + channel + 1) + '.continuous' #todo this should bw in params, it is 100 for me, 105 for Tizzy (I don't have _0)
            channel_data = vr_open_ephys_IO.get_data_continuous(prm, file_path)
            channel_data_all.append(channel_data)

        recording_length = len(channel_data_all[0])
        channels_tetrode = np.zeros((4, recording_length))

        for ch in range(4):
            channels_tetrode[ch, :] = channel_data_all[ch]
        mdaio.writemda16i(channels_tetrode, spike_data_path + 't' + str(tetrode + 1) + '_' + prm.get_date() + '_continuous\\raw.nt' + str(tetrode + 1) + '.mda')


def convert_all_tetrodes_to_mda(prm):
    vr_file_utility.create_folder_structure(prm)
    number_of_tetrodes = prm.get_num_tetrodes()
    folder_path = prm.get_filepath()
    spike_data_path = prm.get_spike_path() + '\\'
    channel_data_all = []

    path = spike_data_path + 'raw' + '.mda'

    for channel in range(16):
        file_path = folder_path + '100_CH' + str(channel + 1) + '.continuous'
        channel_data = vr_open_ephys_IO.get_data_continuous(prm, file_path)
        channel_data_all.append(channel_data)

    recording_length = len(channel_data_all[0])

    channels_all = np.zeros((number_of_tetrodes*4, recording_length))

    for ch in range(16):
        channels_all[ch, :] = channel_data_all[ch]
    mdaio.writemda16i(channels_all, path)












