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


    #print(channel_all_data.shape, moves_light.shape)
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
