import glob
import os


def find_the_file(file_path, pattern, type):
    name = None
    file_found = True
    file_name = None

    file_counter = 0
    for name in glob.glob(file_path + pattern):
        file_counter += 1
        pass

    if file_counter > 1:
        print('There are more than one ' + type + ' files in this folder. This is may not be okay.')

    if name is not None:
        file_name = name.rsplit('/', 1)[1]
    else:
        print('The '+ type + ' file(such as ' + pattern + ' )is not here, or it has an unusual name.')

        file_found = False

    return file_name, file_found


def create_behaviour_folder_structure(prm):
    movement_path = prm.get_filepath() + 'Behaviour'
    prm.set_behaviour_path(movement_path)

    data_path = movement_path + '/Data'
    prm.set_behaviour_data_path(data_path)

    analysis_path = movement_path + '/Analysis'
    prm.set_behaviour_analysis_path(analysis_path)

    stops_plots_path = analysis_path + '/stops_on_track'
    spikes_plots_path = analysis_path + '/spikes_on_track'
    speed_plots_path = analysis_path + '/speed'

    if os.path.exists(movement_path) is False:
        print('Behavioural data will be saved in {}.'.format(movement_path))
        os.makedirs(movement_path)
        os.makedirs(data_path)
        os.makedirs(analysis_path)
        os.makedirs(stops_plots_path)
        os.makedirs(spikes_plots_path)
        os.makedirs(speed_plots_path)


def create_ephys_folder_structure(prm):
    ephys_path = prm.get_filepath() + 'Electrophysiology'
    prm.set_ephys_path(ephys_path)

    continuous_path = ephys_path + '/continuous'
    prm.set_continuous_path(continuous_path)

    continuous_raw_path = continuous_path + '/raw'
    continuous_ref_path = continuous_path + '/referenced'

    oscillations_path = ephys_path + '/theta_and_gamma'

    opto_path = ephys_path + '/opto_stimulation'
    opto_continuous_path = opto_path + '/continuous'
    opto_continuous_raw_path = opto_continuous_path + '/raw'
    opto_continuous_filtered_path = opto_continuous_path + '/filtered'

    fft_path = ephys_path + '/fft'
    prm.set_fft_path(fft_path)

    fft_opto_path = opto_path + '/fft'

    theta_opto_path = opto_path + '/theta'

    spike_path = ephys_path + '/spike_sorting'
    prm.set_spike_path(spike_path)

    sorting_t1_path = spike_path + '/t1_' + prm.get_date()
    sorting_t2_path = spike_path + '/t2_' + prm.get_date()
    sorting_t3_path = spike_path + '/t3_' + prm.get_date()
    sorting_t4_path = spike_path + '/t4_' + prm.get_date()

    sorting_t1_path_continuous = spike_path + '/t1_' + prm.get_date() + '_continuous'
    sorting_t2_path_continuous = spike_path + '/t2_' + prm.get_date() + '_continuous'
    sorting_t3_path_continuous = spike_path + '/t3_' + prm.get_date() + '_continuous'
    sorting_t4_path_continuous = spike_path + '/t4_' + prm.get_date() + '_continuous'

    analysis_path = ephys_path + '/Analysis'
    prm.set_ephys_analysis_path(analysis_path)

    data_path = ephys_path + '/Data'
    prm.set_ephys_data_path(data_path)

    if os.path.exists(ephys_path) is False:
        os.makedirs(ephys_path)
        #os.makedirs(spike_path)
        os.makedirs(continuous_path)
        os.makedirs(opto_path)
        os.makedirs(fft_opto_path)
        os.makedirs(theta_opto_path)
        os.makedirs(opto_continuous_path)
        os.makedirs(opto_continuous_raw_path)
        os.makedirs(opto_continuous_filtered_path)
        os.makedirs(continuous_raw_path)
        os.makedirs(continuous_ref_path)
        os.makedirs(oscillations_path)
        os.makedirs(fft_path)
        os.makedirs(sorting_t1_path)
        os.makedirs(sorting_t2_path)
        os.makedirs(sorting_t3_path)
        os.makedirs(sorting_t4_path)
        #os.makedirs(continuous_t1_path)
        #os.makedirs(continuous_t2_path)
        #os.makedirs(continuous_t3_path)
        #os.makedirs(continuous_t4_path)
        os.makedirs(sorting_t1_path_continuous)
        os.makedirs(sorting_t2_path_continuous)
        os.makedirs(sorting_t3_path_continuous)
        os.makedirs(sorting_t4_path_continuous)

        #os.makedirs(analysis_path)
        #os.makedirs(data_path)


def create_folder_structure(prm):
    create_behaviour_folder_structure(prm)
    create_ephys_folder_structure(prm)


