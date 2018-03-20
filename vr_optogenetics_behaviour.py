
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



def plot_speed(prm, speed_light, speed_nolight, param):

    print('plotting speed...')

    #plot continuous data
    fig = plt.figure(figsize = (14,8))
    ax = fig.add_subplot(111)
    ax.plot(np.arange(0,20,1),speed_light, label='light')
    ax.plot(np.arange(0,20,1),speed_nolight, label='nolight')
    vr_plot_utility.makelegend(fig,ax,0.4)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=7) # set number of ticks on y axis
    ax.set_xlabel('Location (cm)', fontsize=18, labelpad = 20)
    ax.set_ylabel('Speed (cm/s)', fontsize=18, labelpad = 20)

    vr_plot_utility.adjust_spines(ax, ['left','bottom'])
    vr_plot_utility.adjust_spine_thickness(ax)
    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.15, right = 0.92, top = 0.92)

    if param == 1:
        fig.savefig(prm.get_filepath() + 'Behaviour/Analysis/Speed/' + 'Speed_light.png', dpi=200)
        plt.close()
    if param == 2:
        fig.savefig(prm.get_filepath() + 'Behaviour/Analysis/Speed/' + 'Speed_nolight.png', dpi=200)
        plt.close()

def create_speed_hist(prm, light, nolight):
    l_bin_locations = np.zeros((20))
    nl_bin_locations = np.zeros((20))
    for loc_count,loc in enumerate(np.arange(1,200,10)):
        stop_sum = light[np.where(np.logical_and(light[:,3] < (loc+5),  light[:,3] > (loc-5))),4]
        sum = np.mean(stop_sum)
        l_bin_locations[loc_count]= sum

        stop_sum = nolight[np.where(np.logical_and(nolight[:,3] < (loc+5),  nolight[:,3] > (loc-5))), 4]
        sum = np.mean(stop_sum)
        nl_bin_locations[loc_count]= sum

    return l_bin_locations, nl_bin_locations


def load_and_plot_speed(prm):

    light = np.load(prm.get_filepath() + "Behaviour/Data/light.npy")
    no_light = np.load(prm.get_filepath() + "Behaviour/Data/nolight.npy")

    speed_light, speed_nolight = create_speed_hist(prm, light, no_light)

    plot_speed(prm,speed_light, speed_nolight, 1)
