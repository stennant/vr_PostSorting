
import vr_file_utility
import vr_open_ephys_IO
import os
import matplotlib.pylab as plt
import numpy as np
import vr_filter
import vr_plot_utility
import vr_optogenetics
import vr_process_movement
import vr_fft
import vr_track_location_plots
import vr_split_data
from scipy import signal
import scipy.fftpack
from scipy import integrate
import vr_power_calculations
from scipy import stats
#loop through stops:
#looping 250 ms of data so will be array[datasize] interval = 7500
#find power - simp - between 70 and 90 hz
#store for all stops


# average power plots for before and after stop data
def plot_average_stop_start_speed(prm,after_store,before_store):
    print('Plotting and saving speed for before and after stops')

    # outbound
    fig = plt.figure(figsize = (7,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.boxplot([before_store,after_store], notch=True, sym='',showmeans=True)
    ax.set_xlim(0.5,2.5)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xticklabels(['Before', 'After'])
    ax.set_ylabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.82, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + '_AvgSpeed_stop&start.png', dpi=200)
    plt.close()

    print('Average speed : movement = ' + str(round(np.nanmean(before_store),2)) + ' +/- ' + str(round(stats.sem(before_store),2)) + ' stationary = ' + str(round(np.nanmean(before_store),2)) + ' +/- ' + str(round(stats.sem(before_store),2)))


def plot_gamma_power_stop_start(prm,after_store,before_store, channel):

    print('Plotting and saving power calculations for before and after stops')

    # outbound
    fig = plt.figure(figsize = (7,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.boxplot([before_store,after_store], notch=True, sym='',showmeans=True)
    ax.set_xlim(0.5,2.5)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xticklabels(['Before', 'After'])
    ax.set_ylabel('Area (PSD (V^2/Hz))', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.82, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_stop&start.png', dpi=200)
    plt.close()

    print('Average gamma power : movement = ' + str(round(np.nanmean(before_store),2)) + ' +/- ' + str(round(stats.sem(before_store),2)) + ' stationary = ' + str(round(np.nanmean(after_store),2)) + ' +/- ' + str(round(stats.sem(after_store),2)))


def plot_gamma_power_difference_stop_start(prm,store, channel):

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.boxplot(store,notch=True, sym='',showmeans=True)
    ax.set_xlim(0.5,2.5)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xticklabels(['Before', 'After'])
    ax.set_ylabel('Area diff (PSD (V^2/Hz))', fontsize = 18, labelpad = 10)
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.21, right = 0.82, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_stop&start_difference.png', dpi=200)
    plt.close()


def plot_gamma_power_stop_start_location(prm,after_store_ob,before_store_ob,after_store_rz,before_store_rz,after_store_hb,before_store_hb, channel):

    print('Plotting power calculations for before and after stops, according to location')

    # outbound
    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([before_store_ob,after_store_ob],notch=True, sym='',showmeans=True)
    ax.set_ylim(0,400)
    ax.set_xlim(0.5,2.5)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xticklabels(['Before', 'After'])

    print('Average gamma power in outbound region : movement = ' + str(round(np.nanmean(before_store_ob),2)) + ' +/- ' + str(round(stats.sem(before_store_ob),2)) + ' stationary = ' + str(round(np.nanmean(after_store_ob),2)) + ' +/- ' + str(round(stats.sem(after_store_ob),2)))

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,400)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([before_store_rz,after_store_rz],notch=True, sym='',showmeans=True)
    ax.set_xticklabels(['Before', 'After'])
    ax.set_xlim(0.5,2.5)
    ax.set_yticklabels(['', '', '', '','',''])

    print('Average gamma power in reward zone : movement = ' + str(round(np.nanmean(before_store_rz),2)) + ' +/- ' + str(round(stats.sem(before_store_rz),2)) + ' stationary = ' + str(round(np.nanmean(after_store_rz),2)) + ' +/- ' + str(round(stats.sem(after_store_rz),2)))

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('110 - 130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([before_store_hb,after_store_hb],notch=True, sym='',showmeans=True)
    ax.set_ylim(0,400)
    ax.set_xticklabels(['Before', 'After'])
    ax.set_xlim(0.5,2.5)
    ax.set_yticklabels(['', '', '', '','',''])

    print('Average gamma power in homebound region : movement = ' + str(round(np.nanmean(before_store_hb),2)) + ' +/- ' + str(round(stats.sem(before_store_hb),2)) + ' stationary = ' + str(round(np.nanmean(after_store_hb),2)) + ' +/- ' + str(round(stats.sem(after_store_hb),2)))

    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.13, right = 0.92, top = 0.9) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_stop&start_locations.png', dpi=200)
    plt.close()


def plot_gamma_power_difference_stop_start_location(prm,difference_ob,difference_rz, difference_hb,channel):

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.boxplot([difference_ob,difference_rz,difference_hb],notch=True, sym='',showmeans=True)
    ax.set_xlim(0.5,3.5)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.21, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_stop&start_locations_difference.png', dpi=200)
    plt.close()


def plot_gamma_power_stop_start_location_hit_miss(prm,after_store_ob_hit,after_store_rz_hit,after_store_hb_hit,before_store_ob_hit,before_store_rz_hit,before_store_hb_hit, after_store_ob_miss,after_store_rz_miss,after_store_hb_miss,before_store_ob_miss,before_store_rz_miss,before_store_hb_miss, channel):

    print('Plotting power calculations for before and after stops, according to location')

    # outbound
    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([before_store_ob_hit,after_store_ob_hit,before_store_ob_miss,after_store_ob_miss],notch=True, sym='',showmeans=True)
    ax.set_ylim(0,500)
    ax.set_xlim(0.5,4.5)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xticklabels(['Moving \n hit', 'Still \n hit, Moving \n miss', 'Still \n miss'])

    print('Average gamma power in outbound region (hit trials) : movement = ' + str(round(np.nanmean(before_store_ob_hit),2)) + ' +/- ' + str(round(stats.sem(before_store_ob_hit),2)) + ' stationary = ' + str(round(np.nanmean(after_store_ob_hit),2)) + ' +/- ' + str(round(stats.sem(after_store_ob_hit),2)))
    print('Average gamma power in outbound region (miss trials) : movement = ' + str(round(np.nanmean(before_store_ob_miss),2)) + ' +/- ' + str(round(stats.sem(before_store_ob_miss),2)) + ' stationary = ' + str(round(np.nanmean(after_store_ob_miss),2)) + ' +/- ' + str(round(stats.sem(after_store_ob_miss),2)))

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,500)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([before_store_rz_hit,after_store_rz_hit,before_store_rz_miss,after_store_rz_miss],notch=True, sym='',showmeans=True)
    ax.set_xticklabels(['Moving \n hit', 'Still \n hit, Moving \n miss', 'Still \n miss'])
    ax.set_xlim(0.5,4.5)
    ax.set_yticklabels(['', '', '', '','',''])

    print('Average gamma power in reward zone (hit trials) : movement = ' + str(round(np.nanmean(before_store_rz_hit),2)) + ' +/- ' + str(round(stats.sem(before_store_rz_hit),2)) + ' stationary = ' + str(round(np.nanmean(after_store_rz_hit),2)) + ' +/- ' + str(round(stats.sem(after_store_rz_hit),2)))
    print('Average gamma power in reward zone (miss trials) : movement = ' + str(round(np.nanmean(before_store_rz_miss),2)) + ' +/- ' + str(round(stats.sem(before_store_rz_miss),2)) + ' stationary = ' + str(round(np.nanmean(after_store_rz_miss),2)) + ' +/- ' + str(round(stats.sem(after_store_rz_miss),2)))

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('110 - 130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([before_store_hb_hit,after_store_hb_hit,before_store_hb_miss,after_store_hb_miss],notch=True, sym='',showmeans=True)
    ax.set_ylim(0,500)
    ax.set_xticklabels(['Moving \n hit', 'Still \n hit, Moving \n miss', 'Still \n miss'])
    ax.set_xlim(0.5,4.5)
    ax.set_yticklabels(['', '', '', '','',''])

    print('Average gamma power in homebound region (hit trials) : movement = ' + str(round(np.nanmean(before_store_hb_hit),2)) + ' +/- ' + str(round(stats.sem(before_store_hb_hit),2)) + ' stationary = ' + str(round(np.nanmean(after_store_hb_hit),2)) + ' +/- ' + str(round(stats.sem(after_store_hb_hit),2)))
    print('Average gamma power in homebound region (miss trials) : movement = ' + str(round(np.nanmean(before_store_hb_miss),2)) + ' +/- ' + str(round(stats.sem(before_store_hb_miss),2)) + ' stationary = ' + str(round(np.nanmean(after_store_hb_miss),2)) + ' +/- ' + str(round(stats.sem(after_store_hb_miss),2)))

    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.1, right = 0.92, top = 0.9) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_stop&start_locations_hit&miss.png', dpi=200)
    plt.close()



# speed versus power
def plot_gamma_power_speed(prm, bins,speed_bins, channel):

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(bins,speed_bins, 'o', color = 'k', label='after_stop')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins))
    bins = np.delete(bins,speed_bins_nan[:,0])
    speed_bins = np.delete(speed_bins,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins,speed_bins)
    ax.plot(bins,ablinevalues, '-',color = 'Black')

    #ax.errorbar(1,np.nanmean(store), stats.sem(store)/np.sqrt(len(store)), fmt = 'o', color = 'k', markersize=8,capsize = 1.5, elinewidth = 1.5)
    ax.set_ylim(65,140)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    #ax.set_xlabel('Stop', fontsize = 18, labelpad = 10)
    #ax.set_xticks(['0', '10', '20', '30', '40'])

    ax.text(0.7, 0.1, ('p_value'+ str(p_value)))
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.21, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_speedVgamma_power.png', dpi=200)
    plt.close()

    print('Speed versus gamma power : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))


def plot_theta_power_speed(prm, bins,speed_bins, channel):

    print('Plotting theta power versus speed')

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(bins,speed_bins, 'o', color = 'k', label='after_stop')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins))
    bins = np.delete(bins,speed_bins_nan[:,0])
    speed_bins = np.delete(speed_bins,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins,speed_bins)
    ax.plot(bins,ablinevalues, '-',color = 'Black')

    #ax.set_ylim(65,140)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    #ax.set_xlabel('Stop', fontsize = 18, labelpad = 10)
    #ax.set_xticks(['0', '10', '20', '30', '40'])

    ax.text(0.7, 0.1, ('p_value'+ str(p_value)))
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.21, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_speedVtheta_power.png', dpi=200)
    plt.close()


def plot_gamma_power_speed_hit_miss(prm, bins_hit,speed_bins_hit,bins_miss,speed_bins_miss, channel):

    print('Plotting gamma power versus speed for hit and miss trials')

    fig = plt.figure(figsize = (8,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(bins_hit,speed_bins_hit, 'o', color = 'k', label='hit trial')
    ax.plot(bins_miss,speed_bins_miss, 'o', color = 'b', label='miss trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit))
    bins_hit = np.delete(bins_hit,speed_bins_nan[:,0])
    speed_bins_hit = np.delete(speed_bins_hit,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit,speed_bins_hit)
    ax.plot(bins_hit,ablinevalues, '-',color = 'Black')
    ax.text(0.7, 0.1, 'p_value'+ str(p_value))

    print('Speed versus gamma power (hit trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss))
    bins_miss = np.delete(bins_miss,speed_bins_nan[:,0])
    speed_bins_miss = np.delete(speed_bins_miss,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss,speed_bins_miss)
    ax.plot(bins_miss,ablinevalues, '-',color = 'Blue')

    print('Speed versus gamma power (miss trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    #ax.set_ylim(60,140)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    #ax.set_xlabel('Stop', fontsize = 18, labelpad = 10)
    #ax.set_xticks(['0', '10', '20', '30', '40'])
    vr_plot_utility.makelegend(fig,ax, 0.7)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.18, right = 0.72, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_speedVgamma_power_hit&miss.png', dpi=200)
    plt.close()


def plot_theta_power_speed_hit_miss(prm, bins_hit,speed_bins_hit,bins_miss,speed_bins_miss, channel):

    print('Plotting theta power versus speed for hit and miss trials')

    fig = plt.figure(figsize = (8,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(bins_hit,speed_bins_hit, 'o', color = 'k', label='hit trial')
    ax.plot(bins_miss,speed_bins_miss, 'o', color = 'b', label='miss trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit))
    bins_hit = np.delete(bins_hit,speed_bins_nan[:,0])
    speed_bins_hit = np.delete(speed_bins_hit,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit,speed_bins_hit)
    ax.plot(bins_hit,ablinevalues, '-',color = 'Black')
    ax.text(0.7, 0.1, 'p_value'+ str(p_value))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss))
    bins_miss = np.delete(bins_miss,speed_bins_nan[:,0])
    speed_bins_miss = np.delete(speed_bins_miss,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss,speed_bins_miss)
    ax.plot(bins_miss,ablinevalues, '-',color = 'Blue')
    ax.text(0.7, 0.15, 'p_value'+ str(p_value), color = 'b')

    #ax.set_ylim(60,140)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    #ax.set_xlabel('Stop', fontsize = 18, labelpad = 10)
    #ax.set_xticks(['0', '10', '20', '30', '40'])
    vr_plot_utility.makelegend(fig,ax, 0.7)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.18, right = 0.72, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_speedVtheta_power_hit&miss.png', dpi=200)
    plt.close()


def plot_gamma_power_speed_hit_miss_success(prm, bins_hit,speed_bins_hit,bins_miss,speed_bins_miss,bins_success,speed_bins_success, channel):

    print('Plotting gamma power versus speed for hit,miss and successful trials')

    fig = plt.figure(figsize = (8,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(bins_hit,speed_bins_hit, 'o', color = 'k', label='Hit trial')
    ax.plot(bins_miss,speed_bins_miss, 'o', color = 'b', label='Miss trial')
    ax.plot(bins_success,speed_bins_success, 'o', color = 'r', label='Success trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit))
    bins_hit = np.delete(bins_hit,speed_bins_nan[:,0])
    speed_bins_hit = np.delete(speed_bins_hit,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit,speed_bins_hit)
    ax.plot(bins_hit,ablinevalues, '-',color = 'Black')

    print('Speed versus gamma power (hit trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss))
    bins_miss = np.delete(bins_miss,speed_bins_nan[:,0])
    speed_bins_miss = np.delete(speed_bins_miss,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss,speed_bins_miss)
    ax.plot(bins_miss,ablinevalues, '-',color = 'Blue')

    print('Speed versus gamma power (miss trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_success))
    bins_success = np.delete(bins_success,speed_bins_nan[:,0])
    speed_bins_success = np.delete(speed_bins_success,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_success,speed_bins_success)
    ax.plot(bins_success,ablinevalues, '-',color = 'r')

    print('Speed versus gamma power (successful trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    #ax.set_ylim(60,140)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    #ax.set_xlabel('Stop', fontsize = 18, labelpad = 10)
    #ax.set_xticks(['0', '10', '20', '30', '40'])
    vr_plot_utility.makelegend(fig,ax, 0.7)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.18, right = 0.72, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_speedVgamma_power_hit&miss&success.png', dpi=200)
    plt.close()


def plot_theta_power_speed_hit_miss_success(prm, bins_hit,speed_bins_hit,bins_miss,speed_bins_miss,bins_success,speed_bins_success, channel):

    print('Plotting theta power versus speed for hit,miss and successful trials')

    fig = plt.figure(figsize = (8,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.plot(bins_hit,speed_bins_hit, 'o', color = 'k', label='Hit trial')
    ax.plot(bins_miss,speed_bins_miss, 'o', color = 'b', label='Miss trial')
    ax.plot(bins_success,speed_bins_success, 'o', color = 'r', label='Success trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit))
    bins_hit = np.delete(bins_hit,speed_bins_nan[:,0])
    speed_bins_hit = np.delete(speed_bins_hit,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit,speed_bins_hit)
    ax.plot(bins_hit,ablinevalues, '-',color = 'Black')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss))
    bins_miss = np.delete(bins_miss,speed_bins_nan[:,0])
    speed_bins_miss = np.delete(speed_bins_miss,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss,speed_bins_miss)
    ax.plot(bins_miss,ablinevalues, '-',color = 'Blue')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_success))
    bins_success = np.delete(bins_success,speed_bins_nan[:,0])
    speed_bins_success = np.delete(speed_bins_success,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_success,speed_bins_success)
    ax.plot(bins_success,ablinevalues, '-',color = 'r')

    #ax.set_ylim(60,140)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    #ax.set_xlabel('Stop', fontsize = 18, labelpad = 10)
    #ax.set_xticks(['0', '10', '20', '30', '40'])
    vr_plot_utility.makelegend(fig,ax, 0.7)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.18, right = 0.72, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_speedVtheta_power_hit&miss&success.png', dpi=200)
    plt.close()


def plot_gamma_power_speed_hit_miss_locations(prm, bins_hit_ob,speed_bins_hit_ob,bins_miss_ob,speed_bins_miss_ob,bins_hit_rz,speed_bins_hit_rz,bins_miss_rz,speed_bins_miss_rz, bins_hit_hb,speed_bins_hit_hb,bins_miss_hb,speed_bins_miss_hb, channel):

    print('Plotting gamma power versus speed for hit and miss trials, according to location')

    fig = plt.figure(figsize = (14,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)

    ax.plot(bins_hit_ob,speed_bins_hit_ob, 'o', color = 'k', label='Hit trial')
    ax.plot(bins_miss_ob,speed_bins_miss_ob, 'o', color = 'b', label='Miss trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit_ob))
    bins_hit_ob = np.delete(bins_hit_ob,speed_bins_nan[:,0])
    speed_bins_hit_ob = np.delete(speed_bins_hit_ob,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit_ob,speed_bins_hit_ob)
    ax.plot(bins_hit_ob,ablinevalues, '-',color = 'Black')

    print('Speed versus gamma power in outbound region (hit trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss_ob))
    bins_miss_ob = np.delete(bins_miss_ob,speed_bins_nan[:,0])
    speed_bins_miss_ob = np.delete(speed_bins_miss_ob,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss_ob,speed_bins_miss_ob)
    ax.plot(bins_miss_ob,ablinevalues, '-',color = 'Blue')
    ax.set_xticklabels(['hit', 'Miss'])
    ax.set_ylim(60,300)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    print('Speed versus gamma power in outbound region (miss trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #ax.set_ylim(60,150)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.plot(bins_hit_rz,speed_bins_hit_rz, 'o', color = 'k', label='Hit trial')
    ax.plot(bins_miss_rz,speed_bins_miss_rz, 'o', color = 'b', label='Miss trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit_rz))
    bins_hit_rz = np.delete(bins_hit_rz,speed_bins_nan[:,0])
    speed_bins_hit_rz = np.delete(speed_bins_hit_rz,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit_rz,speed_bins_hit_rz)
    ax.plot(bins_hit_rz,ablinevalues, '-',color = 'Black')
    #ax.text(0.5, 0.1, ('p_value'+ str(p_value)))

    print('Speed versus gamma power in reward zone (hit trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss_rz))
    bins_miss_rz = np.delete(bins_miss_rz,speed_bins_nan[:,0])
    speed_bins_miss_rz = np.delete(speed_bins_miss_rz,speed_bins_nan[:,0])
    ablinevalues,slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss_rz,speed_bins_miss_rz)
    ax.plot(bins_miss_rz,ablinevalues, '-',color = 'Blue')
    ax.set_ylim(60,300)

    print('Speed versus gamma power in reward zone (miss trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    vr_plot_utility.makelegend(fig,ax, 0.7)
    ax.set_xticklabels(['hit', 'Miss'])
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('110 - 130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(60,300)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.plot(bins_hit_hb,speed_bins_hit_hb, 'o', color = 'k', label='hit trial')
    ax.plot(bins_miss_hb,speed_bins_miss_hb, 'o', color = 'b', label='hit trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit_hb))
    bins_hit_hb = np.delete(bins_hit_hb,speed_bins_nan[:,0])
    speed_bins_hit_hb = np.delete(speed_bins_hit_hb,speed_bins_nan[:,0])
    ablinevalues,slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit_hb,speed_bins_hit_hb)
    ax.plot(bins_hit_hb,ablinevalues, '-',color = 'Black', linewidth = 1)

    print('Speed versus gamma power in homebound region (hit trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss_hb))
    bins_miss_hb = np.delete(bins_miss_hb,speed_bins_nan[:,0])
    speed_bins_miss_hb = np.delete(speed_bins_miss_hb,speed_bins_nan[:,0])
    ablinevalues,slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss_hb,speed_bins_miss_hb)
    ax.plot(bins_miss_hb,ablinevalues, '-',color = 'Blue', linewidth = 1)
    #ax.text(0.7, 0.75, ('p_value'+ str(p_value)))
    ax.set_xticklabels(['hit', 'Miss'])

    print('Speed versus gamma power in homebound region (miss trials) : p value = ' + str(p_value) + ', slope = ' + str(slope) + ', r value = ' + str(r_value) + ', intercept =  ' + str(intercept))


    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.1, right = 0.85, top = 0.8) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_speedVgamma_power_hit&miss_locations.png', dpi=200)
    plt.close()


def plot_theta_power_speed_hit_miss_locations(prm, bins_hit_ob,speed_bins_hit_ob,bins_miss_ob,speed_bins_miss_ob,bins_hit_rz,speed_bins_hit_rz,bins_miss_rz,speed_bins_miss_rz, bins_hit_hb,speed_bins_hit_hb,bins_miss_hb,speed_bins_miss_hb, channel):

    print('Plotting theta power versus speed for hit and miss trials, according to location')

    fig = plt.figure(figsize = (14,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)

    ax.plot(bins_hit_ob,speed_bins_hit_ob, 'o', color = 'k', label='Hit trial')
    ax.plot(bins_miss_ob,speed_bins_miss_ob, 'o', color = 'b', label='Miss trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit_ob))
    bins_hit_ob = np.delete(bins_hit_ob,speed_bins_nan[:,0])
    speed_bins_hit_ob = np.delete(speed_bins_hit_ob,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit_ob,speed_bins_hit_ob)
    ax.plot(bins_hit_ob,ablinevalues, '-',color = 'Black')
    #ax.text(0.3, 0.1, 'p_value'+ str(p_value))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss_ob))
    bins_miss_ob = np.delete(bins_miss_ob,speed_bins_nan[:,0])
    speed_bins_miss_ob = np.delete(speed_bins_miss_ob,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss_ob,speed_bins_miss_ob)
    ax.plot(bins_miss_ob,ablinevalues, '-',color = 'Blue')
    #ax.text(0.3, 0.15, 'p_value'+ str(p_value))
    ax.set_xticklabels(['hit', 'Miss'])

    ax.set_ylim(60,600)
    ax.set_ylabel('Avg area (PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #ax.set_ylim(60,150)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.plot(bins_hit_rz,speed_bins_hit_rz, 'o', color = 'k', label='Hit trial')
    ax.plot(bins_miss_rz,speed_bins_miss_rz, 'o', color = 'b', label='Miss trial')

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit_rz))
    bins_hit_rz = np.delete(bins_hit_rz,speed_bins_nan[:,0])
    speed_bins_hit_rz = np.delete(speed_bins_hit_rz,speed_bins_nan[:,0])
    ablinevalues, slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit_rz,speed_bins_hit_rz)
    ax.plot(bins_hit_rz,ablinevalues, '-',color = 'Black')
    #ax.text(0.5, 0.1, ('p_value'+ str(p_value)))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss_rz))
    bins_miss_rz = np.delete(bins_miss_rz,speed_bins_nan[:,0])
    speed_bins_miss_rz = np.delete(speed_bins_miss_rz,speed_bins_nan[:,0])
    ablinevalues,slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss_rz,speed_bins_miss_rz)
    ax.plot(bins_miss_rz,ablinevalues, '-',color = 'Blue')
    #ax.text(0.5, 0.15, ('p_value'+ str(p_value)))
    ax.set_ylim(60,600)

    vr_plot_utility.makelegend(fig,ax, 0.7)
    ax.set_xticklabels(['hit', 'Miss'])
    ax.set_xlabel('Speed (cm/s)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('110 - 130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(60,600)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.plot(bins_hit_hb,speed_bins_hit_hb, 'o', color = 'k', label='hit trial')
    ax.plot(bins_miss_hb,speed_bins_miss_hb, 'o', color = 'b', label='hit trial')
    speed_bins_nan = np.argwhere(np.isnan(speed_bins_hit_hb))
    bins_hit_hb = np.delete(bins_hit_hb,speed_bins_nan[:,0])
    speed_bins_hit_hb = np.delete(speed_bins_hit_hb,speed_bins_nan[:,0])
    ablinevalues,slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_hit_hb,speed_bins_hit_hb)
    ax.plot(bins_hit_hb,ablinevalues, '-',color = 'Black', linewidth = 1)
    #ax.text(0.7, 0.7, ('p_value'+ str(p_value)))

    speed_bins_nan = np.argwhere(np.isnan(speed_bins_miss_hb))
    bins_miss_hb = np.delete(bins_miss_hb,speed_bins_nan[:,0])
    speed_bins_miss_hb = np.delete(speed_bins_miss_hb,speed_bins_nan[:,0])
    ablinevalues,slope,intercept,r_value, p_value=vr_power_calculations.linear_regression(bins_miss_hb,speed_bins_miss_hb)
    ax.plot(bins_miss_hb,ablinevalues, '-',color = 'Blue', linewidth = 1)
    #ax.text(0.7, 0.75, ('p_value'+ str(p_value)))

    ax.set_xticklabels(['hit', 'Miss'])

    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.1, right = 0.85, top = 0.8) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_speedVtheta_power_hit&miss_locations.png', dpi=200)
    plt.close()



# avg power plots split on hit and miss
def plot_gamma_power_hit_miss(prm, hit_power,miss_power, channel):

    print('Plotting power calculations for hit and miss trials')

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.boxplot([hit_power,miss_power], notch=True, sym='',showmeans=True)
    ax.set_xlim(0.5,2.5)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_ylabel('Area diff (PSD (V^2/Hz))', fontsize = 18, labelpad = 10)
    #ax.set_xlabel('Stop', fontsize = 18, labelpad = 10)
    ax.set_xticklabels(['Hit', 'Miss'])
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.21, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_hit&miss.png', dpi=200)
    plt.close()

    print('Average gamma power : hit trials = ' + str(round(np.nanmean(hit_power),2)) + ' +/- ' + str(round(stats.sem(hit_power),2)) + ' miss trials = ' + str(round(np.nanmean(miss_power),2)) + ' +/- ' + str(round(stats.sem(miss_power),2)))


def plot_theta_power_hit_miss(prm, hit_power,miss_power, channel):

    print('Plotting power calculations for hit and miss trials')

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.boxplot([hit_power,miss_power], notch=True, sym='',showmeans=True)
    ax.set_xlim(0.5,2.5)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_ylabel('Area diff (PSD (V^2/Hz))', fontsize = 18, labelpad = 10)
    #ax.set_xlabel('Stop', fontsize = 18, labelpad = 10)
    ax.set_xticklabels(['Hit', 'Miss'])
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.21, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgThetaPower_hit&miss.png', dpi=200)
    plt.close()


def plot_gamma_power_hit_miss_success(prm, hit_power,miss_power, success_power,channel):

    print('Plotting power calculations for hit, miss and successful trials')

    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.boxplot([success_power,hit_power,miss_power], notch=True, sym='',showmeans=True)
    ax.set_xlim(0.5,3.5)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_ylabel('Area diff (PSD (V^2/Hz))', fontsize = 18, labelpad = 10)
    ax.set_xticklabels(['Success','Hit', 'Miss'])
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.21, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_hit&miss&success.png', dpi=200)
    plt.close()
    print('Average gamma power : hit trials = ' + str(round(np.nanmean(hit_power),2)) + ' +/- ' + str(round(stats.sem(hit_power),2)) + ' miss trials = ' + str(round(np.nanmean(miss_power),2)) + ' +/- ' + str(round(stats.sem(miss_power),2)) + ' success trials = ' + str(round(np.nanmean(success_power),2)) + ' +/- ' + str(round(stats.sem(success_power),2)))


def plot_theta_power_hit_miss_success(prm, hit_power,miss_power, success_power,channel):

    print('Plotting power calculations for hit, miss and successful trials')

    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.boxplot([success_power,hit_power,miss_power], notch=True, sym='',showmeans=True)
    ax.set_xlim(0.5,3.5)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.set_ylabel('Area diff (PSD (V^2/Hz))', fontsize = 18, labelpad = 10)
    ax.set_xticklabels(['Success','Hit', 'Miss'])
    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.21, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgThetaPower_hit&miss&success.png', dpi=200)
    plt.close()


def plot_gamma_power_hit_miss_locations(prm, hit_power_ob,miss_power_ob, hit_power_rz,miss_power_rz,hit_power_hb,miss_power_hb,channel):

    print('Plotting power calculations for hit and miss trials, according to location')


    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('Outbound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([hit_power_ob,miss_power_ob], notch=True, sym='',showmeans=True)
    ax.set_ylim(0,250)
    ax.set_xticklabels(['Hit', 'Miss'])
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    print('Average gamma power in outbound region : hit trials = ' + str(round(np.nanmean(hit_power_ob),2)) + ' +/- ' + str(round(stats.sem(hit_power_ob),2)) + ' miss trials = ' + str(round(np.nanmean(miss_power_ob),2)) + ' +/- ' + str(round(stats.sem(miss_power_ob),2)))

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #ax.set_ylim(60,150)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([hit_power_rz,miss_power_rz], notch=True, sym='',showmeans=True)
    ax.set_ylim(0,250)
    ax.set_xticklabels(['Hit', 'Miss'])
    ax.set_yticklabels(['','', '', '', '', ''])

    print('Average gamma power in reward zone : hit trials = ' + str(round(np.nanmean(hit_power_rz),2)) + ' +/- ' + str(round(stats.sem(hit_power_rz),2)) + ' miss trials = ' + str(round(np.nanmean(miss_power_rz),2)) + ' +/- ' + str(round(stats.sem(miss_power_rz),2)))

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('Homebound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,250)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([hit_power_hb,miss_power_hb], notch=True, sym='',showmeans=True)
    ax.set_xticklabels(['Hit', 'Miss'])
    ax.set_yticklabels(['','', '', '', '', ''])

    print('Average gamma power in homebound region : hit trials = ' + str(round(np.nanmean(hit_power_hb),2)) + ' +/- ' + str(round(stats.sem(hit_power_hb),2)) + ' miss trials = ' + str(round(np.nanmean(miss_power_hb),2)) + ' +/- ' + str(round(stats.sem(miss_power_hb),2)))

    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.13, right = 0.92, top = 0.8) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_hit&miss_locations.png', dpi=200)
    plt.close()


def plot_theta_power_hit_miss_locations(prm, hit_power_ob,miss_power_ob, hit_power_rz,miss_power_rz,hit_power_hb,miss_power_hb,channel):

    print('Plotting power calculations for hit and miss trials, according to location')


    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('Outbound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([hit_power_ob,miss_power_ob], notch=True, sym='',showmeans=True)
    ax.set_ylim(0,700)
    ax.set_xticklabels(['Hit', 'Miss'])
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #ax.set_ylim(60,150)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([hit_power_rz,miss_power_rz], notch=True, sym='',showmeans=True)
    ax.set_ylim(0,700)
    ax.set_xticklabels(['Hit', 'Miss'])

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('Homebound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,700)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([hit_power_hb,miss_power_hb], notch=True, sym='',showmeans=True)
    ax.set_xticklabels(['Hit', 'Miss'])

    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.1, right = 0.92, top = 0.8) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgThetaPower_hit&miss_locations.png', dpi=200)
    plt.close()


def plot_gamma_power_hit_miss_success_locations(prm, hit_power_ob,miss_power_ob, success_power_ob,hit_power_rz,miss_power_rz,success_power_rz,hit_power_hb,miss_power_hb,success_power_hb,channel):

    print('Plotting power calculations for hit miss and successful trials, according to location')

    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('Outbound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([miss_power_ob,hit_power_ob,success_power_ob], notch=True, sym='',showmeans=True)
    ax.set_ylim(0,210)
    ax.set_xticklabels(['Miss','Hit', 'Success'])
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    print('Average gamma power in outbound region : hit trials = ' + str(round(np.nanmean(hit_power_ob),2)) + ' +/- ' + str(round(stats.sem(hit_power_ob),2)) + ' miss trials = ' + str(round(np.nanmean(miss_power_ob),2)) + ' +/- ' + str(round(stats.sem(miss_power_ob),2)) + ' success trials = ' + str(round(np.nanmean(success_power_ob),2)) + ' +/- ' + str(round(stats.sem(success_power_ob),2)))

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #ax.set_ylim(60,150)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([miss_power_rz,hit_power_rz,success_power_rz], notch=True, sym='',showmeans=True)
    ax.set_ylim(0,210)
    ax.set_xticklabels(['Miss','Hit', 'Success'])
    ax.set_yticklabels(['','', '', ''])

    print('Average gamma power in reward zone : hit trials = ' + str(round(np.nanmean(hit_power_rz),2)) + ' +/- ' + str(round(stats.sem(hit_power_rz),2)) + ' miss trials = ' + str(round(np.nanmean(miss_power_rz),2)) + ' +/- ' + str(round(stats.sem(miss_power_rz),2)) + ' success trials = ' + str(round(np.nanmean(success_power_rz),2)) + ' +/- ' + str(round(stats.sem(success_power_rz),2)))

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('Homebound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,210)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([miss_power_hb,hit_power_hb,success_power_hb], notch=True, sym='',showmeans=True)
    ax.set_xticklabels(['Miss','Hit', 'Success'])
    ax.set_yticklabels(['','', '', ''])

    print('Average gamma power in homebound region : hit trials = ' + str(round(np.nanmean(hit_power_hb),2)) + ' +/- ' + str(round(stats.sem(hit_power_hb),2)) + ' miss trials = ' + str(round(np.nanmean(miss_power_hb),2)) + ' +/- ' + str(round(stats.sem(miss_power_hb),2)) + ' success trials = ' + str(round(np.nanmean(success_power_hb),2)) + ' +/- ' + str(round(stats.sem(success_power_hb),2)))

    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.12, right = 0.94, top = 0.8) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgGammaPower_hit&miss&success_locations.png', dpi=200)
    plt.close()


def plot_theta_power_hit_miss_success_locations(prm, hit_power_ob,miss_power_ob, success_power_ob,hit_power_rz,miss_power_rz,success_power_rz,hit_power_hb,miss_power_hb,success_power_hb,channel):

    print('Plotting power calculations for hit miss and successful trials, according to location')

    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('Outbound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([miss_power_ob,hit_power_ob,success_power_ob], notch=True, sym='',showmeans=True)
    ax.set_ylim(0,220)
    ax.set_xticklabels(['Miss','Hit', 'Success'])
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    #ax.set_ylim(60,150)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([miss_power_rz,hit_power_rz,success_power_rz], notch=True, sym='',showmeans=True)
    ax.set_ylim(0,220)
    ax.set_xticklabels(['Miss','Hit', 'Success'])
    ax.set_yticklabels(['','', '', ''])

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('Homebound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,220)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    ax.boxplot([miss_power_hb,hit_power_hb, success_power_hb], notch=True, sym='',showmeans=True)
    ax.set_xticklabels(['Miss','Hit', 'Success'])
    ax.set_yticklabels(['','', '', ''])

    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.12, right = 0.94, top = 0.8) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/pooled_data/CH' + str(channel) + '_AvgThetaPower_hit&miss&success_locations.png', dpi=200)
    plt.close()

