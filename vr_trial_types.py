'''
Saves the corresponding signal arrays for beaconed, non-beaconed and probe trials.
In our virtual reality task, every every tenth trial is a probe trial, and every fifth trial that is not a probe trial
 is a non-beaconed trial. The rest of the trials are beaconed. In these functions, the indices for the different
trial types are separated and saved into beaconed, nbeaconed and probe arrays. If the arrays already exist, then the
data is loaded from the file (the location of this file is specified in init_params in main).
'''

import numpy as np
import os
import matplotlib.pylab as plt
import vr_process_movement
#import file_reader
import vr_parameters
#import signal_for_indices
import vr_open_ephys_IO

#fr = file_reader.FileReader()

beaconed = None
nbeaconed = None
probe = None
trial_num = None


def keep_first_from_close_series(array, threshold):
    num_delete = 1
    while num_delete > 0:
        diff = np.ediff1d(array, to_begin= threshold + 1)
        to_delete = np.where(diff <= threshold)
        num_delete = len(to_delete[0])

        if num_delete > 0:
            array = np.delete(array, to_delete)

    return array

'''
Finds indices for beginning of outbound journey
input
    prm : object, parameters
    location : numpy array, location of animal
output
    output beginnings : numpy array, first indices in outbound region
'''


def get_outbound_beginning(prm, location):
    filepath = prm.get_filepath()
    if os.path.isfile(filepath + "Behaviour/Data/outbound.npy") is False:
        outbound_beginnings = get_outbound_beginning_indices(prm, location)
        np.save(filepath + "Behaviour/Data/outbound", outbound_beginnings)

    else:
        outbound_beginnings = np.load(filepath + "Behaviour/Data/outbound.npy")
    return outbound_beginnings


def get_outbound_beginning_indices(prm, location):
    outbound_border = prm.get_beginning_of_outbound()
    outbound = np.where((location >= outbound_border) & (location <= outbound_border + 4))
    outbound = np.asanyarray(outbound)
    outbound_plus_one = outbound + 1
    outbound_plus_one = np.asanyarray(outbound_plus_one)
    outbound_beginnings = np.setdiff1d(outbound, outbound_plus_one)
    return outbound_beginnings


def get_beginning_of_track_positions(prm, location):
    filepath = prm.get_filepath()
    if os.path.isfile(filepath + "Behaviour/Data/beginning_of_track.npy") is False:
        position = 0
        beginning_of_track = np.where((location >= position) & (location <= position + 4))
        beginning_of_track = np.asanyarray(beginning_of_track)
        beginning_plus_one = beginning_of_track + 1
        beginning_plus_one = np.asanyarray(beginning_plus_one)
        track_beginnings = np.setdiff1d(beginning_of_track, beginning_plus_one)
        track_beginnings = keep_first_from_close_series(track_beginnings, 30000)
        np.save(filepath + "Behaviour/Data/beginning_of_track", track_beginnings)

    else:
        track_beginnings = np.load(filepath + "Behaviour/Data/beginning_of_track.npy")

    return track_beginnings





def load_trial_types_from_continuous(prm):

    file_path = prm.get_filepath() + prm.first_trial_channel() #todo this should bw in params, it is 100 for me, 105 for Tizzy (I don't have _0)
    trial_first = vr_open_ephys_IO.get_data_continuous(prm, file_path)
    print('first trial channel loaded')
    file_path = prm.get_filepath() + prm.second_trial_channel() #todo this should bw in params, it is 100 for me, 105 for Tizzy (I don't have _0)
    trial_second = vr_open_ephys_IO.get_data_continuous(prm, file_path)
    print('second trial channel loaded')

    if os.path.isfile(prm.get_behaviour_data_path() + "/con_trial_type.npy") is False:
        trial_type = []
        for p,point in np.enumerate(file_path):
            ttp=0
            if (trial_first[p] <5 and trial_second[p] <5):
                ttp=0
            elif (trial_first[p] > 5 and trial_second[p] < 5):
                ttp=1
            elif (trial_first[p] > 5 and trial_second[p] > 5):
                ttp=2
            trial_type=np.append(trial_type,ttp)
        np.save(prm.get_filepath() + "Behaviour/Data/con_trial_type.npy", trial_type)

    return trial_type



def split_trial_types(prm, location, trial_type):
    global beaconed
    global nbeaconed
    global probe
    global trial_num
    if os.path.isfile(prm.get_behaviour_data_path() + "/beaconed.npy") is False:
        beaconed = []
        nbeaconed = []
        probe = []
        trial_num = 1

        for loc, loc_count in enumerate(range(len(location))):
            if trial_type == 2:
                probe.append(location[loc_count])
            elif trial_type == 1:
                nbeaconed.append(location[loc_count])
            else:
                beaconed.append(location[loc_count])
        np.save(prm.get_filepath() + "Behaviour/Data/beaconed.npy", beaconed)
        np.save(prm.get_filepath() + "Behaviour/Data/nbeaconed.npy", nbeaconed)
        np.save(prm.get_filepath() + "Behaviour/Data/probe.npy", probe)
    else:
        beaconed = np.load(prm.get_filepath() + "Behaviour/Data/beaconed.npy")
        nbeaconed = np.load(prm.get_filepath() + "Behaviour/Data/nbeaconed.npy")
        probe = np.load(prm.get_filepath() + "Behaviour/Data/probe.npy")
    return beaconed, nbeaconed, probe



def trial_numbers(prm,location):
    global trial_num
    if os.path.isfile(prm.get_behaviour_data_path() + "/beaconed.npy") is False:
        trial_num = 1
        for i in range(len(location)):
            if i > 0 and (location[i-1]-location[i]) > 150:
                trial_num += 1
        np.save(prm.get_filepath() + "Behaviour/Data/trial_num.npy", trial_num)
    else:
        trial_num = np.load(prm.get_filepath() + "Behaviour/Data/trial_num.npy")


"""""
def beaconed_nbeaconed_probe(prm, location, trial_type):
    global beaconed
    global nbeaconed
    global probe
    global trial_num
    if os.path.isfile(prm.get_behaviour_data_path() + "/beaconed.npy") is False:
        beaconed = []
        nbeaconed = []
        probe = []
        trial_num = 1
        for i in range(len(location)):
            if i > 0 and (location[i-1]-location[i]) > 150:
                trial_num += 1
            if trial_num % 10 == 0:
                probe.append(i)
            elif trial_num % 5 == 0:
                nbeaconed.append(i)
            else:
                beaconed.append(int(i))
        np.save(prm.get_filepath() + "Behaviour/Data/beaconed.npy", beaconed)
        np.save(prm.get_filepath() + "Behaviour/Data/nbeaconed.npy", nbeaconed)
        np.save(prm.get_filepath() + "Behaviour/Data/probe.npy", probe)
        np.save(prm.get_filepath() + "Behaviour/Data/trial_num.npy", trial_num)
    else:
        beaconed = np.load(prm.get_filepath() + "Behaviour/Data/beaconed.npy")
        nbeaconed = np.load(prm.get_filepath() + "Behaviour/Data/nbeaconed.npy")
        probe = np.load(prm.get_filepath() + "Behaviour/Data/probe.npy")
        trial_num = np.load(prm.get_filepath() + "Behaviour/Data/trial_num.npy")
    return beaconed, nbeaconed, probe, trial_num
"""""



# If beaconed, non-beaconed and probe arrays don't exist, the functions to create them are called here
def cached_trial_type(prm, location):
    if os.path.isfile(prm.get_filepath() + "Behaviour/Data/beaconed.npy") is False or os.path.isfile(prm.get_filepath() + "Behaviour/Data/probe.npy") is False:
        trial_types=load_trial_types_from_continuous(prm)
        beaconed_trials, nbeaconed_trials, probe_trials = split_trial_types(prm,location, trial_types)

        np.save(prm.get_filepath() + "Behaviour/Data/beaconed", beaconed_trials)
        np.save(prm.get_filepath() + "Behaviour/Data/nbeaconed", nbeaconed_trials)
        np.save(prm.get_filepath() + "Behaviour/Data/probe", probe_trials)
    else:
        beaconed_trials = np.load(prm.get_filepath() + "Behaviour/Data/beaconed.npy")
        nbeaconed_trials = np.load(prm.get_filepath() + "Behaviour/Data/nbeaconed.npy")
        probe_trials = np.load(prm.get_filepath() + "Behaviour/Data/probe.npy")
    return beaconed_trials, nbeaconed_trials, probe_trials



# Calculate beaconed, non-beaconed and probe trial indices, and save them if they don't exist yet
def save_or_open_trial_arrays(prm):
    # Check for empty files and delete them if there are any
    for file in os.listdir(prm.get_filepath() + '/Behaviour/Data'):
        os.chdir(prm.get_filepath())
        #if file.endswith(".npy") and os.path.getsize(file) == 0:
        #    print('---FILE ERROR: The size of '+file+' is 0, something is wrong.---')
    location = np.load(prm.get_filepath() + '/Behaviour/Data/location.npy')

    beaconed_trials, nbeaconed_trials, probe_trials \
        = cached_trial_type(prm, location)

    trial_numbers(prm,location)

    return beaconed_trials, nbeaconed_trials, probe_trials
