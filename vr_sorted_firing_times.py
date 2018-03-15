import mdaio
import numpy as np
import vr_trial_types
import vr_plot_spikes


def get_firing_info(prm):
    firing_times_path = prm.get_firings_path()
    firing_info = mdaio.readmda(firing_times_path)
    units_list = np.unique(firing_info[2]) # find unique clusters/units
    channel_list = np.unique(firing_info[0])
    return units_list, firing_info


def get_firing_times_of_unit(prm, unit_id):
    units_list, firing_info = get_firing_info(prm)
    if unit_id > len(units_list):
        print('The unit id given to get_firing_times_of_unit does not exist.')

    firing_times_of_unit_indices = np.where(firing_info[2] == unit_id)
    firing_times_of_unit = np.take(firing_info[1], firing_times_of_unit_indices)
    return firing_times_of_unit


def get_channel_ids_for_unit(prm, unit_id):
    units_list, firing_info = get_firing_info(prm)
    if unit_id > len(units_list):
        print('The unit id given to get_firing_times_of_unit does not exist.')

    firing_ch_ids_indices = np.where(firing_info[2] == unit_id)
    ch_ids_for_unit = np.take(firing_info[0], firing_ch_ids_indices)

    return ch_ids_for_unit


def process_firing_times(prm):

    units_list, firing_info = get_firing_info(prm)
    for unit_id, unit in enumerate(units_list):
        firing_times_unit = get_firing_times_of_unit(prm, unit)
        ch_ids_unit = get_channel_ids_for_unit(prm, unit)
        # call histogram/ plotting functions for each cell here
        vr_plot_spikes.plot_spikes(prm, firing_times_unit, unit)








