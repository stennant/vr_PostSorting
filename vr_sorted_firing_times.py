import numpy as np
import vr_trial_types
import vr_plot_spikes
import tables

"""""

# Old code which opened the firings.mda file

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

"""""



def get_snippets(prm):
    path = prm.get_filepath() + 'Firings0.mat'
    firings = tables.open_file(path)
    cluster_id = firings.root.cluid[:]
    cluster_id = cluster_id.flatten()
    spike_index = firings.root.spikeind[:]
    spike_index = spike_index.flatten()
    waveforms = firings.root.waveforms[:]
    #print(spike_index[0:100],'spike_index',spike_index.shape, cluster_id[0:100], 'cluster_id' ,cluster_id.shape)
    return cluster_id, spike_index, waveforms


def get_time_in_bin(prm, location, number_of_trials):
    bin_locations = np.zeros((200,len(np.unique(number_of_trials))))
    data = np.vstack((location,number_of_trials)); data=np.transpose(data)
    for tcount,trial in enumerate(np.unique(number_of_trials)):
        location = data[data[:, 1] == trial,:]
        for loc_count,loc in enumerate(np.arange(1,200,1)):
            time_sum = location[np.where(np.logical_and(location <= (loc+1),  location > (loc)))]
            sum = (len(time_sum))/30 # time in ms spent in that region
            bin_locations[loc_count, tcount]= sum
    return bin_locations



def process_firing_times(prm):
    trials = np.load(prm.get_behaviour_data_path() + '/trial_numbers.npy')
    location = np.load(prm.get_behaviour_data_path() + '/location.npy')
    cluster_id, spike_index, waveforms = get_snippets(prm)
    units_list = np.unique(cluster_id)

    for unit_id, unit in enumerate(units_list):
        firing_times_unit = np.take(spike_index, np.where(cluster_id == unit))
        times = get_time_in_bin(prm, location, trials)
        # call histogram/ plotting functions for each cell here
        vr_plot_spikes.plot_spikes(prm, firing_times_unit, unit, times)








