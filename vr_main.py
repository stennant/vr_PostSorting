import glob
import os
import vr_parameters
import vr_process_movement
import vr_plot_stops
import vr_plot_spikes
import vr_stops
import vr_sorted_firing_times
import vr_trial_types
import vr_plot_continuous_data
import vr_fft
import vr_oscillations
import vr_rewrite_continuous_data
import vr_optogenetics
import vr_optogenetics_behaviour

prm = vr_parameters.Parameters()


def init_vr_params():
    # - 30 cm black box;60 cm outbound journey;20 cm reward zone;60 cm outbound journey;30 cm black box
    prm.set_stop_threshold(0.7)  # speed is given in cm/200ms 0.7*1/2000
    prm.set_num_channels(16)
    prm.set_movement_ch('100_ADC2.continuous')
    prm.set_opto_ch('100_ADC3.continuous')
    prm.set_waveform_size(40)  # number of sampling points to take when taking waveform for spikes (1ms)

    prm.set_track_length(200)
    prm.set_beginning_of_outbound(30)
    prm.set_reward_zone(90)


def init_open_field_params():
    pass

'''
Initializes parameters
    filepath : string, location of raw data file
    filename : string, name of raw data file (without raw.kwd extension)
    good_channels : int, list, channels that are not dead
    stop_threshold : float, given in cm/200ms.
        example:
        0.7cm/200ms = 0.7(1/200cm)/ms = 0.7(1000/200cm/s) = 0.7(5cm/s) = 0.7/5 cm/s
    num_channels : int, number of recording channels
    movement_ch : channel number for movement information
'''


def init_params():

    filename = '2018-02-12_11-22-14'
    #filename = '552_D10_2018-03-09_15-39-54' # test with

    prm.set_filepath('/Users/sarahtennant/Work/Analysis/Opto/Ephys/PVCre1/' + str(filename))
    prm.set_behaviour_data_path('/Users/sarahtennant/Work/Analysis/Opto/Ephys/PVCre1/' + str(filename) + '/Behaviour/Data/')
    prm.set_behaviour_analysis_path('/Users/sarahtennant/Work/Analysis/Opto/Ephys/PVCre1/' + str(filename) + '/Behaviour/Analysis/')
    prm.set_firings_path('/Users/sarahtennant/Work/Analysis/Opto/Ephys/PVCre1/' + str(filename) + '/T4_firings.mda')
    prm.set_sampling_rate(30000)

    prm.set_file(prm.get_filepath(), prm.get_filename())
    prm.set_num_tetrodes(4)

    prm.set_current_tetrode(2)
    prm.set_current_continuous(13)

    prm.set_is_open_field(False)
    prm.set_is_vr(True)

    if prm.is_vr is True:
        init_vr_params()

    if prm.is_open_field is True:
        init_open_field_params()


def process_a_dir(dir_name):
    print('All folders in {} will be processed.'.format(dir_name))
    prm.set_date(dir_name.rsplit('/', 2)[-2])
    prm.set_filepath(dir_name)

    if prm.is_vr is True:

        #following functions process movement information and plot stops per trial
        vr_process_movement.save_or_open_movement_arrays(prm)
        #print('movement has been analysed')
        vr_trial_types.save_or_open_trial_arrays(prm)
        #print('trial type information has been analysed')
        vr_plot_stops.plot_stops(prm)
        #print('Stops have been plotted')

        # plot firing times of clusters against location
        #vr_sorted_firing_times.process_firing_times(prm)
        #print('Firing times have been plotted')

        #load continuous data
        #vr_plot_continuous_data.load_and_plot_continuous_raw(prm)
        #print('continuous raw data has been loaded and plotted')

        #reference continuous data
        #vr_plot_continuous_data.load_and_plot_continuous_referenced(prm)
        #print('continuous referenced data has been loaded and plotted')

        #plot power spectrum
        #vr_fft.calculate_and_plot_power_spectrum(prm)
        #print('power spectrum has been loaded and plotted')

        # filter continuous data for theta and gamma
        #vr_oscillations.load_and_plot_theta_and_gamma(prm)
        #print('data filtered for theta and gamma activity')

        # load and process optogenetics
        #vr_optogenetics.load_and_process_opto_channel(prm)
        #print('optogenetics processed')

        # load and plot stops with opto highlighted
        #vr_plot_stops.plot_opto_stops(prm)

        #vr_optogenetics_behaviour.load_and_plot_speed(prm)


def process_files():
    prm.get_filepath()
    for name in glob.glob(prm.get_filepath()+'*'):
        print(name)
        os.path.isdir(name)
        print("Files processed")

        process_a_dir(name + '/')
        print("Files processed")


def main():
    print('-------------------------------------------------------------')
    print('Check whether the arrays have the correct size in the folder. '
          'An incorrect array only gets deleted automatically if its size is 0. Otherwise, '
          'it needs to be deleted manually in order for it to be generated again.')
    print('-------------------------------------------------------------')

    init_params()
    print('params processed')
    process_files()


if __name__ == '__main__':
    main()
