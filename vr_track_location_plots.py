
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



# power spectras for before and after stop data

def plot_power_spectrum_before_after_stop(prm, before_stop, after_stop, channel):
    ephys_path = prm.get_filepath() + 'Electrophysiology'
    data_path = ephys_path + '/Data'
    analysis_path = ephys_path + '/Analysis'
    spike_path = ephys_path + '/Spike_sorting'

    if os.path.exists(ephys_path) is False:
        print('Behavioural data will be saved in {}.'.format(ephys_path))
        os.makedirs(ephys_path)
        os.makedirs(data_path)
        os.makedirs(analysis_path)
        os.makedirs(spike_path)

    print('Plotting and saving power spectra for before (moving) and after (not moving) stops')

    # beforestop
    fig = plt.figure(figsize = (8,4.5)) # figsize = (width, height)
    ax = fig.add_subplot(121)
    ax.set_title('Before stop', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,20)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop[:7500], 30000, color='k', label='middle upper')
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    # afterstop
    ax = fig.add_subplot(122)
    ax.set_title('After stop', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,20)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop[:7500], 30000, color='k', label='middle upper')
    plt.subplots_adjust(hspace = .35, wspace = .4,  bottom = 0.2, left = 0.13, right = 0.82, top = 0.87) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_before&after.png', dpi=200)
    plt.close()


def plot_power_spectrum_track_locations(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel):


    print('Plotting and saving power spectra for track locations')

    # outbound
    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(121)
    ax.set_title('After stop', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_outbound[:7500], 30000, color='k', label='70 - 90 cm')
    vr_fft.power_spectrum_log(prm, ax, after_stop_rewardzone[:7500], 30000, color='b', label='Reward zone')
    vr_fft.power_spectrum_log(prm, ax, after_stop_homebound[:7500], 30000, color='r', label='110 - 130 cm')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(122)
    ax.set_title('Before stop', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,60)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_outbound[:7500], 30000, color='k', label='70 - 90 cm')
    vr_fft.power_spectrum_log(prm, ax, before_stop_rewardzone[:7500], 30000, color='b', label='Reward zone')
    vr_fft.power_spectrum_log(prm, ax, before_stop_homebound[:7500], 30000, color='r', label='110 - 130 cm')
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)

    plt.subplots_adjust(hspace = .35, wspace = .4,  bottom = 0.2, left = 0.13, right = 0.72, top = 0.87) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_before&after_locations.png', dpi=200)
    plt.close()


def plot_power_spectrum_track_locations_gamma2(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel):


    print('Plotting and saving power spectra for track locations')

    # outbound
    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(121)
    ax.set_title('After stop', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_outbound[:7500], 30000, color='k', label='70 - 90 cm')
    vr_fft.power_spectrum_log(prm, ax, after_stop_rewardzone[:7500], 30000, color='b', label='Reward zone')
    vr_fft.power_spectrum_log(prm, ax, after_stop_homebound[:7500], 30000, color='r', label='110 - 130 cm')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(122)
    ax.set_title('Before stop', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_outbound[:7500], 30000, color='k', label='70 - 90 cm')
    vr_fft.power_spectrum_log(prm, ax, before_stop_rewardzone[:7500], 30000, color='b', label='Reward zone')
    vr_fft.power_spectrum_log(prm, ax, before_stop_homebound[:7500], 30000, color='r', label='110 - 130 cm')
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)
    ax.set_yticklabels(['', '', '', '','',''])
    plt.subplots_adjust(hspace = .35, wspace = .4,  bottom = 0.2, left = 0.13, right = 0.72, top = 0.87) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + 'PowerSpec_before&after_locations_gamma3.png', dpi=200)
    plt.close()

def plot_power_spectrum_track_locations_gamma3(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel):


    print('Plotting and saving power spectra for track locations')

    # outbound
    fig = plt.figure(figsize = (12,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('Outbound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_outbound[:7500], 30000, color='k', label='After stop')
    vr_fft.power_spectrum_log(prm, ax, before_stop_outbound[:7500], 30000, color='b', label='Before stop')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(132)
    ax.set_title('Reward zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_rewardzone[:7500], 30000, color='k', label='After stop')
    vr_fft.power_spectrum_log(prm, ax, before_stop_rewardzone[:7500], 30000, color='b', label='Before stop')
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)
    ax.set_yticklabels(['', '', '', '','',''])

    ax = fig.add_subplot(133)
    ax.set_title('Homebound', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_homebound[:7500], 30000, color='k', label='After stop')
    vr_fft.power_spectrum_log(prm, ax, before_stop_homebound[:7500], 30000, color='b', label='Before stop')
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)
    ax.set_yticklabels(['', '', '', '','',''])

    plt.subplots_adjust(hspace = .35, wspace = .4,  bottom = 0.2, left = 0.13, right = 0.72, top = 0.87) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_before&after_locations_gamma.png', dpi=200)
    plt.close()

def plot_power_spectrum_track_locations_gamma(prm, after_stop_outbound, after_stop_rewardzone, after_stop_homebound, before_stop_outbound, before_stop_rewardzone,  before_stop_homebound, channel):


    print('Plotting and saving power spectra for track locations (gamma)')

    # outbound
    fig = plt.figure(figsize = (12,12)) # figsize = (width, height)

    ax = fig.add_subplot(321)
    ax.set_title('After stop (stationary) \n 70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_outbound[:7500], 30000, color='k', label='middle upper')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(323)
    ax.set_title('Reward zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_rewardzone[:7500], 30000, color='k', label='middle upper')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    # reward zone
    ax = fig.add_subplot(325)
    ax.set_title('110-130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, after_stop_homebound[:7500], 30000, color='k', label='middle upper')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)


    ax = fig.add_subplot(322)
    ax.set_title('Before stop (moving) \n 70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_outbound[:7500], 30000, color='k', label='middle upper')

    # homebound
    ax = fig.add_subplot(324)
    ax.set_title('Reward zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_rewardzone[:7500], 30000, color='k', label='middle upper')

    ax = fig.add_subplot(326)
    ax.set_title('110-130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, before_stop_homebound[:7500], 30000, color='k', label='middle upper')
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.1, left = 0.13, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_before&after_locations_gamma.png', dpi=200)
    plt.close()



# plots for speed

def plot_power_spectrum_speed(prm, upper,middle_upper, middle_lower, lower, channel):

    print('Plotting and saving power spectra for speed quartiles')

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,40)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, upper[:7500], 30000, color='r', label='Upper quartile')
    vr_fft.power_spectrum_log(prm, ax, middle_upper[:7500], 30000, color='k', label='Middle upper quartile')
    vr_fft.power_spectrum_log(prm, ax, middle_lower[:7500], 30000, color='b', label='Middle lower quartile')
    vr_fft.power_spectrum_log(prm, ax, lower[:7500], 30000, color='g', label='Lower quartile')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_SpeedQuartiles.png', dpi=200)
    plt.close()


def plot_power_spectrum_speed_gamma(prm, upper,middle_upper, middle_lower, lower, channel):


    print('Plotting and saving power spectra for speed quartile (gamma)')

    # outbound
    fig = plt.figure(figsize = (9,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, middle_upper[:7500], 30000, color='k', label='Middle upper quartile')
    vr_fft.power_spectrum_log(prm, ax, upper[:7500], 30000, color='r', label='Upper quartile')
    vr_fft.power_spectrum_log(prm, ax, middle_lower[:7500], 30000, color='b', label='Middle lower quartile')
    vr_fft.power_spectrum_log(prm, ax, lower[:7500], 30000, color='g', label='Lower quartile')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.9)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.72, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_SpeedQuartiles_gamma.png', dpi=200)
    plt.close()


def plot_power_spectrum_speed_locations_gamma(prm, outbound_m_upper,outbound_upper,outbound_m_lower,outbound_lower,rz_m_upper,rz_upper,rz_m_lower,rz_lower,hb_m_upper,hb_upper,hb_m_lower,hb_lower, channel):


    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (14,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(131)
    ax.set_title('70-90 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,8)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, outbound_m_upper[:7500], 30000, color = 'k', label = 'Middle upper quartile')
    vr_fft.power_spectrum_log(prm, ax, outbound_upper[:7500], 30000, color = 'r', label = 'Upper quartile')
    vr_fft.power_spectrum_log(prm, ax, outbound_m_lower[:7500], 30000, color = 'b', label = 'Lower middle quartile')
    vr_fft.power_spectrum_log(prm, ax, outbound_lower[:7500], 30000, color = 'g', label = 'Lower quartile')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(132)
    ax.set_title('Reward Zone', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,8)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, rz_m_upper[:7500], 30000, color = 'k', label = 'Middle upper quartile')
    vr_fft.power_spectrum_log(prm, ax, rz_upper[:7500], 30000, color = 'r', label = 'Upper quartile')
    vr_fft.power_spectrum_log(prm, ax, rz_m_lower[:7500], 30000, color = 'b', label = 'Lower middle quartile')
    vr_fft.power_spectrum_log(prm, ax, rz_lower[:7500], 30000, color = 'g', label = 'Lower quartile')
    ax.set_yticklabels(['', '', '', '','',''])
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)

    # reward zone
    ax = fig.add_subplot(133)
    ax.set_title('110 - 130 cm', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,8)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hb_m_upper[:7500], 30000, color = 'k', label = 'Middle upper quartile')
    vr_fft.power_spectrum_log(prm, ax, hb_upper[:7500], 30000, color = 'r', label = 'Upper quartile')
    vr_fft.power_spectrum_log(prm, ax, hb_m_lower[:7500], 30000, color = 'b', label = 'Lower middle quartile')
    vr_fft.power_spectrum_log(prm, ax, hb_lower[:7500], 30000, color = 'g', label = 'Lower quartile')
    ax.set_yticklabels(['', '', '', '','',''])
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    plt.subplots_adjust(hspace = .4, wspace = .3,  bottom = 0.2, left = 0.1, right = 0.72, top = 0.9) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_SpeedQuartiles_locations_gamma.png', dpi=200)
    plt.close()



# plots for hit and miss seperated data


def plot_power_spectrum_all_hitmiss_gamma(prm, hit,miss, channel):


    print('Plotting and saving power spectra for hit and miss trials ')

    # outbound
    fig = plt.figure(figsize = (8,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit[:7500], 30000, color='k', label='Hit')
    vr_fft.power_spectrum_log(prm, ax, miss[:7500], 30000, color='r', label='Miss')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.9)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.82, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_hit&miss_gamma.png', dpi=200)
    plt.close()


def plot_power_spectrum_all_hitmiss_success_gamma(prm, hit,miss, success,channel):


    print('Plotting and saving power spectra for hit and miss trials ')

    # outbound
    fig = plt.figure(figsize = (8,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,15)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit[:7500], 30000, color='k', label='Hit')
    vr_fft.power_spectrum_log(prm, ax, miss[:7500], 30000, color='r', label='Miss')
    vr_fft.power_spectrum_log(prm, ax, success[:7500], 30000, color='b', label='Success')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.9)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.82, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_hit&miss&success_gamma.png', dpi=200)
    plt.close()


def plot_power_spectrum_all_hitmiss(prm, hit,miss, channel):


    print('Plotting and saving power spectra for hit and miss trials ')

    # outbound
    fig = plt.figure(figsize = (8,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,20)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit[:7500], 30000, color='k', label='Hit')
    vr_fft.power_spectrum_log(prm, ax, miss[:7500], 30000, color='r', label='Miss')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.9)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.82, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_hit&miss.png', dpi=200)
    plt.close()


def plot_power_spectrum_all_hitmiss_success(prm, hit,miss, success, channel):


    print('Plotting and saving power spectra for hit and miss trials ')

    # outbound
    fig = plt.figure(figsize = (8,6)) # figsize = (width, height)

    ax = fig.add_subplot(111)
    #ax.set_title('middle_upper', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,30)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit[:7500], 30000, color='k', label='Hit')
    vr_fft.power_spectrum_log(prm, ax, miss[:7500], 30000, color='r', label='Miss')
    vr_fft.power_spectrum_log(prm, ax, success[:7500], 30000, color='b', label='Success')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.9)

    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.2, left = 0.16, right = 0.82, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_hit&miss&success.png', dpi=200)
    plt.close()


def plot_power_spectrum_hitmiss_gamma(prm, hit_before_stop,miss_before_stop, hit_after_stop, miss_after_stop, channel):

    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (10,4.5)) # figsize = (width, height)

    ax = fig.add_subplot(121)
    ax.set_title('Moving (before stop)', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit_before_stop[:7500], 30000, color = 'k', label = 'Hit trial')
    vr_fft.power_spectrum_log(prm, ax, miss_before_stop[:7500], 30000, color = 'b', label = 'Miss trial')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(122)
    ax.set_title('Stationary (after stop)', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit_after_stop[:7500], 30000, color = 'k', label = 'Hit trial')
    vr_fft.power_spectrum_log(prm, ax, miss_after_stop[:7500], 30000, color = 'b', label = 'Miss trial')
    ax.set_yticklabels(['', '', '', '','',''])
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)
    vr_plot_utility.makelegend(fig,ax, 0.7)

    plt.subplots_adjust(hspace = .35, wspace = .4,  bottom = 0.2, left = 0.13, right = 0.72, top = 0.87) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_hit&miss_before&after_gamma.png', dpi=200)
    plt.close()


def plot_power_spectrum_hitmiss_speed_gamma(prm, hit_middle_upper,hit_upper, hit_middle_lower, hit_lower,miss_middle_upper,miss_upper, miss_middle_lower, miss_lower, channel):

    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (10,10)) # figsize = (width, height)

    ax = fig.add_subplot(221)
    ax.set_title('Upper quartile', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,8)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit_upper[:7500], 30000, color = 'k', label = 'Hit trial')
    vr_fft.power_spectrum_log(prm, ax, miss_upper[:7500], 30000, color = 'b', label = 'Miss trial')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(222)
    ax.set_title('Upper middle quartile', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,8)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit_middle_upper[:7500], 30000, color = 'k', label = 'Hit trial')
    vr_fft.power_spectrum_log(prm, ax, miss_middle_upper[:7500], 30000, color = 'b', label = 'Miss trial')
    ax.set_yticklabels(['', '', '', '','',''])
    vr_plot_utility.makelegend(fig,ax, 0.3)

    ax = fig.add_subplot(223)
    ax.set_title('Lower middle quartile', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,8)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit_middle_lower[:7500], 30000, color = 'k', label = 'Hit trial')
    vr_fft.power_spectrum_log(prm, ax, miss_middle_lower[:7500], 30000, color = 'b', label = 'Miss trial')
    ax.set_ylabel('PSD (V^2/Hz)', fontsize = 18, labelpad = 10)
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)

    ax = fig.add_subplot(224)
    ax.set_title('Lower quartile', fontsize = 16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_ylim(0,10)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, hit_lower[:7500], 30000, color = 'k', label = 'Hit trial')
    vr_fft.power_spectrum_log(prm, ax, miss_lower[:7500], 30000, color = 'b', label = 'Miss trial')
    ax.set_yticklabels(['', '', '', '','',''])
    ax.set_xlabel('Frequency (Hz)', fontsize = 18, labelpad = 10)


    plt.subplots_adjust(hspace = .4, wspace = .4,  bottom = 0.1, left = 0.1, right = 0.82, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_PowerSpec_SpeedQuartiles_hit&miss_gamma.png', dpi=200)
    plt.close()





# continuous data plots

def plot_continuous_trials(prm, data, channel): # plots continuous data for an entire trial

    print('plotting continuous data per trial...')

    trials = np.unique(data[:,0]) # find unique trial numbers

    for tcount, trial in enumerate(trials[:]):
        array = data[data[:,0] == trial,:]
        start_time = 0 # in ms
        totaltime = int((array.shape[0])/30)
        end_time = totaltime + start_time # in ms

        try:

            fig = plt.figure(figsize = (14,8))

            # spikes
            ax = fig.add_subplot(411)
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),2])
            ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
            array_min = np.min(array[(start_time*30):(end_time*30),2])
            ax.set_ylim(array_min-10,)
            vr_plot_utility.adjust_spines(ax, ['left'])
            vr_plot_utility.plot_basics(prm,ax)
            vr_plot_utility.adjust_spine_thickness(ax)

            # LFP
            ax = fig.add_subplot(412)
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),3])
            ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
            ax.set_ylim(-200,200)
            vr_plot_utility.adjust_spines(ax, ['left'])
            vr_plot_utility.plot_basics(prm,ax)
            vr_plot_utility.adjust_spine_thickness(ax)

            # theta & gamma
            ax = fig.add_subplot(413)
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),4])
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),5])
            ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
            ax.set_ylim(-270,270)
            vr_plot_utility.adjust_spines(ax, ['left'])
            vr_plot_utility.plot_basics(prm,ax)
            vr_plot_utility.adjust_spine_thickness(ax)

            # location
            ax = fig.add_subplot(414)
            ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),1])
            ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
            ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
            ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
            ax.set_ylabel('Location (cm)', fontsize=18, labelpad = 20)
            vr_plot_utility.adjust_spines(ax, ['left','bottom'])
            vr_plot_utility.plot_basics(prm,ax)
            vr_plot_utility.adjust_spine_thickness(ax)

            plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.1, right = 0.92, top = 0.92)

            fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_Trial' + str(tcount+1) + '.png', dpi=200)
            plt.close()

        except ValueError:
                continue

        tcount+=1


def make_stop_start_continuous_plot(prm, channel, before_stop, after_stop):

    print('plotting continuous data...')

    start_time = 0 # in ms
    end_time = 250 # 250 ms

    fig = plt.figure(figsize = (12,10)) # figsize = (width, height)
    plot_graph(before_stop, start_time,end_time, fig)
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + 'ms_beforestop.png', dpi=200)
    plt.close()

    fig = plt.figure(figsize = (12,10)) # figsize = (width, height)
    plot_graph(after_stop, start_time,end_time, fig)
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + 'ms_afterstop.png', dpi=200)
    plt.close()


def plot_graph(array, start_time,end_time, fig):

    # spikes
    ax = fig.add_subplot(411)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),2])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),2])
    ax.set_ylim(array_min-10,)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # LFP
    ax = fig.add_subplot(412)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),3])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-200,200)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # theta & gamma
    ax = fig.add_subplot(413)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),4])
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),5])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-270,270)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # location
    ax = fig.add_subplot(414)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),1])
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
    ax.set_ylabel('Location (cm)', fontsize=18, labelpad = 20)
    vr_plot_utility.adjust_spines(ax, ['left','bottom'])
    vr_plot_utility.adjust_spine_thickness(ax)

    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.1, right = 0.92, top = 0.92)




"""""
def plot_graph(array, start_time,end_time, fig):

    # spikes
    ax = fig.add_subplot(411)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),2])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    array_min = np.min(array[(start_time*30):(end_time*30),2])
    ax.set_ylim(array_min-10,)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # LFP
    ax = fig.add_subplot(412)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),3])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-200,200)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # theta & gamma
    ax = fig.add_subplot(413)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),4])
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),5])
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_ylabel('Amplitude (uV)', fontsize=18, labelpad = 20)
    ax.set_ylim(-270,270)
    vr_plot_utility.adjust_spines(ax, ['left'])
    vr_plot_utility.adjust_spine_thickness(ax)

    # location
    ax = fig.add_subplot(414)
    ax.plot(np.arange(0,end_time-start_time,(1/30)),array[(start_time*30):(end_time*30),1])
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8,labelsize =18)
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.locator_params(axis = 'x', nbins=7) # set number of ticks on x axis
    ax.locator_params(axis = 'y', nbins=3) # set number of ticks on y axis
    ax.set_xlabel('Time (ms)', fontsize=18, labelpad = 20)
    ax.set_ylabel('Location (cm)', fontsize=18, labelpad = 20)
    vr_plot_utility.adjust_spines(ax, ['left','bottom'])
    vr_plot_utility.adjust_spine_thickness(ax)

    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.15, left = 0.1, right = 0.92, top = 0.92)




def plot_track_locations_examples(prm, location, channel, data='data'):

    print('plotting continuous data...')

    #data = data[data[:,1] > 3,:] # remove all data in black box
    trials = np.unique(data[:,0])

    for tcount, trial in enumerate(trials[10:20]): # only plot first 10 trials
        array = data[data[:,0] == trial,:]
        start_time = 0 # in ms
        totaltime = int((array.shape[0])/30)
        try:
            end_times = (np.array((1000,totaltime))) + start_time # in ms
            for t, times in enumerate(end_times):
                end_time = times

                if location ==0:

                    fig = plt.figure(figsize = (12,10)) # figsize = (width, height)
                    plot_graph(array, start_time,end_time, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_outbound.png', dpi=200)
                    plt.close()

                if location ==1:

                    fig = plt.figure(figsize = (8,10)) # figsize = (width, height)
                    plot_graph(array, start_time,end_time, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_rewardzone.png', dpi=200)
                    plt.close()

                if location ==2:

                    fig = plt.figure(figsize = (12,10)) # figsize = (width, height)
                    plot_graph(array, start_time,end_time, fig)
                    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/continuous/CH' + str(channel) + '_' + str(trial) + '_' + str(end_time-start_time) + 'ms_homebound.png', dpi=200)
                    plt.close()


        except ValueError:
            continue






def plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound, channel):
    ephys_path = prm.get_filepath() + 'Electrophysiology'
    data_path = ephys_path + '/Data'
    analysis_path = ephys_path + '/Analysis'
    spike_path = ephys_path + '/Spike_sorting'

    if os.path.exists(ephys_path) is False:
        print('Behavioural data will be saved in {}.'.format(ephys_path))
        os.makedirs(ephys_path)
        os.makedirs(data_path)
        os.makedirs(analysis_path)
        os.makedirs(spike_path)

    print('Plotting and saving power spectra')

    # outbound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, outbound, 30000)
    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.2, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_outbound.png', dpi=200)
    plt.close()

    # reward zone
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, rewardzone, 30000)
    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.2, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_rewardzone.png', dpi=200)
    plt.close()


    # homebound
    fig = plt.figure(figsize = (6,6)) # figsize = (width, height)
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.tick_params(axis='y', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    ax.tick_params(axis='x', pad = 10, top='off', right = 'off', direction = 'out',width = 2, length = 8, labelsize =18)
    vr_plot_utility.adjust_spine_thickness(ax)
    vr_fft.power_spectrum_log(prm, ax, homebound, 30000)
    plt.subplots_adjust(hspace = .35, wspace = .35,  bottom = 0.2, left = 0.2, right = 0.92, top = 0.92) # change spacing in figure
    fig.savefig(prm.get_filepath() + 'Electrophysiology/track_location_analysis/fft/CH' + str(channel) + '_homebound.png', dpi=200)
    plt.close()



def add_theta_and_gamma_signal(prm,outbound, rewardzone, homebound):
    outbound = outbound[:,4] + outbound[:,5]
    homebound = homebound[:,4] + homebound[:,5]
    rewardzone = rewardzone[:,4] + rewardzone[:,5]

    return outbound, rewardzone, homebound



def calculate_and_plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound, channel):

    # calculate and plot power spectrum
    outbound, rewardzone, homebound = add_theta_and_gamma_signal(prm,outbound, rewardzone, homebound)
    plot_power_spectrum_track_locations(prm, outbound, rewardzone, homebound,  channel)

"""""
