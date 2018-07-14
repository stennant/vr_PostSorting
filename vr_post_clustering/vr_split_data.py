from __future__ import division
import numpy as np
import vr_process_movement
import vr_file_utility
import matplotlib.pylab as plt
import numpy as np
import os
import vr_open_ephys_IO
import vr_trial_types
import vr_process_movement
import vr_optogenetics


'''
Makes an array with the indices when the animal moves (speed>=speed_threshold) and one when is doesn't.
The mouse is considered to stop when the speed is below speed_threshold (speed<speed_threshold).

input
    prm : object, parameters
    speed : numpy array, average speed calculated from instant velocity

output
    stationary : numpy array, indices where speed is <= threshold
    moves : numpy array, indices where speed is <= threshold

'''



def save_indicies_for_movement_and_stationary(prm):
    global trial_num

    if os.path.isfile(prm.get_filepath() + "Behaviour/Data/moves_indicies.npy") is False:

        speed = np.load(prm.get_filepath() + "Behaviour/Data/speed.npy")
        speed = vr_process_movement.remove_beginning_and_end(prm,speed)

        print('splitting movement and stationary data...')

        threshold = prm.get_stop_threshold()
        moves = np.where(abs(speed) > threshold)
        stationary = np.where(abs(speed) <= threshold)

        print('data split')
        np.save(prm.get_filepath() + "Behaviour/Data/moves_indicies", moves)
        np.save(prm.get_filepath() + "Behaviour/Data/stationary_indicies", stationary)

    else:
        moves = np.load(prm.get_filepath() + "Behaviour/Data/moves_indicies.npy")
        stationary = np.load(prm.get_filepath() + "Behaviour/Data/stationary_indicies.npy")

    return moves, stationary




# split the data based on previously saved indicies
def split_movement_stationary_channel(prm, channel_all_data):

    moves = np.load(prm.get_filepath() + "Behaviour/Data/moves_indicies.npy")
    stationary = np.load(prm.get_filepath() + "Behaviour/Data/stationary_indicies.npy")

    channel_all_data = np.transpose(channel_all_data)
    channel_all_data = vr_process_movement.remove_beginning_and_end(prm,channel_all_data[:,0])

    moves = np.take(channel_all_data, moves)
    stationary = np.take(channel_all_data, stationary)

    return moves, stationary



# find duplicate values in array and save them into a seperate array
def duplicates(seq):
    print('finding duplicate indicies...')
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    return list(seen_twice)


# find duplicate values in array and save them into a seperate array
def not_duplicates(seq):
    print('finding duplicate indicies...')
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    not_seen_twice = set(x for x in seq if x in seen or seen_add(x))
    return list(not_seen_twice)


def split_light_and_no_light_indicies(prm):

    if os.path.isfile(prm.get_filepath() + "Behaviour/Data/light_indicies.npy") is False:

        opto_channel = np.load(prm.get_filepath() + "Behaviour/Data/optogenetics.npy")
        trial_channel = np.load(prm.get_filepath() + "Behaviour/Data/trial_numbers.npy")

        print('splitting stimulation and non-stimulation trials...')

        # this code takes the whole 5 seconds the LED is on
        light = []
        light_indicies = []

        light_trials=[]
        nolight_trials=[]

        for t, trial in enumerate(np.unique(trial_channel)):
            trial_data = opto_channel[trial_channel[:] == trial]
            for p,point in enumerate(trial_data):
                if point > 0.5:
                    light_indicies = np.append(light_indicies,p)
                    light_trials = np.append(light_trials,point)
                    break

        for x in light_indicies:
            light = np.append(light, (np.arange(x,x+150000,1)))

        nolight = np.arange(0, len(trial_channel),1); nolight = np.hstack((light,nolight))
        nolight = duplicates(nolight)

        # this code takes only when the pulse is up
        #light = np.where(abs(opto_channel) > 0.5)
        #nolight = np.where(abs(opto_channel) < 0.5) # this code takes only when the pulse is up

        print('trials split')
        np.save(prm.get_filepath() + "Behaviour/Data/light_indicies", light)
        np.save(prm.get_filepath() + "Behaviour/Data/nolight_indicies", nolight)

    else:
        light = np.load(prm.get_filepath() + "Behaviour/Data/light_indicies.npy")
        nolight = np.load(prm.get_filepath() + "Behaviour/Data/nolight_indicies.npy")

    return np.array(light), np.array(nolight)



def save_indicies_for_light_and_no_light(prm):

    #load and save opto channel data
    opto_data = vr_optogenetics.load_and_save_opto_channel(prm)

    #split data according to light and no light stimulation
    light, no_light = split_light_and_no_light_indicies(prm)
    print('data split by light/nolight')



# split the data based on previously saved indicies
def split_light_nolight_movement_stationary(prm, channel_all_data):

    moves = np.load(prm.get_filepath() + "Behaviour/Data/moves_indicies.npy")
    stationary = np.load(prm.get_filepath() + "Behaviour/Data/stationary_indicies.npy")

    light = np.load(prm.get_filepath() + "Behaviour/Data/light_indicies.npy")
    nolight = np.load(prm.get_filepath() + "Behaviour/Data/nolight_indicies.npy")

    channel_all_data = np.transpose(channel_all_data)
    channel_all_data = vr_process_movement.remove_beginning_and_end(prm,channel_all_data[:,0])

    #find duplicates
    moves_light = np.hstack((np.transpose(moves[0,:]), light))
    moves_light = duplicates(moves_light)
    #print(moves_light)


    moves_nolight = np.hstack((np.transpose(moves[0,:]), nolight))
    moves_nolight = duplicates(moves_nolight)

    stationary_light = np.hstack((np.transpose(stationary[0,:]), light))
    stationary_light = duplicates(stationary_light)

    stationary_nolight = np.hstack((np.transpose(stationary[0,:]), nolight))
    stationary_nolight = duplicates(stationary_nolight)

    #print(channel_all_data.shape, moves_light.shape)
    moves_light = np.take(channel_all_data, moves_light)
    stationary_light = np.take(channel_all_data, stationary_light)
    moves_nolight = np.take(channel_all_data, moves_nolight)
    stationary_nolight = np.take(channel_all_data, stationary_nolight)

    return moves_light, stationary_light, moves_nolight, stationary_nolight


def calculate_miss_trials(prm, trials, store):
    trial_numbers = np.unique(trials)
    hit_trials = np.unique(store)

    seq = np.hstack((trial_numbers,hit_trials))
    unique_trials, unique_counts = np.unique(seq, return_counts=True)
    miss_trials = unique_trials[np.where(unique_counts[:] == 1)]

    return miss_trials



def calculate_hit_trials(prm):
    trials = np.load(prm.get_filepath() + "Behaviour/Data/trial_numbers.npy")
    location = np.load(prm.get_filepath() + "Behaviour/Data/location.npy")
    speed = np.load(prm.get_filepath() + "Behaviour/Data/speed.npy")
    STOP_THRESHOLD = 0.7

    array = np.vstack((location, speed, trials)); array = np.transpose(array)
    trial_numbers = np.unique(array[:,2])

    moving = False
    store = []
    for tcount, trial in enumerate(trial_numbers):
        data = array[array[:,2] == trial,:]
        for rowcount, row in enumerate(data):
             if(data[rowcount,1]<=STOP_THRESHOLD and moving and data[rowcount,0] > 88 and data[rowcount, 0] < 110): # if speed is below threshold
                moving = False
                trial = data[rowcount,2]
                store = np.append(store,trial)
             if(row[1]>STOP_THRESHOLD and not moving):
                moving = True
        tcount+=1

    return np.array(store), trials



def hit_miss_indicies(prm):

    hit_trials, trials = calculate_hit_trials(prm)
    miss_trials = calculate_miss_trials(prm, trials, hit_trials)

    print('hit and miss trials split')
    np.save(prm.get_filepath() + "Behaviour/Data/hit_trials", hit_trials)
    np.save(prm.get_filepath() + "Behaviour/Data/miss_trials", miss_trials)

    print('Hit and miss trials calculated')

    return hit_trials, miss_trials



def hit_miss_trials(prm, hit_trials, miss_trials, before_stop, after_stop):
    trials_hit = np.unique(hit_trials)
    trials_miss = np.unique(miss_trials)


    hit_before_stop = np.zeros((0, before_stop.shape[1]))
    hit_after_stop = np.zeros((0, before_stop.shape[1]))

    for tcount, trial in enumerate(trials_hit):
        data_before = before_stop[before_stop[:,0] == trial,:]
        data_after = after_stop[after_stop[:,0] == trial,:]
        hit_before_stop = np.vstack((hit_before_stop,data_before))
        hit_after_stop = np.vstack((hit_after_stop,data_after))

    miss_before_stop = np.zeros((0, before_stop.shape[1]))
    miss_after_stop = np.zeros((0, before_stop.shape[1]))

    for tcount, trial in enumerate(trials_miss):
        data_before = before_stop[before_stop[:,0] == trial,:]
        data_after = after_stop[after_stop[:,0] == trial,:]
        miss_before_stop = np.vstack((miss_before_stop,data_before))
        miss_after_stop = np.vstack((miss_after_stop,data_after))

    print('Before and after stop data separated for hit and miss trials')

    return hit_before_stop,miss_before_stop,hit_after_stop,miss_after_stop



def hit_miss_speed(prm, hit_trials, miss_trials,  middle_upper,upper, middle_lower, lower):
    trials_hit = np.unique(hit_trials)
    trials_miss = np.unique(miss_trials)


    hit_upper = np.zeros((0, middle_upper.shape[1]))
    hit_m_upper = np.zeros((0, middle_upper.shape[1]))
    hit_lower = np.zeros((0, middle_upper.shape[1]))
    hit_m_lower = np.zeros((0, middle_upper.shape[1]))

    for tcount, trial in enumerate(trials_hit):
        data_upper = upper[upper[:,0] == trial,:]
        data_m_upper = middle_upper[middle_upper[:,0] == trial,:]
        data_lower = middle_lower[middle_lower[:,0] == trial,:]
        data_m_lower = lower[lower[:,0] == trial,:]

        hit_upper = np.vstack((hit_upper,data_upper))
        hit_m_upper = np.vstack((hit_m_upper,data_m_upper))
        hit_lower = np.vstack((hit_lower,data_lower))
        hit_m_lower = np.vstack((hit_m_lower,data_m_lower))

    miss_upper = np.zeros((0, middle_upper.shape[1]))
    miss_m_upper = np.zeros((0, middle_upper.shape[1]))
    miss_lower = np.zeros((0, middle_upper.shape[1]))
    miss_m_lower = np.zeros((0, middle_upper.shape[1]))

    for tcount, trial in enumerate(trials_miss):
        data_upper = upper[upper[:,0] == trial,:]
        data_m_upper = middle_upper[middle_upper[:,0] == trial,:]
        data_lower = middle_lower[middle_lower[:,0] == trial,:]
        data_m_lower = lower[lower[:,0] == trial,:]

        miss_upper = np.vstack((miss_upper,data_upper))
        miss_m_upper = np.vstack((miss_m_upper,data_m_upper))
        miss_lower = np.vstack((miss_lower,data_lower))
        miss_m_lower = np.vstack((miss_m_lower,data_m_lower))

    print('Speed data separated for hit and miss trials')

    return miss_upper,miss_m_upper,miss_lower,miss_m_lower,hit_upper,hit_m_upper,hit_lower,hit_m_lower
